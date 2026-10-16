#!/usr/bin/env python3
"""Eval runner for the install-auditor skill (Python 3.9+, stdlib only).

Subcommands
-----------
validate   Schema and invariant check of evals/evals.json.
prepare    Snapshot the skill and write per-eval task prompts into an
           iteration directory outside the repo.
run        Execute prepared evals through `claude -p` (or print the commands
           with --dry-run).
grade      Grade saved outputs: deterministic assertions are checked in
           place; `contains_concept` assertions are handed to a model.
summary    Aggregate grading.json files into summary.md / summary.json.

Credentials
-----------
validate, prepare, deterministic grade, summary, run --dry-run and the unit
tests need no model and no credentials. `run` needs `claude -p` to be
authenticated (ANTHROPIC_API_KEY or a Claude login), or an orchestrating
agent that executes each task_prompt.md itself and saves the final message as
response.md. `grade --model-grader claude-cli`, or an agent-written
model_grading.json, is needed for the `contains_concept` assertions.

Layout
------
<workspace>/iteration-N/
    iteration_meta.json
    skill-snapshot/                      skill files the runs may read
    eval-<id>/
        eval_metadata.json
        task_prompt.md
        with_skill/run-1/
            outputs/                     executor cwd; the audit report lands here
            response.md                  final assistant message
            assistant_text.md, transcript.jsonl, timing.json, run_meta.json
            model_grader_prompt.md, model_grading.json, grading.json
    summary.md, summary.json

The workspace must live outside the skill repo: `claude -p` discovers
ancestor CLAUDE.md files, so a run inside the repo would inherit unrelated
instructions. The snapshot omits evals/, CLAUDE.md and .projex/closed/ so the
audited skill copy cannot see expected verdicts.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
EVALS_PATH = SKILL_ROOT / "evals" / "evals.json"
VERDICTS = ("APPROVED", "CONDITIONAL", "REJECTED")
DETERMINISTIC = {"exact_match", "verdict_check", "contains_string", "file_exists", "line_count_max"}
MODEL_GRADED = {"contains_concept"}
SNAPSHOT_DIRS = ("workflows/", "references/", "scripts/")
MIN_CASES_PER_WORKFLOW = 3
RUN_SUBDIR = Path("with_skill") / "run-1"

VERDICT_RE = re.compile(r"^[ \t>*_]*Verdict[ \t]*[:*]+[ \t*]*(APPROVED|CONDITIONAL|REJECTED)\b", re.M)
ROUTE_RE = re.compile(r"^\s*Routes to:\s*`?workflows/([a-z-]+)\.md", re.M)
SNAPSHOT_REF_RE = re.compile(r"\.projex/(\d{10}-[\w.-]+\.md)")

TASK_PROMPT_TEMPLATE = """\
You are performing an install audit using the install-auditor skill.

Skill path: {snapshot}
Read {snapshot}/SKILL.md first and follow it exactly. Relative paths in the skill (workflows/, references/, scripts/, .projex/) resolve against the skill path. Use only this copy of the skill, not any other installed install-auditor.

Working directory: {outputs}
Write every file you produce, including the audit report, into the working directory.

Safety: this is an audit. Never install, download-and-execute, pull, or run the subject under audit.

User request:
{prompt}
"""

MODEL_GRADER_INSTRUCTIONS = """\
You are grading the output of an install-auditor run against assertions.

Judge each numbered assertion only from the outputs provided below. An
assertion passes only if you can quote an evidence span from the outputs that
supports it; otherwise it fails. Do not use outside knowledge about the
package under audit.

Reply with only this JSON object and nothing else:
{"expectations": [{"index": <int>, "text": "<assertion text>", "passed": <true|false>, "evidence": "<quoted span or reason>"}]}
"""


# Loading and validation

def load_evals(path: Path = EVALS_PATH) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def known_workflows(root: Path = SKILL_ROOT) -> set[str]:
    return {p.stem for p in (root / "workflows").glob("*.md")}


def skill_frontmatter_name(root: Path = SKILL_ROOT) -> str | None:
    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        return None
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    block = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not block:
        return None
    name = re.search(r"^name:\s*(\S+)\s*$", block.group(1), re.M)
    return name.group(1) if name else None


def _validate_assertion(label: str, idx: int, a: object) -> list[str]:
    where = f"{label} assertion[{idx}]"
    if not isinstance(a, dict):
        return [f"{where}: not an object"]
    errors: list[str] = []
    text, atype = a.get("text"), a.get("type")
    if not isinstance(text, str) or not text.strip():
        errors.append(f"{where}: text must be a non-empty string")
    if atype not in DETERMINISTIC | MODEL_GRADED:
        errors.append(f"{where}: unknown type {atype!r}")
        return errors
    allowed = {"text", "type"}
    if atype == "exact_match":
        allowed.add("expected")
        if a.get("expected") not in VERDICTS:
            errors.append(f"{where}: exact_match needs 'expected' in {list(VERDICTS)}, got {a.get('expected')!r}")
    elif atype == "verdict_check":
        allowed.add("expected")
        exp = a.get("expected")
        if not isinstance(exp, list) or not exp:
            errors.append(f"{where}: verdict_check needs non-empty list 'expected'")
        else:
            bad = [v for v in exp if v not in VERDICTS]
            if bad:
                errors.append(f"{where}: verdict_check 'expected' has unknown verdicts {bad}")
            if len(set(map(str, exp))) != len(exp):
                errors.append(f"{where}: verdict_check 'expected' has duplicates")
    elif atype == "contains_string":
        allowed.add("value")
        if not isinstance(a.get("value"), str) or not a["value"]:
            errors.append(f"{where}: contains_string needs non-empty string 'value'")
    elif atype == "file_exists":
        allowed.add("glob")
        if not isinstance(a.get("glob"), str) or not a["glob"]:
            errors.append(f"{where}: file_exists needs non-empty string 'glob'")
    elif atype == "line_count_max":
        allowed.add("max")
        mx = a.get("max")
        if not isinstance(mx, int) or isinstance(mx, bool) or mx <= 0:
            errors.append(f"{where}: line_count_max needs integer 'max' > 0")
    extra = sorted(set(a) - allowed)
    if extra:
        errors.append(f"{where}: unexpected keys {extra} for type {atype}")
    return errors


def validate(data: dict, workflows: set[str], root: Path = SKILL_ROOT) -> list[str]:
    """Return error strings; an empty list means the data is valid."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    expected_name = skill_frontmatter_name(root)
    if expected_name is not None and data.get("skill_name") != expected_name:
        errors.append(f"skill_name {data.get('skill_name')!r} != SKILL.md name {expected_name!r}")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals must be a non-empty list")
        return errors
    seen_ids: set[int] = set()
    per_workflow: dict[str, int] = {}
    for pos, ev in enumerate(evals):
        if not isinstance(ev, dict):
            errors.append(f"evals[{pos}]: not an object")
            continue
        eid = ev.get("id")
        label = f"eval {eid}" if isinstance(eid, int) and not isinstance(eid, bool) else f"eval at position {pos}"
        if not isinstance(eid, int) or isinstance(eid, bool):
            errors.append(f"{label}: id must be an integer")
        elif eid in seen_ids:
            errors.append(f"{label}: duplicate id")
        else:
            seen_ids.add(eid)
        for key in ("prompt", "expected_output"):
            if not isinstance(ev.get(key), str) or not ev[key].strip():
                errors.append(f"{label}: {key} must be a non-empty string")
        files = ev.get("files")
        if not isinstance(files, list):
            errors.append(f"{label}: files must be a list")
        else:
            for f in files:
                if not isinstance(f, str) or not (root / f).exists():
                    errors.append(f"{label}: file {f!r} does not exist under the skill root")
        wf = ev.get("workflow")
        if wf not in workflows:
            errors.append(f"{label}: workflow {wf!r} is not one of {sorted(workflows)}")
        else:
            per_workflow[wf] = per_workflow.get(wf, 0) + 1
        asserts = ev.get("assertions")
        if not isinstance(asserts, list) or not asserts:
            errors.append(f"{label}: assertions must be a non-empty list")
        else:
            for i, a in enumerate(asserts):
                errors.extend(_validate_assertion(label, i, a))
    for wf in sorted(workflows):
        n = per_workflow.get(wf, 0)
        if n < MIN_CASES_PER_WORKFLOW:
            errors.append(f"workflow {wf}: {n} eval(s), need at least {MIN_CASES_PER_WORKFLOW}")
    return errors


def count_assertions(data: dict) -> tuple[int, int, int]:
    total = det = 0
    for ev in data.get("evals", []):
        for a in ev.get("assertions", []):
            total += 1
            if a.get("type") in DETERMINISTIC:
                det += 1
    return total, det, total - det


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.evals) if args.evals else EVALS_PATH
    try:
        data = load_evals(path)
    except (OSError, ValueError) as exc:
        print(f"cannot load {path}: {exc}", file=sys.stderr)
        return 1
    errors = validate(data, known_workflows())
    if errors:
        for e in errors:
            print(e)
        return 1
    total, det, concept = count_assertions(data)
    print(f"{len(data['evals'])} evals, {total} assertions ({det} deterministic, {concept} model-graded)")
    counts: dict[str, int] = {}
    for ev in data["evals"]:
        counts[ev["workflow"]] = counts.get(ev["workflow"], 0) + 1
    for wf in sorted(counts):
        print(f"{wf}: {counts[wf]}")
    return 0


# Workspace helpers

def die(message: str, code: int = 2) -> SystemExit:
    """Print message to stderr and return a SystemExit carrying the exit code."""
    print(message, file=sys.stderr)
    return SystemExit(code)


def resolve_workspace(arg: str | None, root: Path = SKILL_ROOT) -> Path:
    ws = Path(arg).expanduser().resolve() if arg else (root.parent / f"{root.name}-workspace").resolve()
    root = root.resolve()
    if ws == root or root in ws.parents:
        raise die("workspace must be outside the skill repo (ancestor CLAUDE.md would leak into runs)")
    return ws


def iteration_dirs(ws: Path) -> list[Path]:
    found = []
    if ws.is_dir():
        for p in ws.iterdir():
            m = re.fullmatch(r"iteration-(\d+)", p.name)
            if m and p.is_dir():
                found.append((int(m.group(1)), p))
    return [p for _, p in sorted(found)]


def resolve_iteration(ws: Path, name: str | None) -> Path:
    if name:
        it = ws / name
        if not it.is_dir():
            raise die(f"iteration not found: {it}")
        return it
    its = iteration_dirs(ws)
    if not its:
        raise die(f"no iterations under {ws}; run 'prepare' first")
    return its[-1]


def parse_csv(value: str | None) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()] if value else []


def select_evals(evals: list[dict], ids: str | None, workflows: str | None) -> list[dict]:
    chosen = list(evals)
    if ids:
        try:
            wanted = {int(i) for i in parse_csv(ids)}
        except ValueError:
            raise die(f"--ids must be comma-separated integers, got {ids!r}")
        missing = wanted - {e["id"] for e in evals}
        if missing:
            raise die(f"unknown eval ids: {sorted(missing)}")
        chosen = [e for e in chosen if e["id"] in wanted]
    if workflows:
        wf = set(parse_csv(workflows))
        unknown = wf - {e["workflow"] for e in evals}
        if unknown:
            raise die(f"unknown workflows: {sorted(unknown)}")
        chosen = [e for e in chosen if e["workflow"] in wf]
    return sorted(chosen, key=lambda e: e["id"])


def iteration_evals(it: Path, ids: str | None = None, workflows: str | None = None) -> list[dict]:
    """eval_metadata.json records of an iteration, filtered and sorted by id."""
    metas = []
    for p in it.glob("eval-*/eval_metadata.json"):
        metas.append(json.loads(p.read_text(encoding="utf-8")))
    metas = [{**m, "id": m["eval_id"]} for m in metas]
    return select_evals(metas, ids, workflows)


def run_dir_of(it: Path, eval_id: int) -> Path:
    return it / f"eval-{eval_id}" / RUN_SUBDIR


def write_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def git_out(root: Path, *args: str) -> str | None:
    try:
        res = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True,
                             encoding="utf-8", check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    return res.stdout


# prepare

def snapshot_files(root: Path = SKILL_ROOT) -> list[str]:
    """Repo-relative POSIX paths that belong in the skill snapshot."""
    listing = git_out(root, "ls-files")
    if listing is None:
        raise die(f"git ls-files failed in {root}; the snapshot needs a git checkout")
    picked = [f for f in listing.splitlines()
              if f == "SKILL.md" or f.startswith(SNAPSHOT_DIRS)]
    skill_md = root / "SKILL.md"
    if skill_md.is_file():
        refs = SNAPSHOT_REF_RE.findall(skill_md.read_text(encoding="utf-8", errors="replace"))
        for name in refs:
            rel = f".projex/{name}"
            if (root / rel).is_file():
                picked.append(rel)
    return sorted(set(picked))


def build_snapshot(dest: Path, root: Path = SKILL_ROOT) -> list[str]:
    copied = []
    for rel in snapshot_files(root):
        src = root / rel
        if not src.is_file():
            continue  # tracked but deleted in the working tree
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        copied.append(rel)
    return copied


def cmd_prepare(args: argparse.Namespace) -> int:
    path = Path(args.evals) if args.evals else EVALS_PATH
    data = load_evals(path)
    errors = validate(data, known_workflows())
    if errors:
        print("evals.json is invalid; run 'validate':", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    ws = resolve_workspace(args.workspace)
    chosen = select_evals(data["evals"], args.ids, args.workflow)
    if not chosen:
        print("no evals selected", file=sys.stderr)
        return 2
    ws.mkdir(parents=True, exist_ok=True)
    existing = iteration_dirs(ws)
    n = 1 + max((int(p.name.split("-")[1]) for p in existing), default=0)
    it = ws / f"iteration-{n}"
    snap = it / "skill-snapshot"
    snap.mkdir(parents=True)
    copied = build_snapshot(snap)
    dirty = git_out(SKILL_ROOT, "status", "--porcelain")
    head = git_out(SKILL_ROOT, "rev-parse", "HEAD")
    write_json(it / "iteration_meta.json", {
        "skill_root": str(SKILL_ROOT),
        "git_head": head.strip() if head else None,
        "git_dirty": bool(dirty.strip()) if dirty is not None else None,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "eval_ids": [e["id"] for e in chosen],
        "snapshot_files": copied,
    })
    for ev in chosen:
        eid = ev["id"]
        run_dir = run_dir_of(it, eid)
        outputs = run_dir / "outputs"
        outputs.mkdir(parents=True)
        for rel in ev.get("files", []):
            dst = outputs / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            src = SKILL_ROOT / rel
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        write_json(it / f"eval-{eid}" / "eval_metadata.json", {
            "eval_id": eid,
            "eval_name": f"eval-{eid}-{ev['workflow']}",
            "workflow": ev["workflow"],
            "prompt": ev["prompt"],
            "expected_output": ev["expected_output"],
            "assertions": ev["assertions"],
        })
        (it / f"eval-{eid}" / "task_prompt.md").write_text(
            TASK_PROMPT_TEMPLATE.format(snapshot=snap, outputs=outputs, prompt=ev["prompt"]),
            encoding="utf-8")
    print(f"prepared {len(chosen)} eval(s) in {it}")
    print(f"snapshot: {len(copied)} files in {snap}")
    print("next:")
    print(f"  run (needs claude auth):  python3 evals/run_evals.py run --workspace {ws} --iteration {it.name}")
    print("  agent-driven: execute each eval-<id>/task_prompt.md in a fresh subagent with cwd")
    print("    eval-<id>/with_skill/run-1/outputs/ and save its final message to eval-<id>/with_skill/run-1/response.md")
    print(f"  then: python3 evals/run_evals.py grade --workspace {ws} --iteration {it.name}")
    return 0


# run

def default_allowed_tools(snapshot: Path) -> list[str]:
    s = snapshot.as_posix()
    return [
        "Read", "Write", "Edit", "Glob", "Grep", "WebFetch", "WebSearch",
        f"Bash(pwsh -File {s}/scripts/:*)", f"Bash(powershell -File {s}/scripts/:*)",
        f"Bash(python3 {s}/scripts/:*)",
        "Bash(npm view:*)", "Bash(cosign verify:*)", "Bash(crane manifest:*)", "Bash(skopeo inspect:*)",
    ]


def build_exec_cmd(task_prompt: str, snapshot: Path, model: str | None,
                   budget: float | None, extra: list[str]) -> list[str]:
    """argv for one headless audit.

    Permission mode dontAsk denies every tool not on the allowlist instead of
    waiting for a prompt that headless mode cannot answer. Eval prompts carry
    hostile install commands, so the allowlist excludes bare Bash and any
    unrestricted shell prefix; bypassPermissions is never used.
    """
    cmd = ["claude", "-p", task_prompt, "--output-format", "stream-json", "--verbose",
           "--permission-mode", "dontAsk", "--no-session-persistence",
           "--add-dir", str(snapshot),
           "--allowedTools", *default_allowed_tools(snapshot), *extra]
    if model:
        cmd += ["--model", model]
    if budget is not None:
        cmd += ["--max-budget-usd", str(budget)]
    return cmd


def parse_transcript(stdout: str, snapshot_skill_md: Path) -> dict:
    """Tolerant stream-json parser: skips malformed lines and missing fields."""
    texts: list[str] = []
    result_text = None
    cost = None
    usage = None
    skill_read = False
    try:
        want = snapshot_skill_md.resolve()
    except OSError:
        want = snapshot_skill_md
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if not isinstance(ev, dict):
            continue
        kind = ev.get("type")
        if kind == "assistant":
            msg = ev.get("message")
            content = msg.get("content") if isinstance(msg, dict) else None
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and isinstance(block.get("text"), str):
                    texts.append(block["text"])
                elif block.get("type") == "tool_use" and block.get("name") == "Read":
                    inp = block.get("input")
                    fp = inp.get("file_path") if isinstance(inp, dict) else None
                    if isinstance(fp, str):
                        try:
                            if Path(fp).resolve() == want:
                                skill_read = True
                        except OSError:
                            pass
        elif kind == "result":
            if isinstance(ev.get("result"), str):
                result_text = ev["result"]
            if isinstance(ev.get("total_cost_usd"), (int, float)):
                cost = ev["total_cost_usd"]
            if isinstance(ev.get("usage"), dict):
                usage = ev["usage"]
    tokens = None
    if usage:
        parts = [usage.get(k) for k in ("input_tokens", "output_tokens")]
        nums = [p for p in parts if isinstance(p, (int, float))]
        tokens = int(sum(nums)) if nums else None
    return {"assistant_text": "\n\n".join(texts), "result": result_text, "cost": cost,
            "tokens": tokens, "skill_md_read": skill_read}


def _as_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def execute_one(it: Path, ev: dict, args: argparse.Namespace, extra: list[str]) -> dict:
    eid = ev["eval_id"]
    run_dir = run_dir_of(it, eid)
    outputs = run_dir / "outputs"
    snapshot = it / "skill-snapshot"
    task_prompt = (it / f"eval-{eid}" / "task_prompt.md").read_text(encoding="utf-8")
    cmd = build_exec_cmd(task_prompt, snapshot, args.model, args.max_budget_usd, extra)
    start = time.monotonic()
    timed_out = False
    try:
        proc = subprocess.run(cmd, cwd=outputs, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=args.timeout)
        stdout, stderr, code = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        stdout, stderr, code = _as_text(exc.stdout), _as_text(exc.stderr), None
    except OSError as exc:
        stdout, stderr, code = "", f"could not start claude: {exc}", None
    duration = round(time.monotonic() - start, 3)
    (run_dir / "transcript.jsonl").write_text(stdout or "", encoding="utf-8")
    parsed = parse_transcript(stdout or "", snapshot / "SKILL.md")
    (run_dir / "assistant_text.md").write_text(parsed["assistant_text"], encoding="utf-8")
    if parsed["result"] is not None:
        (run_dir / "response.md").write_text(parsed["result"], encoding="utf-8")
    write_json(run_dir / "timing.json", {"total_duration_seconds": duration, "total_tokens": parsed["tokens"]})
    write_json(run_dir / "run_meta.json", {
        "executor": "claude-cli",
        "argv_without_prompt": cmd[:2] + cmd[3:],
        "exit_code": code,
        "timed_out": timed_out,
        "duration_seconds": duration,
        "total_cost_usd": parsed["cost"],
        "snapshot_skill_md_read": parsed["skill_md_read"],
        "stderr_tail": (stderr or "")[-2000:],
    })
    return {"ok": parsed["result"] is not None, "exit_code": code, "stderr": stderr or ""}


def cmd_run(args: argparse.Namespace) -> int:
    ws = resolve_workspace(args.workspace)
    it = resolve_iteration(ws, args.iteration)
    evals = iteration_evals(it, args.ids, args.workflow)
    if not evals:
        print("no evals selected", file=sys.stderr)
        return 2
    extra = list(args.allow_tool or [])
    if args.dry_run:
        snapshot = it / "skill-snapshot"
        for ev in evals:
            cmd = build_exec_cmd("<task_prompt.md>", snapshot, args.model, args.max_budget_usd, extra)
            print(f"# eval-{ev['eval_id']} (cwd {run_dir_of(it, ev['eval_id']) / 'outputs'})")
            print(shlex.join(cmd))
        return 0
    if shutil.which("claude") is None:
        print("claude CLI not found on PATH; install it, or execute the task_prompt.md files with an agent", file=sys.stderr)
        return 2
    executed = 0
    failures = 0
    for ev in evals:
        eid = ev["eval_id"]
        run_dir = run_dir_of(it, eid)
        if (run_dir / "response.md").is_file() and not args.force:
            print(f"eval-{eid}: skipped (response.md exists; use --force)")
            continue
        first = executed == 0
        executed += 1
        print(f"eval-{eid}: running ...", flush=True)
        res = execute_one(it, ev, args, extra)
        if res["ok"]:
            print(f"eval-{eid}: done")
            continue
        failures += 1
        tail = res["stderr"][-500:].strip()
        if first and not args.keep_going:
            print(f"claude -p failed on eval {eid} (exit {res['exit_code']}). "
                  "Likely not authenticated: set ANTHROPIC_API_KEY or run 'claude' login. "
                  f"stderr tail: {tail}", file=sys.stderr)
            return 2
        print(f"eval-{eid}: failed (exit {res['exit_code']}); stderr tail: {tail}", file=sys.stderr)
    return 1 if failures else 0


# grade

def collect(run_dir: Path) -> dict:
    out = run_dir / "outputs"
    reports = sorted(out.rglob("audit-*.md")) if out.is_dir() else []

    def read(p: Path) -> str:
        return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""

    report_texts = [read(p) for p in reports]
    response = read(run_dir / "response.md")
    assistant = read(run_dir / "assistant_text.md")
    verdicts = [v for t in report_texts for v in VERDICT_RE.findall(t)] or VERDICT_RE.findall(response)
    route = ROUTE_RE.search("\n".join(report_texts + [assistant, response]))
    return {"outputs": out, "reports": reports, "report_texts": report_texts, "response": response,
            "haystack": "\n".join(report_texts + [response, assistant]),
            "verdicts": verdicts, "routed_to": route.group(1) if route else None}


def grade_deterministic(a: dict, c: dict) -> tuple[bool, str]:
    """Verdicts come from report files first, response.md only when no report
    carries one. Every verdict found must satisfy the assertion, so a run with
    several reports cannot hide a bad verdict behind a good one."""
    t, v = a["type"], c["verdicts"]
    if t == "exact_match":
        return (bool(v) and set(v) == {a["expected"]}, f"verdicts found: {v or 'none'}")
    if t == "verdict_check":
        return (bool(v) and set(v) <= set(a["expected"]), f"verdicts found: {v or 'none'}; allowed {a['expected']}")
    if t == "contains_string":
        ok = a["value"] in c["haystack"]
        return ok, f"{'found' if ok else 'not found'}: {a['value']!r}"
    if t == "file_exists":
        hits = (sorted(p.relative_to(c["outputs"]).as_posix() for p in c["outputs"].rglob(a["glob"]))
                if c["outputs"].is_dir() else [])
        return bool(hits), f"matches for {a['glob']!r}: {hits or 'none'}"
    if t == "line_count_max":
        if not c["reports"]:
            return False, "no audit-*.md report"
        counts = {p.name: len(txt.splitlines()) for p, txt in zip(c["reports"], c["report_texts"])}
        return all(n <= a["max"] for n in counts.values()), f"line counts {counts}; max {a['max']}"
    raise ValueError(t)


def load_model_grading(run_dir: Path) -> dict | None:
    p = run_dir / "model_grading.json"
    if not p.is_file():
        return None
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"warning: {p} is not valid JSON ({exc}); ignoring", file=sys.stderr)
        return None
    return obj if isinstance(obj, dict) else None


def merge_model_grading(pending: list[dict], mg: dict | None, label: str) -> tuple[list[dict], list[dict]]:
    """Split pending concept assertions into (graded, still pending).

    An entry applies only when both index and text match the current
    assertion, so grading made against reworded assertions is not reused."""
    if not mg or not isinstance(mg.get("expectations"), list):
        return [], pending
    by_index = {e.get("index"): e for e in mg["expectations"] if isinstance(e, dict)}
    graded, left = [], []
    for item in pending:
        entry = by_index.get(item["index"])
        if entry is None:
            left.append(item)
            continue
        if entry.get("text") != item["text"]:
            print(f"warning: {label} assertion {item['index']}: assertion text changed since model grading",
                  file=sys.stderr)
            left.append(item)
            continue
        graded.append({
            "index": item["index"], "text": item["text"], "type": item["type"],
            "grader": entry.get("grader") or mg.get("grader") or "model",
            "passed": bool(entry.get("passed")), "evidence": str(entry.get("evidence", "")),
        })
    return graded, left


def build_grader_prompt(meta: dict, pending: list[dict], c: dict) -> str:
    parts = [MODEL_GRADER_INSTRUCTIONS, "## Expected output\n\n" + meta["expected_output"], "## Assertions to grade\n"]
    parts += [f"{item['index']}. {item['text']}" for item in pending]
    parts.append("\n## Outputs\n")
    for p, txt in zip(c["reports"], c["report_texts"]):
        rel = p.relative_to(c["outputs"]).as_posix()
        parts.append(f"### Report file: {rel}\n\n````markdown\n{txt}\n````\n")
    parts.append(f"### Final response\n\n````markdown\n{c['response']}\n````\n")
    return "\n".join(parts)


def run_claude_grader(prompt: str, pending: list[dict], run_dir: Path, model: str | None) -> list[dict] | None:
    """Ask `claude -p` to grade; returns validated expectation dicts or None."""
    if shutil.which("claude") is None:
        print("model grader: claude CLI not found on PATH", file=sys.stderr)
        return None
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--permission-mode", "dontAsk",
           "--no-session-persistence"]
    if model:
        cmd += ["--model", model]
    try:
        proc = subprocess.run(cmd, cwd=run_dir, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=600)
        envelope = json.loads(proc.stdout)
        text = envelope["result"]
        obj = json.loads(text[text.find("{"): text.rfind("}") + 1])
        expectations = obj["expectations"]
        valid = {p["index"]: p for p in pending}
        out = []
        for e in expectations:
            if e["index"] in valid and isinstance(e["passed"], bool):
                out.append({"index": e["index"], "text": valid[e["index"]]["text"],
                            "passed": e["passed"], "evidence": str(e.get("evidence", ""))})
        if not out:
            raise ValueError("no usable expectations")
        return out
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as exc:
        print(f"model grader failed ({type(exc).__name__}: {exc}); assertions stay pending", file=sys.stderr)
        return None


def grade_run(run_dir: Path, meta: dict, model_grader: str = "none", model: str | None = None) -> dict:
    c = collect(run_dir)
    label = f"eval-{meta['eval_id']}"
    expectations: list[dict] = []
    pending: list[dict] = []
    for idx, a in enumerate(meta["assertions"]):
        if a["type"] in DETERMINISTIC:
            ok, evidence = grade_deterministic(a, c)
            expectations.append({"index": idx, "text": a["text"], "type": a["type"],
                                 "grader": "deterministic", "passed": ok, "evidence": evidence})
        else:
            pending.append({"index": idx, "text": a["text"], "type": a["type"]})
    graded, pending = merge_model_grading(pending, load_model_grading(run_dir), label)
    if pending:
        prompt = build_grader_prompt(meta, pending, c)
        (run_dir / "model_grader_prompt.md").write_text(prompt, encoding="utf-8")
        if model_grader == "claude-cli":
            got = run_claude_grader(prompt, pending, run_dir, model)
            if got:
                write_json(run_dir / "model_grading.json", {"grader": "claude-cli", "expectations": got})
                more, pending = merge_model_grading(pending, load_model_grading(run_dir), label)
                graded += more
    expectations += graded
    expectations.sort(key=lambda e: e["index"])
    passed = sum(1 for e in expectations if e["passed"])
    total = len(expectations)
    meta_path = run_dir / "run_meta.json"
    read_flag = None
    if meta_path.is_file():
        try:
            read_flag = json.loads(meta_path.read_text(encoding="utf-8")).get("snapshot_skill_md_read")
        except ValueError:
            read_flag = None
    routed = c["routed_to"]
    result = {
        "eval_id": meta["eval_id"], "workflow": meta["workflow"],
        "expectations": expectations, "pending": pending,
        "diagnostics": {
            "verdicts": c["verdicts"],
            "report_files": [p.relative_to(c["outputs"]).as_posix() for p in c["reports"]],
            "routed_to": routed,
            "routing_match": (routed == meta["workflow"]) if routed is not None else None,
            "snapshot_skill_md_read": read_flag,
        },
        "summary": {"passed": passed, "failed": total - passed, "total": total, "pending": len(pending),
                    "pass_rate": round(passed / total, 4) if total else 0.0},
    }
    write_json(run_dir / "grading.json", result)
    return result


def cmd_grade(args: argparse.Namespace) -> int:
    ws = resolve_workspace(args.workspace)
    it = resolve_iteration(ws, args.iteration)
    evals = iteration_evals(it, args.ids, args.workflow)
    graded = skipped = 0
    for meta in evals:
        run_dir = run_dir_of(it, meta["eval_id"])
        if not (run_dir / "response.md").is_file():
            print(f"eval-{meta['eval_id']}: not run (no response.md); skipped")
            skipped += 1
            continue
        res = grade_run(run_dir, meta, args.model_grader, args.model)
        s = res["summary"]
        print(f"eval-{meta['eval_id']}: {s['passed']}/{s['total']} graded passed, {s['pending']} pending")
        graded += 1
    print(f"graded {graded}, skipped {skipped}")
    return 0


# summary

def build_summary(it: Path, evals: list[dict]) -> tuple[dict, bool]:
    rows, failing, missing = [], [], []
    by_wf: dict[str, dict] = {}
    for meta in evals:
        eid, wf = meta["eval_id"], meta["workflow"]
        gp = run_dir_of(it, eid) / "grading.json"
        if not gp.is_file():
            missing.append(eid)
            continue
        g = json.loads(gp.read_text(encoding="utf-8"))
        det = [e for e in g["expectations"] if e.get("grader") == "deterministic"]
        mod = [e for e in g["expectations"] if e.get("grader") != "deterministic"]
        row = {
            "eval_id": eid, "workflow": wf, "verdicts": g["diagnostics"].get("verdicts", []),
            "deterministic": {"passed": sum(e["passed"] for e in det), "total": len(det)},
            "model": {"passed": sum(e["passed"] for e in mod), "total": len(mod)},
            "pending": len(g["pending"]),
            "routing_match": g["diagnostics"].get("routing_match"),
        }
        rows.append(row)
        agg = by_wf.setdefault(wf, {"evals": 0, "passed": 0, "total": 0, "pending": 0})
        agg["evals"] += 1
        agg["passed"] += g["summary"]["passed"]
        agg["total"] += g["summary"]["total"]
        agg["pending"] += g["summary"]["pending"]
        for e in g["expectations"]:
            if not e["passed"]:
                failing.append({"eval_id": eid, "index": e["index"], "text": e["text"], "evidence": e["evidence"]})
    data = {"iteration": it.name, "evals": rows, "by_workflow": by_wf,
            "failing": failing, "missing": missing}
    return data, bool(failing or missing)


def render_summary(data: dict) -> str:
    def routing(v: object) -> str:
        return "n/a" if v is None else ("match" if v else "MISMATCH")

    lines = [f"# Eval summary: {data['iteration']}", "",
             "| id | workflow | verdicts | deterministic | model | pending | routing |",
             "|---|---|---|---|---|---|---|"]
    for r in data["evals"]:
        lines.append(f"| {r['eval_id']} | {r['workflow']} | {', '.join(r['verdicts']) or 'none'} "
                     f"| {r['deterministic']['passed']}/{r['deterministic']['total']} "
                     f"| {r['model']['passed']}/{r['model']['total']} | {r['pending']} | {routing(r['routing_match'])} |")
    lines += ["", "## By workflow", "", "| workflow | evals | graded passed | graded total | pending |", "|---|---|---|---|---|"]
    for wf in sorted(data["by_workflow"]):
        a = data["by_workflow"][wf]
        lines.append(f"| {wf} | {a['evals']} | {a['passed']} | {a['total']} | {a['pending']} |")
    if data["missing"]:
        lines += ["", "## Missing grading", "", "Selected evals with no grading.json: " + ", ".join(map(str, data["missing"]))]
    if data["failing"]:
        lines += ["", "## Failing assertions", ""]
        for f in data["failing"]:
            lines.append(f"- eval {f['eval_id']} assertion {f['index']}: {f['text']} — {f['evidence']}")
    return "\n".join(lines) + "\n"


def cmd_summary(args: argparse.Namespace) -> int:
    ws = resolve_workspace(args.workspace)
    it = resolve_iteration(ws, args.iteration)
    evals = iteration_evals(it, args.ids, args.workflow)
    data, failed = build_summary(it, evals)
    md = render_summary(data)
    (it / "summary.md").write_text(md, encoding="utf-8")
    write_json(it / "summary.json", data)
    print(md)
    return 1 if failed else 0


# CLI

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="run_evals.py", description="Eval runner for the install-auditor skill")
    sub = p.add_subparsers(dest="command", required=True)

    def common(sp: argparse.ArgumentParser, iteration: bool = True) -> None:
        sp.add_argument("--workspace", help="workspace dir outside the skill repo (default: <repo>-workspace beside the repo)")
        if iteration:
            sp.add_argument("--iteration", help="iteration dir name (default: latest)")
        sp.add_argument("--ids", help="comma-separated eval ids")
        sp.add_argument("--workflow", help="comma-separated workflow names")

    v = sub.add_parser("validate", help="check evals.json schema and invariants")
    v.add_argument("--evals", help="path to an evals.json (default: the repo file)")
    v.set_defaults(func=cmd_validate)

    pr = sub.add_parser("prepare", help="snapshot the skill and write task prompts")
    common(pr, iteration=False)
    pr.add_argument("--evals", help="path to an evals.json (default: the repo file)")
    pr.set_defaults(func=cmd_prepare)

    r = sub.add_parser("run", help="execute prepared evals through claude -p")
    common(r)
    r.add_argument("--model")
    r.add_argument("--max-budget-usd", type=float)
    r.add_argument("--timeout", type=int, default=900, help="seconds per eval (default 900)")
    r.add_argument("--allow-tool", action="append", metavar="RULE", help="extra --allowedTools rule (operator responsibility)")
    r.add_argument("--dry-run", action="store_true", help="print the commands only")
    r.add_argument("--keep-going", action="store_true", help="continue after the first eval fails")
    r.add_argument("--force", action="store_true", help="re-run evals that already have response.md")
    r.set_defaults(func=cmd_run)

    g = sub.add_parser("grade", help="grade saved outputs")
    common(g)
    g.add_argument("--model-grader", choices=["none", "claude-cli"], default="none")
    g.add_argument("--model", help="model for --model-grader claude-cli")
    g.set_defaults(func=cmd_grade)

    s = sub.add_parser("summary", help="aggregate grading into summary.md / summary.json")
    common(s)
    s.set_defaults(func=cmd_summary)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
