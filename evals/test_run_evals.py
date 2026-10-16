"""Offline unit tests for run_evals.py (no network, no `claude`).

Run: python3 -m unittest discover -s evals -p "test_*.py" -v
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import run_evals as R  # noqa: E402


def make_run(root: Path, reports: dict[str, str] | None = None, response: str = "",
             assistant: str = "") -> Path:
    run_dir = root / "run-1"
    outputs = run_dir / "outputs"
    outputs.mkdir(parents=True)
    for name, text in (reports or {}).items():
        (outputs / name).write_text(text, encoding="utf-8")
    (run_dir / "response.md").write_text(response, encoding="utf-8")
    if assistant:
        (run_dir / "assistant_text.md").write_text(assistant, encoding="utf-8")
    return run_dir


def report(verdict: str, lines: int = 40, coverage: bool = True) -> str:
    body = [f"# Install Audit: pkg", "", f"**Verdict: {verdict} ✅**", ""]
    if coverage:
        body.append("## Audit Coverage")
    while len(body) < lines:
        body.append(f"line {len(body)}")
    return "\n".join(body[:lines]) + "\n"


def meta(assertions: list[dict], workflow: str = "registry-package", eval_id: int = 0) -> dict:
    return {"eval_id": eval_id, "workflow": workflow, "expected_output": "expected",
            "assertions": assertions}


EVAL0_ASSERTIONS = [
    {"text": "Report identifies this as a Tier 1 / Quick audit", "type": "contains_concept"},
    {"text": "Verdict is APPROVED", "type": "exact_match", "expected": "APPROVED"},
    {"text": "Report is saved to a .md file", "type": "file_exists", "glob": "audit-*.md"},
    {"text": "Report is concise — under 80 lines", "type": "line_count_max", "max": 79},
]


class ValidateTests(unittest.TestCase):
    def test_repo_evals_valid(self):
        data = R.load_evals(R.EVALS_PATH)
        self.assertEqual(R.validate(data, R.known_workflows()), [])
        total, det, concept = R.count_assertions(data)
        self.assertEqual((len(data["evals"]), total, det, concept), (41, 248, 82, 166))

    def _synthetic(self, root: Path) -> tuple[dict, set[str]]:
        (root / "SKILL.md").write_text("---\nname: demo\n---\nbody\n", encoding="utf-8")
        evals = []
        for i in range(6):
            evals.append({
                "id": i, "workflow": "a" if i < 3 else "b", "prompt": "p", "expected_output": "e",
                "files": [],
                "assertions": [{"text": "Verdict is APPROVED", "type": "exact_match", "expected": "APPROVED"}],
            })
        return {"skill_name": "demo", "evals": evals}, {"a", "b"}

    def test_validate_rejects(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data, wfs = self._synthetic(root)
            self.assertEqual(R.validate(data, wfs, root), [])

            def mutated(fn):
                d, _ = self._synthetic(root)
                fn(d)
                return R.validate(d, wfs, root)

            cases = {
                "exact_match without expected": (
                    lambda d: d["evals"][1]["assertions"][0].pop("expected"), "eval 1"),
                "verdict_check with MAYBE": (
                    lambda d: d["evals"][2]["assertions"].append(
                        {"text": "t", "type": "verdict_check", "expected": ["MAYBE"]}), "eval 2"),
                "unknown type": (
                    lambda d: d["evals"][3]["assertions"].append({"text": "t", "type": "vibes"}), "eval 3"),
                "unknown workflow": (
                    lambda d: d["evals"][4].update(workflow="zzz"), "eval 4"),
                "duplicate id": (
                    lambda d: d["evals"][5].update(id=0), "eval 0"),
            }
            for label, (fn, needle) in cases.items():
                with self.subTest(label):
                    errors = mutated(fn)
                    self.assertTrue(any(needle in e for e in errors), errors)

            with self.subTest("workflow under minimum"):
                d, _ = self._synthetic(root)
                d["evals"].pop()
                errors = R.validate(d, wfs, root)
                self.assertTrue(any("workflow b" in e for e in errors), errors)

            with self.subTest("skill_name mismatch"):
                d, _ = self._synthetic(root)
                d["skill_name"] = "other"
                self.assertTrue(any("skill_name" in e for e in R.validate(d, wfs, root)))


class GradeTests(unittest.TestCase):
    def test_grade_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-express.md": report("APPROVED")}, "Done.")
            res = R.grade_run(run_dir, meta(EVAL0_ASSERTIONS))
            self.assertEqual([e["passed"] for e in res["expectations"]], [True, True, True])
            self.assertEqual([p["index"] for p in res["pending"]], [0])
            self.assertEqual(res["summary"], {"passed": 3, "failed": 0, "total": 3, "pending": 1, "pass_rate": 1.0})
            self.assertTrue((run_dir / "model_grader_prompt.md").is_file())
            self.assertTrue((run_dir / "grading.json").is_file())
            on_disk = json.loads((run_dir / "grading.json").read_text(encoding="utf-8"))
            for e in on_disk["expectations"]:
                self.assertTrue({"text", "passed", "evidence"} <= set(e))

    def test_grade_verdict_mismatch_and_missing(self):
        exact = {"text": "Verdict is APPROVED", "type": "exact_match", "expected": "APPROVED"}
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-x.md": report("REJECTED")})
            ok, evidence = R.grade_deterministic(exact, R.collect(run_dir))
            self.assertFalse(ok)
            self.assertIn("REJECTED", evidence)
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), None, "I could not finish.")
            ok, evidence = R.grade_deterministic(exact, R.collect(run_dir))
            self.assertFalse(ok)
            self.assertIn("none", evidence)

    def test_multi_report_verdict_check(self):
        check = {"text": "t", "type": "verdict_check", "expected": ["APPROVED", "CONDITIONAL"]}
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-a.md": report("APPROVED"), "audit-b.md": report("REJECTED")})
            ok, _ = R.grade_deterministic(check, R.collect(run_dir))
            self.assertFalse(ok)

    def test_placeholder_not_a_verdict(self):
        line = "**Verdict: [APPROVED ✅ | CONDITIONAL ⚠️ | REJECTED ❌]**"
        self.assertEqual(R.VERDICT_RE.findall(line), [])
        self.assertEqual(R.VERDICT_RE.findall("**Verdict: CONDITIONAL ⚠️**"), ["CONDITIONAL"])
        self.assertEqual(R.VERDICT_RE.findall("**Verdict:** REJECTED"), ["REJECTED"])
        self.assertEqual(R.VERDICT_RE.findall("This is not Verdict: APPROVED material"), [])

    def test_line_count_max(self):
        check = {"text": "t", "type": "line_count_max", "max": 79}
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-a.md": report("APPROVED", lines=80)})
            self.assertFalse(R.grade_deterministic(check, R.collect(run_dir))[0])
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-a.md": report("APPROVED", lines=79)})
            self.assertTrue(R.grade_deterministic(check, R.collect(run_dir))[0])

    def test_model_grading_merge(self):
        concept = EVAL0_ASSERTIONS[0]
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-express.md": report("APPROVED")}, "Done.")
            (run_dir / "model_grading.json").write_text(json.dumps({
                "grader": "agent",
                "expectations": [{"index": 0, "text": concept["text"], "passed": True, "evidence": "Tier 1"}],
            }), encoding="utf-8")
            res = R.grade_run(run_dir, meta(EVAL0_ASSERTIONS))
            self.assertEqual(res["pending"], [])
            self.assertEqual(res["summary"]["total"], 4)
            merged = [e for e in res["expectations"] if e["index"] == 0][0]
            self.assertEqual((merged["grader"], merged["passed"]), ("agent", True))
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), {"audit-express.md": report("APPROVED")}, "Done.")
            (run_dir / "model_grading.json").write_text(json.dumps({
                "grader": "agent",
                "expectations": [{"index": 0, "text": "reworded assertion", "passed": True, "evidence": "x"}],
            }), encoding="utf-8")
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                res = R.grade_run(run_dir, meta(EVAL0_ASSERTIONS))
            self.assertEqual([p["index"] for p in res["pending"]], [0])
            self.assertIn("assertion text changed", err.getvalue())

    def test_routing_diagnostic(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), None, "Routes to:      workflows/registry-package.md\n**Verdict: APPROVED**")
            self.assertEqual(R.collect(run_dir)["routed_to"], "registry-package")
            res = R.grade_run(run_dir, meta([EVAL0_ASSERTIONS[1]]))
            self.assertTrue(res["diagnostics"]["routing_match"])
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = make_run(Path(tmp), None, "**Verdict: APPROVED**")
            self.assertIsNone(R.collect(run_dir)["routed_to"])


class PrepareAndRunTests(unittest.TestCase):
    def test_prepare_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = R.main(["prepare", "--workspace", str(ws), "--ids", "0"])
            self.assertEqual(code, 0)
            it = ws / "iteration-1"
            snap = it / "skill-snapshot"
            self.assertTrue((snap / "SKILL.md").is_file())
            skill_text = (R.SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
            for name in R.SNAPSHOT_REF_RE.findall(skill_text):
                if (R.SKILL_ROOT / ".projex" / name).is_file():
                    self.assertTrue((snap / ".projex" / name).is_file(), name)
            self.assertTrue((snap / "references").is_dir())
            for absent in ("evals", "CLAUDE.md", "STEWARDSHIP.md", ".projex/closed"):
                self.assertFalse((snap / absent).exists(), absent)
            prompt = (it / "eval-0" / "task_prompt.md").read_text(encoding="utf-8")
            self.assertIn(str(snap), prompt)
            self.assertIn(R.load_evals()["evals"][0]["prompt"], prompt)
            self.assertTrue((it / "eval-0" / "with_skill" / "run-1" / "outputs").is_dir())
            self.assertEqual(json.loads((it / "eval-0" / "eval_metadata.json").read_text(encoding="utf-8"))["eval_id"], 0)
            err = io.StringIO()
            with contextlib.redirect_stderr(err), self.assertRaises(SystemExit) as cm:
                R.main(["prepare", "--workspace", str(R.SKILL_ROOT / "inside-repo")])
            self.assertEqual(cm.exception.code, 2)

    def test_dry_run_cmd(self):
        snap = Path("/ws/iteration-1/skill-snapshot")
        cmd = R.build_exec_cmd("prompt", snap, None, None, [])
        self.assertIn("dontAsk", cmd)
        self.assertNotIn("bypassPermissions", " ".join(cmd))
        allowed = cmd[cmd.index("--allowedTools") + 1:]
        self.assertNotIn("Bash", allowed)
        self.assertNotIn("Bash(pwsh:*)", allowed)
        self.assertTrue(all(a.startswith("Bash(") for a in allowed if a.startswith("Bash")))
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            with contextlib.redirect_stdout(io.StringIO()):
                R.main(["prepare", "--workspace", str(ws), "--ids", "0,13"])
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = R.main(["run", "--workspace", str(ws), "--dry-run"])
            self.assertEqual(code, 0)
            commands = [ln for ln in out.getvalue().splitlines() if ln.startswith("claude ")]
            self.assertEqual(len(commands), 2)
            for ln in commands:
                self.assertIn("--permission-mode dontAsk", ln)
                self.assertNotIn("bypassPermissions", ln)
            self.assertFalse(any((ws / "iteration-1" / f"eval-{i}" / "with_skill" / "run-1" / "response.md").exists()
                                 for i in (0, 13)))

    def test_parse_transcript_tolerant(self):
        snap_md = Path("/ws/skill-snapshot/SKILL.md")
        lines = [
            "not json",
            json.dumps({"type": "assistant", "message": {"content": [
                {"type": "text", "text": "hello"},
                {"type": "tool_use", "name": "Read", "input": {"file_path": "/ws/skill-snapshot/SKILL.md"}}]}}),
            json.dumps({"type": "assistant", "message": "odd"}),
            json.dumps({"type": "result", "result": "final", "total_cost_usd": 0.5,
                        "usage": {"input_tokens": 3, "output_tokens": 4}}),
        ]
        parsed = R.parse_transcript("\n".join(lines), snap_md)
        self.assertEqual(parsed["assistant_text"], "hello")
        self.assertEqual(parsed["result"], "final")
        self.assertEqual((parsed["cost"], parsed["tokens"]), (0.5, 7))
        self.assertTrue(parsed["skill_md_read"])
        empty = R.parse_transcript("", snap_md)
        self.assertIsNone(empty["result"])


if __name__ == "__main__":
    unittest.main()
