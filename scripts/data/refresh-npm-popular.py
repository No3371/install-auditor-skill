#!/usr/bin/env python3
"""Regenerate npm-popular.tsv, the bundled popular-package baseline of typosquat-check.

Maintainer tool: the skill never runs it, so it has no .ps1 twin. Needs registry.npmjs.org.
Candidates: npm search results for SEED_TERMS (two pages of 250 each) plus MUST_INCLUDE
(each resolved by an exact-name search). Scoped names are dropped (typosquat-check
compares unscoped basenames; generic scoped basenames such as core or cli would collide
with unrelated names). Ranked by the search API's downloads.weekly, highest first; the
top --count rows are written. The search API is used instead of
api.npmjs.org/downloads because one search page returns 250 weekly counts.

Usage: python3 scripts/data/refresh-npm-popular.py [--count 1000]
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "npm-popular.tsv")
SEARCH = "https://registry.npmjs.org/-/v1/search?size=%d&from=%d&text=%s"

SEED_TERMS = [
    "react", "vue", "angular", "svelte", "next", "webpack", "vite", "rollup", "esbuild", "babel",
    "eslint", "prettier", "typescript", "types", "jest", "mocha", "test", "lint", "cli", "util",
    "utils", "string", "array", "object", "file", "fs", "path", "stream", "color", "ansi",
    "parse", "json", "yaml", "node", "http", "request", "fetch", "server", "express", "middleware",
    "promise", "async", "date", "time", "crypto", "hash", "buffer", "url", "glob", "lodash",
    "config", "env", "debug", "log", "core", "plugin", "loader", "postcss", "css", "aws",
    "google", "graphql", "database", "sql", "redis", "auth", "jwt", "uuid", "semver", "terminal",
]

MUST_INCLUDE = [
    "express", "lodash", "react", "react-dom", "chalk", "debug", "commander", "yargs", "semver",
    "uuid", "axios", "moment", "dayjs", "date-fns", "cross-env", "dotenv", "prettier", "eslint",
    "typescript", "webpack", "vite", "rollup", "esbuild", "jest", "mocha", "chai", "sinon",
    "request", "node-fetch", "cors", "body-parser", "cookie-parser", "morgan", "helmet",
    "jsonwebtoken", "bcrypt", "bcryptjs", "mongoose", "mysql", "mysql2", "pg", "redis", "ioredis",
    "socket.io", "ws", "minimist", "mkdirp", "rimraf", "glob", "fs-extra", "async", "bluebird",
    "underscore", "colors", "classnames", "prop-types", "react-router", "react-router-dom",
    "redux", "react-redux", "vue", "next", "nuxt", "electron", "tslib", "core-js", "zod", "rxjs",
    "nodemon", "concurrently", "husky", "lint-staged", "inquirer", "ora", "nanoid", "qs", "ms",
    "ua-parser-js", "rc",
]


def search(text, size, frm=0):
    url = SEARCH % (size, frm, urllib.parse.quote(text, safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "install-auditor/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp).get("objects") or []
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    return []


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--count", type=int, default=1000)
    args = p.parse_args(argv)

    weekly = {}

    def add(objs, only=None):
        for o in objs:
            name = (o.get("package") or {}).get("name")
            if not name or name.startswith("@") or (only and name != only):
                continue
            w = int((o.get("downloads") or {}).get("weekly") or 0)
            weekly[name] = max(w, weekly.get(name, 0))

    for term in SEED_TERMS:
        for frm in (0, 250):
            add(search(term, 250, frm))
    missing = []
    for name in dict.fromkeys(MUST_INCLUDE):
        before = name in weekly
        add(search(name, 20), only=name)
        if name not in weekly and not before:
            missing.append(name)

    ranked = sorted(weekly.items(), key=lambda kv: (-kv[1], kv[0]))[:args.count]
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# npm popular-package baseline for typosquat-check.ps1 / typosquat-check.py\n")
        f.write("# Unscoped npm packages ranked by weekly downloads (registry.npmjs.org/-/v1/search downloads.weekly).\n")
        f.write("# Snapshot: %s. Regenerate: python3 scripts/data/refresh-npm-popular.py\n" % datetime.date.today().isoformat())
        f.write("# Format: <name><TAB><weekly downloads>, highest first.\n")
        for name, w in ranked:
            f.write("%s\t%d\n" % (name, w))
    print("wrote %d rows to %s; must-include not found: %s" % (len(ranked), OUT, missing or "none"), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
