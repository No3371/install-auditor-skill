"""Offline regression tests for the lookup scripts in scripts/ and their .ps1 twins.

No network. Python tests replace each module's HTTP helpers. PowerShell tests run when
`pwsh` is on PATH: they copy the .ps1 into a temp dir (so caches land there, not in
scripts/) and run it behind global Invoke-RestMethod / Invoke-WebRequest functions,
which take precedence over the cmdlets of the same name.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True  # importing the scripts must not leave scripts/__pycache__ behind

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PWSH = shutil.which("pwsh")


def load(stem):
    spec = importlib.util.spec_from_file_location(stem.replace("-", "_"), SCRIPTS / (stem + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mod.main(argv)
    return json.loads(buf.getvalue())


PS_MOCK = r"""
$ErrorActionPreference = 'Stop'
$global:MockRoutes = @(Get-Content -Raw -Path $env:MOCK_ROUTES | ConvertFrom-Json)
function global:Invoke-RestMethod {
    param($Uri, $Method, $ContentType, $Body, $Headers, $TimeoutSec)
    foreach ($r in $global:MockRoutes) {
        if ("$Uri".Contains($r.match)) {
            if ($r.fail) { throw "mock: $Uri unreachable" }
            return $r.body
        }
    }
    throw "mock: no route for $Uri"
}
function global:Invoke-WebRequest {
    param($Uri, $Method, $Headers, $TimeoutSec, [switch]$UseBasicParsing)
    foreach ($r in $global:MockRoutes) {
        if ("$Uri".Contains($r.match)) {
            if ($r.status -eq 404) {
                $msg = [System.Net.Http.HttpResponseMessage]::new([System.Net.HttpStatusCode]::NotFound)
                throw [Microsoft.PowerShell.Commands.HttpResponseException]::new('404 (Not Found)', $msg)
            }
            if ($r.fail) { throw "mock: $Uri unreachable" }
            return [pscustomobject]@{ StatusCode = 200 }
        }
    }
    throw "mock: no route for $Uri"
}
$params = Get-Content -Raw -Path $env:MOCK_PARAMS | ConvertFrom-Json -AsHashtable
& $env:MOCK_SCRIPT @params
"""


def run_ps(stem, params, routes, baseline_tsv=None):
    """Run scripts/<stem>.ps1 offline. routes: [{match, body?, fail?, status?}], first match wins."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        script = tmp / (stem + ".ps1")
        shutil.copy2(SCRIPTS / (stem + ".ps1"), script)
        if baseline_tsv is not None:
            (tmp / "data").mkdir()
            (tmp / "data" / "npm-popular.tsv").write_text(baseline_tsv, encoding="utf-8")
        (tmp / "routes.json").write_text(json.dumps(routes), encoding="utf-8")
        (tmp / "params.json").write_text(json.dumps(params), encoding="utf-8")
        (tmp / "mock.ps1").write_text(PS_MOCK, encoding="utf-8")
        env = dict(os.environ, MOCK_ROUTES=str(tmp / "routes.json"),
                   MOCK_PARAMS=str(tmp / "params.json"), MOCK_SCRIPT=str(script))
        proc = subprocess.run([PWSH, "-NoProfile", "-NonInteractive", "-File", str(tmp / "mock.ps1")],
                              capture_output=True, text=True, env=env, timeout=180)
        if not proc.stdout.strip().startswith("{"):
            raise AssertionError("pwsh produced no JSON:\n" + proc.stderr + proc.stdout)
        return json.loads(proc.stdout)


# ── Fixtures ────────────────────────────────────────────────────────────────

OSV_ALL_VERSIONS = {"vulns": [{
    "id": "GHSA-test-0001", "aliases": ["CVE-2099-0001"], "summary": "fixture vuln",
    "database_specific": {"severity": "HIGH"},
    "affected": [{"package": {"name": "fixpkg"},
                  "ranges": [{"type": "SEMVER", "events": [{"introduced": "0"}]}]}],
}]}

NPM_ONE_MAINTAINER = {
    "name": "fixpkg", "description": "fixture", "dist-tags": {"latest": "1.0.0"},
    "maintainers": [{"name": "solo"}],
    "versions": {"1.0.0": {"license": "MIT", "scripts": {"postinstall": "node x.js"}}},
    "time": {"created": "2020-01-01T00:00:00Z", "modified": "2020-01-01T00:00:00Z",
             "1.0.0": "2020-01-01T00:00:00Z"},
}

PYPI_ONE_AUTHOR = {
    "info": {"name": "fixpkg", "version": "1.0.0", "summary": "fixture", "license": "MIT",
             "author": "solo", "maintainer": None, "requires_dist": None, "project_urls": None,
             "classifiers": []},
    "urls": [], "releases": {"1.0.0": []},
}

NPM_IDENTITY_DRIFT = {
    "name": "fixpkg", "description": "fixture", "dist-tags": {"latest": "1.1.0"},
    "maintainers": [{"name": "solo"}],
    "versions": {
        "1.0.0": {"license": "MIT",
                  "_npmUser": {"name": "GitHub Actions",
                               "trustedPublisher": {"id": "github", "oidcConfigId": "cfg-1"}},
                  "dist": {"attestations": {"url": "https://registry.npmjs.org/-/npm/v1/attestations/fixpkg@1.0.0",
                                            "provenance": {"predicateType": "https://slsa.dev/provenance/v1"}}}},
        "1.1.0-beta.1": {"license": "MIT", "_npmUser": {"name": "canary-bot"}},
        "1.1.0": {"license": "MIT", "_npmUser": {"name": "solo"}, "scripts": {"preinstall": "node setup.js"}},
    },
    # 1.0.1 is in `time` but no longer served: removed, like a pulled malicious release.
    "time": {"created": "2020-01-01T00:00:00Z", "modified": "2020-03-01T00:00:00Z",
             "1.0.0": "2020-01-01T00:00:00Z", "1.0.1": "2020-01-15T00:00:00Z",
             "1.1.0-beta.1": "2020-02-01T00:00:00Z", "1.1.0": "2020-03-01T00:00:00Z"},
}
DRIFT_ROUTES = [{"match": "registry.npmjs.org", "body": NPM_IDENTITY_DRIFT}, {"match": "", "fail": True}]
DRIFT_PREVIOUS = {"version": "1.0.0", "publisher": "GitHub Actions",
                  "trustedPublisher": {"id": "github", "oidcConfigId": "cfg-1"},
                  "provenance": "https://slsa.dev/provenance/v1", "installHooks": []}


def without(d, *keys):
    return {k: v for k, v in d.items() if k not in keys}


BASELINE_TSV = """# fixture baseline
chalk\t500000000
react\t180000000
react-dom\t170000000
lodash\t160000000
express\t145000000
chai\t140000000
cross-env\t26000000
"""


# ── vuln-lookup ─────────────────────────────────────────────────────────────

class VulnLookupPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("vuln-lookup")
        self.tmp = tempfile.TemporaryDirectory()
        self.mod.CACHE_DIR = self.tmp.name  # absolute: os.path.join(SCRIPT_DIR, abs) -> abs

    def tearDown(self):
        self.tmp.cleanup()

    def test_osv_range_matrix(self):
        f = self.mod.test_osv_version_affected
        semver = lambda *events: [{"type": "SEMVER", "events": list(events)}]
        self.assertTrue(f("1.0.0", semver({"introduced": "0"}), []))            # all versions affected
        self.assertTrue(f("0.0.8", semver({"introduced": "0"}, {"fixed": "0.2.1"}), []))
        self.assertFalse(f("1.2.6", semver({"introduced": "0"}, {"fixed": "0.2.1"}), []))
        self.assertTrue(f("1.5.0", semver({"introduced": "1.0.0"}), []))        # open-ended, above floor
        self.assertFalse(f("0.9.0", semver({"introduced": "1.0.0"}), []))       # open-ended, below floor
        self.assertTrue(f("2.0.0", semver({"introduced": "1.0.0"}, {"last_affected": "2.0.0"}), []))
        self.assertTrue(f("1.0.0", [], []))                                      # no data: conservative
        self.assertTrue(f("1.0.0", [], ["1.0.0"]))

    def _run(self, argv, ghsa):
        def fake_http_json(url, **kw):
            if "osv.dev" in url:
                return OSV_ALL_VERSIONS
            if isinstance(ghsa, Exception):
                raise ghsa
            return ghsa
        self.mod.http_json = fake_http_json
        return run_main(self.mod, argv)

    def test_version_filter_keeps_introduced_zero(self):
        out = self._run(["-Ecosystem", "npm", "-Name", "fixpkg", "-Version", "1.0.0"], [])
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["summary"], {"totalCount": 1, "osvCount": 1, "ghsaCount": 0, "highestSeverity": "high"})
        self.assertEqual(out["sources"], ["OSV", "GHSA"])
        self.assertNotIn("ghsaNote", out)

    def test_ghsa_failure_is_reported(self):
        out = self._run(["-Ecosystem", "npm", "-Name", "fixpkg"], OSError("blocked"))
        self.assertEqual(out["sources"], ["OSV"])
        self.assertEqual(out["ghsaResults"], [])
        self.assertIn("ghsaNote", out)


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class VulnLookupPowerShell(unittest.TestCase):
    def test_single_hit_is_an_array(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "body": []}])
        self.assertIsInstance(out["osvResults"], list)
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["summary"], {"totalCount": 1, "osvCount": 1, "ghsaCount": 0, "highestSeverity": "high"})

    def test_zero_hits_and_empty_ghsa_success(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": {}}, {"match": "api.github.com", "body": []}])
        self.assertEqual(out["osvResults"], [])
        self.assertEqual(out["ghsaResults"], [])
        self.assertEqual(out["sources"], ["OSV", "GHSA"])
        self.assertNotIn("ghsaNote", out)

    def test_version_filter_keeps_introduced_zero(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg", "Version": "1.0.0"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "body": []}])
        self.assertEqual(len(out["osvResults"]), 1)
        self.assertEqual(out["riskLevel"], "high")

    def test_ghsa_failure_is_reported(self):
        out = run_ps("vuln-lookup", {"Ecosystem": "npm", "Name": "fixpkg"},
                     [{"match": "api.osv.dev", "body": OSV_ALL_VERSIONS}, {"match": "api.github.com", "fail": True}])
        self.assertEqual(out["sources"], ["OSV"])
        self.assertEqual(out["ghsaResults"], [])
        self.assertIn("ghsaNote", out)


# ── registry-lookup ─────────────────────────────────────────────────────────

REGISTRY_ROUTES = [
    {"match": "registry.npmjs.org", "body": NPM_ONE_MAINTAINER},
    {"match": "pypi.org/pypi/", "body": PYPI_ONE_AUTHOR},
    {"match": "", "fail": True},  # downloads, pypistats, scorecard: unreachable
]
ONE_HOOK = [{"hook": "postinstall", "command": "node x.js"}]


class RegistryLookupPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("registry-lookup")

        def fake_invoke_api(url, timeout=15):
            for r in REGISTRY_ROUTES:
                if r["match"] in url:
                    return None if r.get("fail") else r["body"]
        self.mod.invoke_api = fake_invoke_api

    def test_single_entries_are_arrays(self):
        npm = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        self.assertEqual((npm["previousVersion"], npm["removedVersions"], npm["trustedPublisher"]), (None, [], None))
        pypi = run_main(self.mod, ["pypi", "fixpkg"])
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))
        self.assertNotIn("previousVersion", pypi)


class RegistryLookupNpmIdentityPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("registry-lookup")

        def fake_invoke_api(url, timeout=15):
            for r in DRIFT_ROUTES:
                if r["match"] in url:
                    return None if r.get("fail") else r["body"]
        self.mod.invoke_api = fake_invoke_api

    def test_identity_drop_and_removed_version(self):
        out = run_main(self.mod, ["npm", "fixpkg"])
        self.assertEqual((out["publisher"], out["trustedPublisher"], out["provenance"]), ("solo", None, None))
        self.assertEqual(without(out["previousVersion"], "publishedAt"), DRIFT_PREVIOUS)
        self.assertEqual(out["previousVersion"]["publishedAt"], "2020-01-01")
        self.assertEqual(out["removedVersions"], ["1.0.1"])

    def test_prerelease_compares_with_any_earlier_version(self):
        out = run_main(self.mod, ["npm", "fixpkg", "1.1.0-beta.1"])
        self.assertEqual((out["publisher"], out["previousVersion"]["version"]), ("canary-bot", "1.0.0"))


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class RegistryLookupPowerShell(unittest.TestCase):
    def test_single_entries_are_arrays(self):
        npm = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((npm["maintainers"], npm["maintainerCount"], npm["installScripts"]), (["solo"], 1, ONE_HOOK))
        self.assertEqual((npm["previousVersion"], npm["removedVersions"], npm["trustedPublisher"]), (None, [], None))
        pypi = run_ps("registry-lookup", {"Ecosystem": "pypi", "Name": "fixpkg"}, REGISTRY_ROUTES)
        self.assertEqual((pypi["maintainers"], pypi["maintainerCount"]), (["solo"], 1))

    def test_identity_drop_and_removed_version(self):
        out = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg"}, DRIFT_ROUTES)
        self.assertEqual((out["publisher"], out["trustedPublisher"], out["provenance"]), ("solo", None, None))
        self.assertEqual(without(out["previousVersion"], "publishedAt"), DRIFT_PREVIOUS)
        self.assertEqual(out["removedVersions"], ["1.0.1"])

    def test_prerelease_compares_with_any_earlier_version(self):
        out = run_ps("registry-lookup", {"Ecosystem": "npm", "Name": "fixpkg", "Version": "1.1.0-beta.1"}, DRIFT_ROUTES)
        self.assertEqual((out["publisher"], out["previousVersion"]["version"]), ("canary-bot", "1.0.0"))


# ── typosquat-check ─────────────────────────────────────────────────────────

class TyposquatPython(unittest.TestCase):
    def setUp(self):
        self.mod = load("typosquat-check")
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "npm-popular.tsv"
        path.write_text(BASELINE_TSV, encoding="utf-8")
        self.mod.BASELINE_PATH = str(path)
        self.mod.get_npm_weekly_downloads = lambda name: None
        self.exists = True
        self.mod.npm_package_exists = lambda name: self.exists

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, *args):
        return run_main(self.mod, ["-Ecosystem", "npm", "-Name"] + list(args))

    def test_typo_of_popular_package_is_high(self):
        out = self.check("expresss")
        self.assertEqual(out["riskLevel"], "high")
        self.assertEqual(out["closestMatches"][0], {"name": "express", "distance": 1, "downloads": 145000000})

    def test_separator_typo_is_high(self):
        self.assertEqual(self.check("crossenv")["closestMatches"][0]["name"], "cross-env")

    def test_known_popular_packages_are_low(self):
        for name in ("chalk", "react"):  # chalk~chai (distance 2), react prefixes react-dom
            out = self.check(name)
            self.assertEqual(out["riskLevel"], "low", name)
            self.assertEqual(out["combosquatHints"], [], name)
            self.assertTrue(out["details"].startswith("'%s' is in the bundled top-7" % name), out["details"])

    def test_scoped_name_is_not_known_popular(self):
        self.assertNotIn("is in the bundled", self.check("@evil/chalk")["details"])

    def test_size_limits_baseline(self):
        self.assertEqual(self.check("expresss", "-Size", "2")["riskLevel"], "low")

    def test_existence_notes(self):
        self.exists = False
        self.assertIn("registry returned 404", self.check("zzqqxx")["details"])
        self.exists = None
        self.assertIn("could not confirm", self.check("zzqqxx")["details"])

    def test_missing_baseline_still_checks_compare_to(self):
        self.mod.BASELINE_PATH = str(Path(self.tmp.name) / "absent.tsv")
        out = self.check("lodahs", "-CompareTo", "lodash")
        self.assertEqual(out["riskLevel"], "high")
        self.assertIn("missing or unreadable", out["details"])

    def test_legacy_cache_flags_accepted(self):
        self.assertEqual(self.check("expresss", "-NoCache", "-CacheHours", "1")["riskLevel"], "high")


class BundledBaseline(unittest.TestCase):
    def test_bundled_file_shape(self):
        rows = []
        for line in (SCRIPTS / "data" / "npm-popular.tsv").read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                name, weekly = line.split("\t")
                rows.append((name, int(weekly)))
        names = [n for n, _ in rows]
        self.assertGreaterEqual(len(rows), 1000)
        self.assertEqual(len(names), len(set(names)))
        self.assertFalse([n for n in names if n.startswith("@")])
        self.assertEqual([w for _, w in rows], sorted((w for _, w in rows), reverse=True))
        for must in ("express", "lodash", "react", "chalk", "cross-env", "prettier", "semver", "commander"):
            self.assertIn(must, names)


@unittest.skipUnless(PWSH, "pwsh not on PATH")
class TyposquatParity(unittest.TestCase):
    """The .ps1 must emit exactly what the .py emits for the same baseline, offline."""

    def test_twins_agree(self):
        py = TyposquatPython("test_typo_of_popular_package_is_high")
        py.setUp()
        try:
            for args in (["expresss"], ["chalk"], ["react"], ["lodahs", "-CompareTo", "lodash"], ["expresss", "-Size", "2"]):
                params = {"Ecosystem": "npm", "Name": args[0]}
                for flag, value in zip(args[1::2], args[2::2]):
                    params[flag.lstrip("-")] = int(value) if value.isdigit() else value
                ps = run_ps("typosquat-check", params,
                            [{"match": "api.npmjs.org", "fail": True}, {"match": "registry.npmjs.org", "status": 200}],
                            baseline_tsv=BASELINE_TSV)
                self.assertEqual(ps, py.check(*args), args)
        finally:
            py.tearDown()


if __name__ == "__main__":
    unittest.main()
