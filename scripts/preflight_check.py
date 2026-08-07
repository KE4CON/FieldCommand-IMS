#!/usr/bin/env python3
"""FieldCommand IMS — source integrity preflight.

Catches the class of breakage a browser-loaded, never-compiled app hides:
Python/shell syntax errors, invalid JSON, duplicated-file corruption, and
JavaScript syntax errors inside HTML <script> blocks.

Usage:
    python scripts/preflight_check.py                 # run everything (local pre-push)
    python scripts/preflight_check.py --corruption-only
    python scripts/preflight_check.py --js-only

Exits non-zero if any check fails. Used by .github/workflows/ci.yml.
"""
import os, re, sys, glob, json, subprocess, tempfile, shutil
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rel(p): return os.path.relpath(p, ROOT)
def _skip_git(f): return ".git" in f.replace("\\", "/").split("/")

def py_compile_all():
    import py_compile
    fails = []
    for base in ("python", "docs_generators"):
        for f in glob.glob(os.path.join(ROOT, base, "**", "*.py"), recursive=True):
            try:
                py_compile.compile(f, doraise=True)
            except py_compile.PyCompileError as e:
                fails.append((rel(f), str(e).splitlines()[-1]))
    return fails

def shell_all():
    if not shutil.which("bash"):
        print("       (bash not found — shell check skipped locally; CI runs it)"); return []
    fails = []
    for f in glob.glob(os.path.join(ROOT, "scripts", "**", "*.sh"), recursive=True):
        r = subprocess.run(["bash", "-n", f], capture_output=True, text=True)
        if r.returncode:
            fails.append((rel(f), r.stderr.strip()))
    return fails

def json_all():
    fails = []
    for f in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
        if _skip_git(f): continue
        try:
            json.load(open(f, encoding="utf-8"))
        except Exception as e:
            fails.append((rel(f), str(e)))
    return fails

def corruption():
    fails = []
    exts = {".py", ".html", ".htm", ".js", ".sh"}
    for f in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
        if not os.path.isfile(f) or _skip_git(f): continue
        ext = os.path.splitext(f)[1].lower()
        if ext not in exts: continue
        try:
            c = open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        flags = []
        if ext == ".py":
            if len(re.findall(r'(?m)^if __name__ ?== ?["\']__main__["\']', c)) > 1:
                flags.append("2+ __main__ guards")
            if c.count("SPDX-License-Identifier") > 1:
                flags.append("2+ SPDX headers")
        if ext in (".html", ".htm"):
            # only a line-starting 2nd <!DOCTYPE> is corruption; print-template DOCTYPEs live inside JS strings
            if len(re.findall(r'(?mi)^<!doctype', c)) > 1:
                flags.append("2+ top-level <!DOCTYPE>")
        s = c.strip()
        if len(s) > 800 and s.count(s[:180]) > 1:
            flags.append("early-content chunk recurs (possible whole-file duplication)")
        if flags:
            fails.append((rel(f), "; ".join(flags)))
    return fails

def js_all():
    if not shutil.which("node"):
        print("       (node not found — JS syntax check skipped locally; CI runs it)"); return []
    fails = []
    files = (glob.glob(os.path.join(ROOT, "html", "**", "*.html"), recursive=True) +
             glob.glob(os.path.join(ROOT, "html", "**", "*.js"), recursive=True))
    for f in files:
        c = open(f, encoding="utf-8", errors="replace").read()
        blocks = [c] if f.endswith(".js") else re.findall(r'<script\b[^>]*>(.*?)</script>', c, re.S | re.I)
        for i, b in enumerate(blocks):
            if not b.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
                tf.write(b); name = tf.name
            r = subprocess.run(["node", "--check", name], capture_output=True, text=True)
            os.unlink(name)
            if r.returncode:
                msg = (r.stderr.strip().splitlines() or ["syntax error"])[0]
                fails.append((f"{rel(f)} [script #{i}]", msg))
    return fails

def report(title, fails):
    if fails:
        print(f"[FAIL] {title}:")
        for name, msg in fails:
            print(f"       {name}: {msg}")
    else:
        print(f"[ok]   {title}")
    return not fails

def main():
    args = set(sys.argv[1:])
    ok = True
    if "--js-only" in args:
        ok &= report("JavaScript syntax", js_all())
    elif "--corruption-only" in args:
        ok &= report("Corruption / duplication", corruption())
    else:
        ok &= report("Python compile", py_compile_all())
        ok &= report("Shell syntax", shell_all())
        ok &= report("JSON valid", json_all())
        ok &= report("Corruption / duplication", corruption())
        ok &= report("JavaScript syntax", js_all())
    print("\nPREFLIGHT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
