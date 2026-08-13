#!/usr/bin/env python3
"""
trackA_eliminator.py — sound, complete R1/R2 elimination as a BRANCHING TREE.

Soundness contract (audit item #1 of the night plan):
  * R1 on a single-monomial equation  coeff * v1^e1 * ... * vk^ek = 0  first divides
    out every variable already known nonzero; if nothing remains -> CONTRADICTION
    (branch closed); if one variable remains -> deterministic v := 0; if >= 2 remain
    -> the node BRANCHES INTO ONE CHILD PER REMAINING VARIABLE (u*w = 0  =>  u = 0 OR
    w = 0).  No silent choice, the children jointly cover the parent's solution set.
  * R2 solves an equation for a variable v ONLY when the full coefficient of v in the
    equation is a single term  c * m  with c a nonzero rational and m a monomial all
    of whose variables are already known nonzero, AND m divides every monomial of the
    remainder B (divisibility checked at PIVOT SELECTION — the Session-20
    infinite-loop fix).  Then v := -B/(c*m) is polynomial and v is eliminated.
    If v was known nonzero, the constraint "replacement != 0" is RECORDED in
    nonzero_exprs (never silently dropped).
  * A state is CLOSED (contradiction) exactly when an equation reduces to a nonzero
    constant, or a variable known nonzero is forced to 0.  Closed branches emit
    machine-replayable certificates; --verify replays every certificate against the
    root system with independent step checking.
  * Enrichment (sound): from an equation  c*m + c0 = 0  with c, c0 nonzero constants
    and m a monomial, every variable of m is nonzero.

Primary mode: exact arithmetic over Q (fractions.Fraction).
Optional scouting mode: --mod P with P a prime = 1 (mod 3) (evidence only, never proof).

Input: a system JSON produced by trackA_gghv_system.py.
Output: a tree JSON (default trackA_reduced_system.json) with, per leaf, either a
closure certificate or the reduced OPEN system (equations, substitution stack,
nonzero facts) for Track B.

CLI:
  python3 trackA_eliminator.py --system trackA_system_case2.json \
      --normalize d_2_1=1 --out trackA_reduced_system.json
  python3 trackA_eliminator.py --selftest
  python3 trackA_eliminator.py --verify trackA_reduced_system.json
"""

from fractions import Fraction
import argparse
import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------- coefficients
MODP = None            # None -> exact Q; else prime modulus (scouting only)


def cnum(x):
    if MODP is None:
        return Fraction(x)
    return x % MODP


def cfrac(fr):
    """Fraction -> coefficient in current mode."""
    if MODP is None:
        return fr
    num, den = fr.numerator, fr.denominator
    if den % MODP == 0:
        raise ZeroDivisionError("denominator divisible by scouting prime")
    return (num * pow(den, -1, MODP)) % MODP


def cadd(a, b):
    return a + b if MODP is None else (a + b) % MODP


def cmul(a, b):
    return a * b if MODP is None else (a * b) % MODP


def cneg(a):
    return -a if MODP is None else (-a) % MODP


def cdiv(a, b):
    if MODP is None:
        return a / b
    return (a * pow(b, -1, MODP)) % MODP


def ciszero(a):
    return a == 0 if MODP is None else a % MODP == 0


# --------------------------------------------------------------------- polynomials
# poly: dict  monomial -> coeff;  monomial: tuple of (var, exp), sorted by var, exp>=1.

def pzero():
    return {}


def pconst(c):
    return {(): c} if not ciszero(c) else {}


def pvar(v):
    return {((v, 1),): cnum(1)}


def padd(p, q):
    r = dict(p)
    for m, c in q.items():
        nc = cadd(r.get(m, cnum(0)), c)
        if ciszero(nc):
            r.pop(m, None)
        else:
            r[m] = nc
    return r


def pscale(p, c):
    if ciszero(c):
        return {}
    return {m: cmul(cc, c) for m, cc in p.items()}


def mono_mul(m1, m2):
    d = {}
    for v, e in m1:
        d[v] = d.get(v, 0) + e
    for v, e in m2:
        d[v] = d.get(v, 0) + e
    return tuple(sorted(d.items()))


def pmul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = mono_mul(m1, m2)
            nc = cadd(r.get(m, cnum(0)), cmul(c1, c2))
            if ciszero(nc):
                r.pop(m, None)
            else:
                r[m] = nc
    return r


def ppow(p, e):
    r = pconst(cnum(1))
    for _ in range(e):
        r = pmul(r, p)
    return r


def psub_var(p, v, repl):
    """Substitute v -> repl (a poly) in p, exactly."""
    out = {}
    for m, c in p.items():
        ve = 0
        rest = []
        for (w, e) in m:
            if w == v:
                ve = e
            else:
                rest.append((w, e))
        term = {tuple(rest): c}
        if ve:
            term = pmul(term, ppow(repl, ve))
        for mm, cc in term.items():
            nc = cadd(out.get(mm, cnum(0)), cc)
            if ciszero(nc):
                out.pop(mm, None)
            else:
                out[mm] = nc
    return out


def pvars(p):
    s = set()
    for m in p:
        for v, _ in m:
            s.add(v)
    return s


def pcanon(p):
    """Canonical form for dedup/printing: exact mode -> primitive, first-sorted-term
    positive; mod-p -> leading coeff 1."""
    if not p:
        return ()
    items = sorted(p.items())
    if MODP is None:
        from math import gcd
        num = 0
        den = 1
        for _, c in items:
            num = gcd(num, abs(c.numerator))
            den = den * c.denominator // gcd(den, c.denominator)
        scale = Fraction(den, num if num else 1)
        if items[0][1] < 0:
            scale = -scale
        return tuple((m, c * scale) for m, c in items)
    lead = items[0][1]
    inv = pow(lead, -1, MODP)
    return tuple((m, (c * inv) % MODP) for m, c in items)


def pstr(p):
    if not p:
        return "0"
    parts = []
    for m, c in sorted(p.items()):
        ms = "*".join("%s^%d" % (v, e) if e > 1 else v for v, e in m) or "1"
        parts.append("%s*%s" % (c, ms))
    return " + ".join(parts)


# ----------------------------------------------------------------------- system io
def load_system(path):
    with open(path) as fh:
        data = json.load(fh)
    eqs = []
    for ser in data["equations"]:
        p = {}
        for mono, (num, den) in ser["terms"]:
            m = tuple((v, e) for v, e in mono)
            p[m] = cfrac(Fraction(num, den))
        eqs.append(p)
    return data, eqs


# ------------------------------------------------------------------------- states
class Node:
    __slots__ = ("nid", "parent", "eqs", "nonzero", "nonzero_exprs", "steps",
                 "status", "children", "reason", "depth", "merged_into")

    def __init__(self, nid, parent, eqs, nonzero, nonzero_exprs, steps, depth):
        self.nid = nid
        self.parent = parent
        self.eqs = eqs                      # list of polys
        self.nonzero = nonzero              # frozenset of vars
        self.nonzero_exprs = nonzero_exprs  # list of polys that must be != 0
        self.steps = steps                  # certificate steps from the ROOT
        self.status = "open"                # open|closed|leaf|merged|capped
        self.children = []
        self.reason = None
        self.depth = depth
        self.merged_into = None


def canon_key(eqs, nonzero, nonzero_exprs):
    # SOUNDNESS: nonzero_exprs are path-provenance constraints; two states may only
    # be merged when these agree too, else a representative closed via one of its
    # exprs would wrongly close the other path.
    hs = hashlib.sha256()
    for cp in sorted(pcanon(p) for p in eqs):
        hs.update(repr(cp).encode())
    hs.update(repr(sorted(nonzero)).encode())
    for cp in sorted(set(pcanon(p) for p in nonzero_exprs)):
        hs.update(b"NZE" + repr(cp).encode())
    return hs.hexdigest()


def prune_nonzero_exprs(exprs):
    """Drop satisfied (constant nonzero) and duplicate constraints."""
    out = []
    seen = set()
    for p in exprs:
        if list(p.keys()) == [()]:      # nonzero constant: satisfied forever
            continue
        k = pcanon(p)
        if k in seen or not p:
            if not p:
                out.append(p)            # keep the vanished one: caller detects
            continue
        seen.add(k)
        out.append(p)
    return out


def simplify_eqs(eqs):
    """Dedup (canonical), drop zeros. Returns (list, contradiction_poly|None)."""
    seen = {}
    out = []
    contra = None
    for p in eqs:
        if not p:
            continue
        if list(p.keys()) == [()]:
            contra = p
            continue
        k = pcanon(p)
        if k in seen:
            continue
        seen[k] = True
        out.append(p)
    out.sort(key=pcanon)
    return out, contra


# ------------------------------------------------------------------ rule selection
def strip_nonzero(m, nonzero):
    """Remove nonzero vars from monomial m; return tuple of remaining (var,exp)."""
    return tuple((v, e) for (v, e) in m if v not in nonzero)


def find_r1_det_or_contra(eqs, nonzero):
    """Single-monomial equations: return ('contra', i) | ('force0', i, var) | None."""
    for i, p in enumerate(eqs):
        if len(p) != 1:
            continue
        (m, c), = p.items()
        rem = strip_nonzero(m, nonzero)
        if not rem:
            return ("contra", i)
        dvars = [v for v, _ in rem]
        if len(dvars) == 1:
            return ("force0", i, dvars[0])
    return None


def find_enrich(eqs, nonzero):
    """Equation c*m + c0 = 0 (two terms, one the constant) -> vars(m) all nonzero."""
    for i, p in enumerate(eqs):
        if len(p) != 2 or () not in p:
            continue
        m = [mm for mm in p if mm != ()][0]
        new = [v for v, _ in m if v not in nonzero]
        if new:
            return (i, new)
    return None


def find_r2(eqs, nonzero, max_repl_terms):
    """Find (i, var, coeff_c, coeff_mono, B) with the pivot contract of the header.

    Deterministic: first equation in order, then first admissible variable in sorted
    order; prefer pivots with constant coefficient (empty monomial) and small B.
    """
    best = None
    for i, p in enumerate(eqs):
        cand_vars = {}
        for m, c in p.items():
            for v, e in m:
                cand_vars.setdefault(v, []).append((m, c, e))
        for v in sorted(cand_vars):
            occ = cand_vars[v]
            if any(e > 1 for _, _, e in occ):
                continue
            if len(occ) != 1:
                continue                      # coefficient of v must be a single term
            m, c, _ = occ[0]
            cof = tuple(t for t in m if t[0] != v)   # cofactor monomial
            if any(w not in nonzero for w, _ in cof):
                continue
            # B = p - c * v * cof
            B = dict(p)
            del B[m]
            if not B:
                # equation says c * (nonzero mono) * v = 0 -> v = 0 (R1-det handles);
                # treat here as pivot with B = 0 for uniformity
                pass
            # divisibility of every monomial of B by cof (checked at SELECTION)
            ok = True
            cofd = dict(cof)
            for mm in B:
                md = dict(mm)
                for w, e in cofd.items():
                    if md.get(w, 0) < e:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            if len(B) > max_repl_terms:
                continue
            score = (len(B) > 0 and len(cof) > 0, len(B), i, v)
            if best is None or score < best[0]:
                best = (score, i, v, c, cof, B)
    if best is None:
        return None
    _, i, v, c, cof, B = best
    return (i, v, c, cof, B)


def find_r1_branch(eqs, nonzero):
    """Smallest multi-var single-monomial equation to branch on."""
    best = None
    for i, p in enumerate(eqs):
        if len(p) != 1:
            continue
        (m, _), = p.items()
        rem = strip_nonzero(m, nonzero)
        dvars = sorted(set(v for v, _ in rem))
        if len(dvars) >= 2:
            key = (len(dvars), pcanon(p))
            if best is None or key < best[0]:
                best = (key, i, dvars)
    if best is None:
        return None
    _, i, dvars = best
    return (i, dvars)


def divide_B_by_cof(B, cof, c):
    """Return -B / (c * cof) as a poly (divisibility pre-checked)."""
    cofd = dict(cof)
    out = {}
    for mm, cc in B.items():
        md = dict(mm)
        for w, e in cofd.items():
            md[w] -= e
            if md[w] == 0:
                del md[w]
        out[tuple(sorted(md.items()))] = cneg(cdiv(cc, c))
    return out


# ----------------------------------------------------------------------- the tree
def eliminate(root_eqs, root_nonzero, max_nodes=200000, max_repl_terms=400,
              progress=None, checkpoint_path=None, checkpoint_every=2000):
    nodes = []
    dedup = {}
    stats = {"r1_det": 0, "r2": 0, "enrich": 0, "branch_nodes": 0, "contra": 0,
             "merged": 0, "open_leaves": 0, "capped": 0}

    def new_node(parent, eqs, nonzero, nonzero_exprs, steps, depth):
        n = Node(len(nodes), parent, eqs, nonzero, nonzero_exprs, steps, depth)
        nodes.append(n)
        return n

    root = new_node(None, root_eqs, frozenset(root_nonzero), [], [], 0)
    stack = [root.nid]
    t0 = time.time()
    processed = 0

    while stack:
        if len(nodes) > max_nodes:
            for nid in stack:
                nodes[nid].status = "capped"
                stats["capped"] += 1
            break
        nid = stack.pop()
        node = nodes[nid]
        eqs = node.eqs
        nonzero = set(node.nonzero)
        nonzero_exprs = list(node.nonzero_exprs)
        steps = list(node.steps)
        processed += 1
        if progress and processed % progress == 0:
            print("  [t=%.0fs] processed=%d nodes=%d stack=%d closed=%d open=%d"
                  % (time.time() - t0, processed, len(nodes), len(stack),
                     stats["contra"], stats["open_leaves"]), flush=True)
            if checkpoint_path:
                _write_checkpoint(checkpoint_path, nodes, stats, done=False)

        # ---- deterministic closure loop
        closed = False
        while True:
            eqs, contra = simplify_eqs(eqs)
            if contra is not None:
                node.status = "closed"
                node.reason = {"type": "constant_eq", "poly": pstr(contra)}
                steps.append(["contradiction", "nonzero constant equation",
                              pstr(contra)])
                stats["contra"] += 1
                closed = True
                break
            act = find_r1_det_or_contra(eqs, nonzero)
            if act is not None:
                if act[0] == "contra":
                    p = eqs[act[1]]
                    node.status = "closed"
                    node.reason = {"type": "monomial_of_nonzeros", "poly": pstr(p)}
                    steps.append(["contradiction",
                                  "single monomial in nonzero-only vars", pstr(p)])
                    stats["contra"] += 1
                    closed = True
                    break
                _, i, v = act
                if v in nonzero:
                    node.status = "closed"
                    node.reason = {"type": "nonzero_forced_zero", "var": v}
                    steps.append(["contradiction", "nonzero var forced 0", v])
                    stats["contra"] += 1
                    closed = True
                    break
                steps.append(["sub", v, "0", "R1-det from: " + pstr(eqs[i])])
                eqs = [psub_var(p, v, {}) for p in eqs]
                nonzero_exprs = [psub_var(p, v, {}) for p in nonzero_exprs]
                if any(not p for p in nonzero_exprs):
                    node.status = "closed"
                    node.reason = {"type": "nonzero_expr_vanished", "var": v}
                    steps.append(["contradiction",
                                  "recorded nonzero expression became 0 after " + v
                                  + ":=0", ""])
                    stats["contra"] += 1
                    closed = True
                    break
                stats["r1_det"] += 1
                continue
            enr = find_enrich(eqs, nonzero)
            if enr is not None:
                i, new = enr
                nonzero.update(new)
                steps.append(["nonzero", new, "enrich from: " + pstr(eqs[i])])
                stats["enrich"] += 1
                continue
            r2 = find_r2(eqs, nonzero, max_repl_terms)
            if r2 is not None:
                i, v, c, cof, B = r2
                repl = divide_B_by_cof(B, cof, c)
                steps.append(["sub", v, pstr(repl), "R2 from: " + pstr(eqs[i])])
                eqs = [psub_var(p, v, repl) for p in eqs]
                nonzero_exprs = [psub_var(p, v, repl) for p in nonzero_exprs]
                if v in nonzero:
                    nonzero.discard(v)
                    if not repl:
                        node.status = "closed"
                        node.reason = {"type": "nonzero_forced_zero", "var": v}
                        steps.append(["contradiction", "nonzero var forced 0", v])
                        stats["contra"] += 1
                        closed = True
                        break
                    nonzero_exprs.append(repl)
                    steps.append(["nonzero_expr", pstr(repl),
                                  "transferred from nonzero var " + v])
                if any((not p) for p in nonzero_exprs):
                    node.status = "closed"
                    node.reason = {"type": "nonzero_expr_vanished", "var": v}
                    steps.append(["contradiction",
                                  "recorded nonzero expression became 0 after R2 on "
                                  + v, ""])
                    stats["contra"] += 1
                    closed = True
                    break
                stats["r2"] += 1
                continue
            break
        node.steps = steps
        node.nonzero = frozenset(nonzero)
        node.nonzero_exprs = nonzero_exprs
        node.eqs = eqs
        if closed:
            continue

        # ---- dedup
        nonzero_exprs = prune_nonzero_exprs(nonzero_exprs)
        node.nonzero_exprs = nonzero_exprs
        key = canon_key(eqs, nonzero, nonzero_exprs)
        if key in dedup and dedup[key] != nid:
            node.status = "merged"
            node.merged_into = dedup[key]
            stats["merged"] += 1
            continue
        dedup[key] = nid

        # ---- R1 or-branching
        br = find_r1_branch(eqs, nonzero)
        if br is None:
            node.status = "leaf"
            stats["open_leaves"] += 1
            continue
        i, dvars = br
        node.status = "branched"
        node.reason = {"type": "r1_or_branch", "poly": pstr(eqs[i]), "vars": dvars}
        stats["branch_nodes"] += 1
        for v in dvars:
            ceqs = [psub_var(p, v, {}) for p in eqs]
            cnz = [psub_var(p, v, {}) for p in nonzero_exprs]
            csteps = steps + [["branch", v,
                               "OR-branch on " + pstr(eqs[i]) + " ; this child: "
                               + v + " := 0"]]
            child = new_node(nid, ceqs, frozenset(nonzero), cnz, csteps,
                             node.depth + 1)
            node.children.append(child.nid)
            stack.append(child.nid)

    if checkpoint_path:
        _write_checkpoint(checkpoint_path, nodes, stats, done=True)
    return nodes, stats


# ------------------------------------------------------------------- serialization
def node_to_json(n, with_system):
    d = {"id": n.nid, "parent": n.parent, "status": n.status, "depth": n.depth,
         "steps": n.steps, "children": n.children, "reason": n.reason,
         "merged_into": n.merged_into,
         "nonzero": sorted(n.nonzero)}
    if with_system and n.status in ("leaf", "capped"):
        d["equations"] = [pstr(p) for p in n.eqs]
        d["equations_raw"] = [[[list(m), [c.numerator, c.denominator]
                                if MODP is None else [c, 1]]
                               for m, c in sorted(p.items())] for p in n.eqs]
        d["nonzero_exprs"] = [pstr(p) for p in n.nonzero_exprs]
        d["n_vars"] = len(set().union(*[pvars(p) for p in n.eqs])) if n.eqs else 0
        d["n_eqs"] = len(n.eqs)
    return d


def _write_checkpoint(path, nodes, stats, done):
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump({"done": done, "stats": stats,
                   "nodes": [node_to_json(n, True) for n in nodes]}, fh)
    os.replace(tmp, path)


# ------------------------------------------------------------------ verification
def _replay_one(eqs0, root_nonzero, steps):
    """Replay one certificate with step-by-step validation.

    Returns (ok, message). Validation per step:
      sub/R1-det : some current equation is a single monomial whose non-nonzero
                   vars are exactly {v}, and the replacement is 0.
      sub/R2     : some current equation equals c*cof*v + B with cof a monomial in
                   nonzero vars, cof | B, and the recorded replacement == -B/(c*cof).
      branch     : v not in nonzero, and some current single-monomial equation
                   contains v among its non-nonzero variables.
      nonzero    : justified by an equation  c*m + c0 = 0 with c0 constant.
      contradiction: re-derived from the current state, per kind.
    """
    eqs = [dict(p) for p in eqs0]
    nonzero = set(root_nonzero)
    nz_exprs = []
    for step in steps:
        eqs, contra = simplify_eqs(eqs)
        tag = step[0]
        if tag == "sub":
            v, repl_str, why = step[1], step[2], step[3]
            repl = parse_poly(repl_str)
            if why.startswith("R1-det"):
                if repl != {}:
                    return False, "R1-det with nonzero replacement"
                if not any(len(p) == 1 and
                           set(w for w, _ in strip_nonzero(list(p)[0], nonzero))
                           == {v} for p in eqs):
                    return False, "R1-det: no single-monomial equation forcing " + v
            elif why.startswith("R2"):
                found = False
                for p in eqs:
                    occ = [(m, c) for m, c in p.items()
                           if any(w == v and e == 1 for w, e in m)]
                    if len(occ) != 1 or any(
                            any(w == v and e > 1 for w, e in m) for m in p):
                        continue
                    m, c = occ[0]
                    cof = tuple(t for t in m if t[0] != v)
                    if any(w not in nonzero for w, _ in cof):
                        continue
                    B = dict(p)
                    del B[m]
                    cofd = dict(cof)
                    if any(dict(mm).get(w, 0) < e for mm in B
                           for w, e in cofd.items()):
                        continue
                    if divide_B_by_cof(B, cof, c) == repl:
                        found = True
                        break
                if not found:
                    return False, "R2: no equation validates pivot for " + v
            else:
                return False, "unknown sub provenance: " + why
            eqs = [psub_var(p, v, repl) for p in eqs]
            nz_exprs = [psub_var(p, v, repl) for p in nz_exprs]
            if v in nonzero:
                nonzero.discard(v)
                if repl == {}:
                    # will be justified by a following contradiction step
                    nz_exprs.append({})
                else:
                    nz_exprs.append(repl)
        elif tag == "branch":
            v = step[1]
            if v in nonzero:
                return False, "branch sets nonzero var to 0"
            if not any(len(p) == 1 and
                       v in set(w for w, _ in strip_nonzero(list(p)[0], nonzero))
                       for p in eqs):
                return False, "branch: no single-monomial equation contains " + v
            eqs = [psub_var(p, v, {}) for p in eqs]
            nz_exprs = [psub_var(p, v, {}) for p in nz_exprs]
        elif tag == "nonzero":
            new = step[1]
            just = False
            for p in eqs:
                if len(p) == 2 and () in p:
                    m = [mm for mm in p if mm != ()][0]
                    if set(new) <= set(w for w, _ in m):
                        just = True
                        break
            if not just:
                return False, "nonzero enrichment unjustified: %s" % new
            nonzero.update(new)
        elif tag == "nonzero_expr":
            pass                              # recorded at sub time already
        elif tag == "contradiction":
            kind = step[1]
            eqs, contra = simplify_eqs(eqs)
            if kind == "nonzero constant equation":
                if contra is None:
                    return False, "no constant contradiction present"
            elif kind == "single monomial in nonzero-only vars":
                if not any(len(p) == 1 and not strip_nonzero(list(p)[0], nonzero)
                           for p in eqs):
                    return False, "no all-nonzero monomial equation present"
            elif kind == "nonzero var forced 0":
                v = step[2]
                forced_by_eq = any(
                    len(p) == 1 and
                    set(w for w, _ in strip_nonzero(list(p)[0], nonzero)) == {v}
                    for p in eqs) and v in nonzero
                forced_by_sub = {} in nz_exprs
                if not (forced_by_eq or forced_by_sub):
                    return False, "nonzero-forced-zero not re-derivable for " + v
            elif kind.startswith("recorded nonzero expression"):
                if {} not in nz_exprs:
                    return False, "no vanished nonzero expression found"
            else:
                return False, "unknown contradiction kind: " + kind
            return True, "ok"
        else:
            return False, "unknown step tag " + tag
    return False, "certificate ended without contradiction"


def verify_tree(tree_path, system_path):
    """Independent replay of every closed branch's certificate."""
    global MODP
    data = json.load(open(tree_path))
    MODP = data["meta"].get("mod")
    sysdata, eqs0 = load_system(system_path)
    norm = data["meta"].get("normalize", {})
    for v, val in norm.items():
        eqs0 = [psub_var(p, v, pconst(cfrac(Fraction(val)))) for p in eqs0]
    root_nonzero = set(data["meta"]["root_nonzero"])
    n_ok = n_closed = 0
    for n in data["nodes"]:
        if n["status"] != "closed":
            continue
        n_closed += 1
        ok, msg = _replay_one(eqs0, root_nonzero, n["steps"])
        if ok:
            n_ok += 1
        else:
            print("REPLAY FAILURE at node %d: %s" % (n["id"], msg))
    print("verify: %d/%d closed-branch certificates replayed OK" % (n_ok, n_closed))
    return n_ok == n_closed


def parse_poly(s):
    """Parse pstr output back to a poly (for replay)."""
    s = s.strip()
    if s == "0":
        return {}
    out = {}
    for part in s.split(" + "):
        cstr, mstr = part.split("*", 1)
        c = cfrac(Fraction(cstr))
        m = []
        if mstr != "1":
            for f in mstr.split("*"):
                if "^" in f:
                    v, e = f.split("^")
                    m.append((v, int(e)))
                else:
                    m.append((f, 1))
        mono = tuple(sorted(m))
        out[mono] = cadd(out.get(mono, cnum(0)), c)
    return {m: c for m, c in out.items() if not ciszero(c)}


# ---------------------------------------------------------------------- selftests
def selftest():
    """Demonstrate the soundness properties on tiny systems."""
    global MODP
    MODP = None
    print("selftest 1: u*w = 0 must OR-branch (audit item #1)")
    eqs = [{((("u"), 1), (("w"), 1)): Fraction(3)}]
    eqs = [{(("u", 1), ("w", 1)): Fraction(3)}]
    nodes, stats = eliminate(eqs, [])
    branch_nodes = [n for n in nodes if n.status == "branched"]
    assert len(branch_nodes) == 1 and len(branch_nodes[0].children) == 2, stats
    print("  OK: 1 branch node with 2 children (u:=0 | w:=0), no silent choice")

    print("selftest 2: divisibility checked at pivot selection (no infinite loop)")
    # a*v + b^2 = 0 with a nonzero-known: pivot on v needs a | b^2 -> rejected;
    # b has exponent 2 (not linear), a's cofactor contains v (not nonzero) -> no R2.
    eqs = [{(("a", 1), ("v", 1)): Fraction(1), (("b", 2),): Fraction(1)}]
    nodes, stats = eliminate(eqs, ["a"])
    leaf = [n for n in nodes if n.status == "leaf"]
    assert stats["r2"] == 0 and len(leaf) == 1, stats
    print("  OK: pivot rejected at selection, leaf kept open with equation intact")

    print("selftest 3: R2 fires when the pivot monomial does divide B")
    # a*v + a*b = 0, a nonzero -> v := -b
    eqs = [{(("a", 1), ("v", 1)): Fraction(1),
            (("a", 1), ("b", 1)): Fraction(1)}]
    nodes, stats = eliminate(eqs, ["a"])
    assert stats["r2"] == 1
    print("  OK: v := -b, certificate:", nodes[0].steps)

    print("selftest 4: contradiction on nonzero var forced to zero")
    eqs = [{(("u", 1),): Fraction(2)}]
    nodes, stats = eliminate(eqs, ["u"])
    assert nodes[0].status == "closed"
    print("  OK: closed with reason", nodes[0].reason)

    print("selftest 5: constant equation contradiction")
    eqs = [{(): Fraction(5)}]
    nodes, stats = eliminate(eqs, [])
    assert nodes[0].status == "closed"
    print("  OK")

    print("selftest 6: or-branch cascade + sound dedup (u*w=0, u^2+w^2+u*w=0)")
    eqs = [{(("u", 1), ("w", 1)): Fraction(1)},
           {(("u", 2),): Fraction(1), (("w", 2),): Fraction(1),
            (("u", 1), ("w", 1)): Fraction(1)}]
    nodes, stats = eliminate(eqs, [])
    # branch u:=0 -> w^2=0 -> w:=0; branch w:=0 -> u:=0; identical terminal states
    # merge (same eqs, nonzero, AND nonzero_exprs), leaving one leaf.
    leaves = [n for n in nodes if n.status == "leaf"]
    merged = [n for n in nodes if n.status == "merged"]
    assert stats["branch_nodes"] == 1 and len(leaves) == 1 and len(merged) == 1, stats
    print("  OK: both children explored, cascade forced the other var, states merged")

    print("selftest 7: enrichment (v*m + const = 0 => vars of m nonzero)")
    eqs = [{(("u", 1), ("w", 1)): Fraction(1), (): Fraction(-1)},
           {(("u", 1), ("z", 1)): Fraction(1)}]
    nodes, stats = eliminate(eqs, [])
    # u,w nonzero by enrichment; then u*z = 0 forces z = 0 deterministically.
    assert stats["enrich"] >= 1 and stats["r1_det"] >= 1
    print("  OK: no branching needed; z forced 0 after enrichment")
    print("ALL SELFTESTS PASS")


# --------------------------------------------------------------------------- main
def main():
    global MODP
    ap = argparse.ArgumentParser()
    ap.add_argument("--system")
    ap.add_argument("--normalize", default=None,
                    help="e.g. d_2_1=1 (comma separated var=rational)")
    ap.add_argument("--out", default=os.path.join(HERE, "trackA_reduced_system.json"))
    ap.add_argument("--mod", type=int, default=None)
    ap.add_argument("--max-nodes", type=int, default=200000)
    ap.add_argument("--max-repl-terms", type=int, default=400)
    ap.add_argument("--progress", type=int, default=500)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--verify", nargs=2, metavar=("TREE", "SYSTEM"))
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return
    if args.verify:
        ok = verify_tree(args.verify[0], args.verify[1])
        sys.exit(0 if ok else 1)

    MODP = args.mod
    if MODP is not None and MODP % 3 != 1:
        print("WARNING: scouting prime %d is not = 1 mod 3; refusing." % MODP)
        sys.exit(2)

    sysdata, eqs = load_system(args.system)
    nonzero = list(sysdata["nonzero"])
    norm = {}
    if args.normalize:
        for item in args.normalize.split(","):
            v, val = item.split("=")
            norm[v] = val
            eqs = [psub_var(p, v, pconst(cfrac(Fraction(val)))) for p in eqs]
            if v in nonzero and Fraction(val) != 0:
                nonzero.remove(v)
    print("eliminator: %d equations, %d variables, nonzero=%s, normalize=%s, mode=%s"
          % (len(eqs), len(set().union(*[pvars(p) for p in eqs])), nonzero, norm,
             "exact-Q" if MODP is None else "mod %d (SCOUTING ONLY)" % MODP))
    t0 = time.time()
    nodes, stats = eliminate(eqs, nonzero, max_nodes=args.max_nodes,
                             max_repl_terms=args.max_repl_terms,
                             progress=args.progress,
                             checkpoint_path=args.out + ".ckpt")
    dt = time.time() - t0
    print("done in %.1fs; stats: %s" % (dt, stats))
    leaves = [n for n in nodes if n.status == "leaf"]
    closed = [n for n in nodes if n.status == "closed"]
    print("tree: %d nodes, %d closed, %d open leaves, %d merged, %d capped"
          % (len(nodes), len(closed), len(leaves),
             stats["merged"], stats["capped"]))
    for n in leaves:
        nv = len(set().union(*[pvars(p) for p in n.eqs])) if n.eqs else 0
        print("  open leaf %d (depth %d): %d eqs, %d vars" %
              (n.nid, n.depth, len(n.eqs), nv))
    meta = {"system": os.path.basename(args.system),
            "system_hash": sysdata.get("content_hash"),
            "normalize": norm, "root_nonzero": nonzero, "mod": MODP,
            "stats": stats, "elapsed_sec": dt,
            "soundness": "R1 or-branching over every variable of the monomial; "
                         "R2 pivots only unit*nonzero-monomial with divisibility "
                         "checked at selection; every closed branch certified"}
    with open(args.out, "w") as fh:
        json.dump({"meta": meta,
                   "nodes": [node_to_json(n, True) for n in nodes]}, fh)
    print("written:", args.out)


if __name__ == "__main__":
    main()
