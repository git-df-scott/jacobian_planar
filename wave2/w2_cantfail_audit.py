"""
Wave 2 - The can't-fail audit.

A certifier whose check condition is a literal `True` certifies nothing.  Three
such lines were found in the wave-1 certifiers:

    w1_h1c_endgame_closed_form.py:89   check("k >= 1 forces c = 0...", True, ...)
    w1_h1e_d_crossfire.py:58           check(..., True, ...)
    w1_h1e_d_crossfire.py:88           check(..., True, ...)

The first one is the serious case: it "certified" precisely the statement that
w2_h1c_refutation.py refutes with an explicit counterexample.

This script scans every Python file in the repository, by AST rather than by
regex, for check-style calls whose condition argument is a compile-time
constant -- `True`, `1`, a non-empty string, and so on.  It reports them and
exits nonzero if any are found, so it can be wired into CI.

It is itself tested: a synthetic file containing one rigged check and one
honest check is scanned, and the scanner must find exactly the rigged one.
"""

import ast
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK_NAMES = {"check", "assert_check", "record", "certify", "verify", "claim"}


def constant_truth(node):
    """Is this AST node a compile-time constant that is always truthy?"""
    try:
        val = ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError):
        return None
    return bool(val)


def scan_source(src, filename):
    """Return [(lineno, funcname, label, literal_repr)] for rigged checks."""
    out = []
    try:
        tree = ast.parse(src, filename=filename)
    except SyntaxError as e:
        return [(getattr(e, "lineno", 0), "<parse-error>", str(e), "")]
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
        if name not in CHECK_NAMES:
            continue
        # the condition is the first non-string positional arg, or the second
        # positional arg when the first is a label string.
        args = list(node.args)
        cond = None
        if args:
            first = constant_truth(args[0])
            if isinstance(args[0], ast.Constant) and isinstance(args[0].value, str) and len(args) > 1:
                cond = args[1]
            elif first is None:
                cond = None          # first arg is an expression -> honest
            else:
                cond = args[0]
        for kw in node.keywords:
            if kw.arg in ("cond", "condition", "ok", "value"):
                cond = kw.value
        if cond is None:
            continue
        truth = constant_truth(cond)
        if truth is True:
            label = ""
            if args and isinstance(args[0], ast.Constant) and isinstance(args[0].value, str):
                label = args[0].value
            out.append((node.lineno, name, label, ast.unparse(cond)))
    return out


def scan_tree(root):
    findings = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                src = f.read()
            for hit in scan_source(src, path):
                findings.append((os.path.relpath(path, root),) + hit)
    return findings


# ---------------------------------------------------------------------------
# Self-test: the scanner must catch a rigged check and must NOT flag an honest
# one.  Without this the auditor would be the same kind of object it audits.
# ---------------------------------------------------------------------------
SELFTEST = '''
def check(name, cond, note=None):
    pass

check("rigged - can never fail", True, "note")
check("honest", 2 + 2 == 4)
check("honest too", some_value != 0)
'''
with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
    tf.write(SELFTEST)
    tmp = tf.name
hits = scan_source(SELFTEST, tmp)
os.unlink(tmp)

print("=" * 74)
print("SELF-TEST OF THE SCANNER")
print("=" * 74)
print(f"    synthetic file: 1 rigged check, 2 honest checks")
print(f"    scanner found {len(hits)} rigged: {[(h[0], h[2]) for h in hits]}")
selftest_ok = len(hits) == 1 and "rigged" in hits[0][2]
print(f"    self-test {'PASS' if selftest_ok else 'FAIL'}")

# ---------------------------------------------------------------------------
print()
print("=" * 74)
print(f"SCANNING {ROOT}")
print("=" * 74)
found = scan_tree(ROOT)
if found:
    for path, line, name, label, cond in found:
        print(f"    {path}:{line}  {name}(..., {cond}, ...)   label={label!r}")
else:
    print("    no compile-time-constant check conditions found in this tree")

print()
print("=" * 74)
print("KNOWN WAVE-1 OFFENDERS  (files not present in this repository)")
print("=" * 74)
KNOWN = [
    ("w1_h1c_endgame_closed_form.py", 89,
     "check(\"k >= 1 forces c = 0...\", True, ...)",
     "SEVERE - certified the statement refuted by wave2/w2_h1c_refutation.py"),
    ("w1_h1e_d_crossfire.py", 58, "check(..., True, ...)",
     "LOW - wraps a prose claim, but still cannot fail"),
    ("w1_h1e_d_crossfire.py", 88, "check(..., True, ...)",
     "LOW - wraps a prose claim, but still cannot fail"),
]
for fn, line, snippet, sev in KNOWN:
    present = os.path.exists(os.path.join(ROOT, fn))
    print(f"    {fn}:{line}   {snippet}")
    print(f"        severity: {sev}")
    print(f"        file present in this repository: {present}")
print("""
    RULE ADOPTED FOR WAVE 2 AND AFTER
    Every check condition must be an expression computed from the objects
    under test.  Every certifier must contain at least one NEGATIVE CONTROL
    -- an input on which it is required to fail -- so that "all checks
    passed" carries information.  All five wave-2 certifiers comply.
""")

ok = selftest_ok and not found
print("=" * 74)
print(f"    scanner self-test: {'PASS' if selftest_ok else 'FAIL'}")
print(f"    rigged checks in tree: {len(found)}")
print("=" * 74)
sys.exit(0 if ok else 1)
