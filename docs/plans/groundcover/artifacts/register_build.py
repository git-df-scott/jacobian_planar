#!/usr/bin/env python3
"""Build a machine-readable register of every msolve (*.ms) system in the JC2
campaign worktrees, plus an enumeration of every recorded timeout shape.

Read-only w.r.t. the worktrees. Writes REGISTER.json, TIMEOUT_SHAPES.json,
REGISTER_SUMMARY.md into OUT.
"""
import os, re, sys, json, hashlib, random, collections

WT  = "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt"
OUT = "/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/groundcover"
BIG = 5 * 1024 * 1024          # header-only threshold
PRIME1 = 2147483629            # rank computed mod these two 31-bit primes
PRIME2 = 2147483587            # (entries are tiny exponent differences)
MAXROWS = 4000                 # cap on difference rows fed to the rank engine

# ---------------------------------------------------------------- parsing ---
def split_top(s, sep=','):
    out, depth, cur = [], 0, []
    for ch in s:
        if ch in '([{': depth += 1
        elif ch in ')]}': depth -= 1
        if ch == sep and depth == 0:
            out.append(''.join(cur)); cur = []
        else:
            cur.append(ch)
    out.append(''.join(cur))
    return out

TERM_SPLIT = re.compile(r'(?<![\^*])([+-])')
def split_terms(poly):
    """Split a paren-free polynomial into signed term strings."""
    terms, depth, cur, sign = [], 0, [], 1
    i, n = 0, len(poly)
    while i < n:
        ch = poly[i]
        if ch in '([{': depth += 1
        elif ch in ')]}': depth -= 1
        if depth == 0 and ch in '+-' and cur and poly[i-1] not in '*^+-/(':
            terms.append((sign, ''.join(cur))); cur = []
            sign = 1 if ch == '+' else -1
        elif depth == 0 and ch in '+-' and not cur:
            if ch == '-': sign = -sign
        else:
            cur.append(ch)
        i += 1
    if cur: terms.append((sign, ''.join(cur)))
    return terms

def parse_term(sign, t):
    """-> (coeff:int, monomial: tuple((var,exp),...) sorted)."""
    coeff, expo = sign, {}
    for f in t.split('*'):
        f = f.strip()
        if not f: continue
        if '^' in f:
            b, _, e = f.partition('^')
            b, e = b.strip(), int(e.strip())
        else:
            b, e = f, 1
        if re.fullmatch(r'\d+', b):
            coeff *= int(b) ** e
        elif re.fullmatch(r'-?\d+', b):
            coeff *= int(b) ** e
        else:
            expo[b] = expo.get(b, 0) + e
    return coeff, tuple(sorted(expo.items()))

def parse_poly(poly, char):
    mons = {}
    for sign, t in split_terms(poly):
        c, m = parse_term(sign, t)
        mons[m] = mons.get(m, 0) + c
    if char > 0:
        mons = {m: c % char for m, c in mons.items()}
    return {m: c for m, c in mons.items() if c != 0}

def canon_poly_str(mons):
    return '+'.join('%d*%s' % (c, '.'.join('%s^%d' % v for v in m) or '1')
                    for m, c in sorted(mons.items()))

# ------------------------------------------------------------------- rank ---
import numpy as np

def rank_mod(rows, ncols, p):
    """Exact rank of a small-integer matrix mod the 31-bit prime p (vectorized)."""
    M = np.asarray(rows, dtype=np.int64) % p
    r = 0
    for c in range(ncols):
        if r >= M.shape[0]: break
        nz = np.nonzero(M[r:, c])[0]
        if nz.size == 0: continue
        i = r + int(nz[0])
        if i != r: M[[r, i]] = M[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r] = (M[r] * inv) % p
        col = M[r + 1:, c].copy()
        nzr = np.nonzero(col)[0]
        if nzr.size:
            M[r + 1 + nzr] = (M[r + 1 + nzr] - col[nzr, None] * M[r][None, :]) % p
        r += 1
        if r == ncols: break
    return r

def torus_rank(gens_mons, varidx):
    """dim of {w : w.(m1-m2)=0 for m1,m2 in the same generator}."""
    n = len(varidx)
    rows = []
    for mons in gens_mons:
        ms = list(mons.keys())
        if len(ms) < 2: continue
        base = [0] * n
        for v, e in ms[0]:
            if v in varidx: base[varidx[v]] = e
        for m in ms[1:]:
            vec = [0] * n
            for v, e in m:
                if v in varidx: vec[varidx[v]] = e
            rows.append([a - b for a, b in zip(vec, base)])
            if len(rows) >= MAXROWS: break
        if len(rows) >= MAXROWS: break
    if not rows: return n, True, 0
    r1 = rank_mod(rows, n, PRIME1)
    exact = True
    if n - r1 > 0:                      # only double-check the claims we report
        r2 = rank_mod(rows, n, PRIME2)
        if r2 != r1: r1 = max(r1, r2); exact = False
    return n - r1, exact, len(rows)

# ------------------------------------------------------------------- file ---
def big_scan(path):
    """Single streaming pass over a huge export: ws-stripped sha256, raw md5,
    and a top-level generator count.  These exports are paren-free (verified
    over the whole corpus), so commas can be counted with a C-level .count()."""
    h = hashlib.sha256(); m = hashlib.md5()
    ncom = 0; last_ns = b''; hasparen = False
    with open(path, 'rb') as fh:
        l1 = fh.readline(); l2 = fh.readline()
        for l in (l1, l2):
            m.update(l); h.update(b''.join(l.split()))
        while True:
            chunk = fh.read(1 << 22)
            if not chunk: break
            m.update(chunk)
            sq = b''.join(chunk.split())
            h.update(sq)
            ncom += chunk.count(b',')
            if b'(' in chunk or b')' in chunk: hasparen = True
            if sq: last_ns = sq[-1:]
    n = ncom + (1 if (last_ns and last_ns != b',') else 0)
    return h.hexdigest(), m.hexdigest(), n, hasparen

def ws_sha(path):
    h = hashlib.sha256(); m = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b''):
            m.update(chunk)
            h.update(b''.join(chunk.split()))
    return h.hexdigest(), m.hexdigest()

def analyse(path, wt, rel):
    size = os.path.getsize(path)
    rec = {"worktree": wt, "path": rel, "abs_path": path, "size_bytes": size,
           "kind": "system", "parse_ok": True, "parse_note": None}
    try:
        with open(path, 'rb') as fh:
            head = fh.readline().decode('utf8', 'replace')
            char_line = fh.readline().decode('utf8', 'replace')
    except Exception as e:
        rec.update(parse_ok=False, parse_note="read error: %s" % e); return rec
    varlist = [v.strip() for v in head.strip().rstrip(',').split(',') if v.strip()]
    cl = char_line.strip()
    if not re.fullmatch(r'\d+', cl):
        # msolve OUTPUT files carry "[dim, deg, [...]]"-ish second lines
        rec.update(kind="msolve_output", parse_ok=False,
                   parse_note="line 2 is not a bare characteristic (%r) -> msolve output, not an input system" % cl[:40])
        rec["n_vars"] = len(varlist)
        rec["sha256_ws"], rec["md5_raw"] = ws_sha(path)
        rec["content_hash"] = rec["sha256_ws"]; rec["hash_mode"] = "raw_ws"
        return rec
    char = int(cl)
    rec["characteristic"] = char
    rec["n_vars"] = len(varlist)
    rec["vars"] = varlist if len(varlist) <= 60 else varlist[:60] + ["..."]

    if size > BIG:
        rec["hash_mode"] = "raw_ws"
        sh, md, ne, hp = big_scan(path)
        rec["sha256_ws"], rec["md5_raw"] = sh, md
        rec["content_hash"] = sh
        rec["n_eqs"] = ne
        rec["has_parens"] = hp
        rec["max_total_degree"] = None
        rec["grading_torus_rank"] = None
        rec["torus_rank_exact"] = None
        rec["has_rabinowitsch"] = None
        rec["parse_note"] = "header-only (>5MB): degree, torus rank and Rabinowitsch scan skipped"
        rec["excess"] = rec["n_eqs"] - rec["n_vars"]
        return rec

    data = open(path, 'rb').read()
    rec["md5_raw"] = hashlib.md5(data).hexdigest()
    text = data.decode('utf8', 'replace')
    body = text.split('\n', 2)[2] if text.count('\n') >= 2 else ''
    raw_gens = [g.strip() for g in split_top(body)]
    raw_gens = [g for g in raw_gens if g]
    varidx = {v: i for i, v in enumerate(varlist)}
    gens_mons, maxdeg, rab, extra = [], 0, False, set()
    try:
        for g in raw_gens:
            mons = parse_poly(g, char)
            gens_mons.append(mons)
            for m in mons:
                maxdeg = max(maxdeg, sum(e for _, e in m))
                for v, _ in m:
                    if v not in varidx: extra.add(v)
            if len(mons) == 2:
                degs = sorted(sum(e for _, e in m) for m in mons)
                if degs[0] == 0 and degs[1] >= 1: rab = True
    except Exception as e:
        rec.update(parse_ok=False, parse_note="poly parse error: %s" % e)
        rec["sha256_ws"], _ = ws_sha(path)
        rec["content_hash"] = rec["sha256_ws"]; rec["hash_mode"] = "raw_ws"
        rec["n_eqs"] = len(raw_gens)
        rec["excess"] = rec["n_eqs"] - rec["n_vars"]
        return rec
    if extra:
        rec["parse_note"] = "monomials use %d symbol(s) absent from the variable line: %s" % (
            len(extra), sorted(extra)[:8])
        for v in sorted(extra): varidx[v] = len(varidx)
    rec["n_eqs"] = len(gens_mons)
    rec["excess"] = rec["n_eqs"] - rec["n_vars"]
    rec["max_total_degree"] = maxdeg
    rec["has_rabinowitsch"] = rab
    canon = '\n'.join(sorted(canon_poly_str(m) for m in gens_mons))
    rec["content_hash"] = hashlib.sha256(
        ('%d|%d|' % (char, len(varlist)) + canon).encode()).hexdigest()
    rec["hash_mode"] = "canonical"
    tr, exact, nrows = torus_rank(gens_mons, varidx)
    rec["grading_torus_rank"] = tr
    rec["torus_rank_exact"] = exact
    rec["torus_rows_used"] = nrows
    return rec

# ------------------------------------------------------------------ main ----
def main():
    files = []
    for wt in sorted(os.listdir(WT)):
        root = os.path.join(WT, wt)
        if not os.path.isdir(root): continue
        for dp, dn, fn in os.walk(root):
            if '.git' in dp.split(os.sep): continue
            for f in fn:
                if f.endswith('.ms'):
                    p = os.path.join(dp, f)
                    if os.path.isfile(p) and not os.path.islink(p):
                        files.append((p, wt, os.path.relpath(p, root)))
    files.sort()
    sys.stderr.write("scanning %d .ms files\n" % len(files))
    recs = []
    for i, (p, wt, rel) in enumerate(files):
        if i % 200 == 0: sys.stderr.write("  [%d/%d]\n" % (i, len(files)))
        try:
            recs.append(analyse(p, wt, rel))
        except Exception as e:
            recs.append({"worktree": wt, "path": rel, "abs_path": p,
                         "size_bytes": os.path.getsize(p), "parse_ok": False,
                         "kind": "system", "parse_note": "fatal: %r" % (e,)})
    json.dump({"generated_from": WT, "n_files": len(recs), "records": recs},
              open(os.path.join(OUT, "REGISTER.json"), "w"), indent=1)
    sys.stderr.write("REGISTER.json written (%d records)\n" % len(recs))
    return recs


# =====================================================================
# PHASE 2 -- timeout enumeration + summary.  Run: register_build.py p2
# =====================================================================
TEXT_EXT = ('.log', '.tsv', '.md', '.txt', '.jsonl', '.csv', '.out', '.json')
CODEISH = re.compile(r'os\.environ|= *int\(|timeout *= *[A-Z_]+|def |import |subprocess|"""')
MS_RE   = re.compile(r'([A-Za-z0-9_.+\-/]+\.ms)')
ENGINES = [('msolve', r'msolve'), ('Singular', r'[Ss]ingular|facstd|\bstd\b|slimgb'),
           ('Macaulay2', r'Macaulay2|\bM2\b'), ('Magma', r'[Mm]agma'),
           ('Maple', r'[Mm]aple'), ('bridge', r'bridge')]
EQVAR = [re.compile(r'(\d+)\s*eqs?\s*/\s*(\d+)\s*vars?'),
         re.compile(r'(\d+)\s*eqs?[ ,]+(\d+)\s*vars?'),
         re.compile(r'"eqs"\s*:\s*(\d+).*?"vars"\s*:\s*(\d+)'),
         re.compile(r'(\d+)\s*equations?[ ,]+(\d+)\s*(?:vars?|variables|unknowns)')]
VAREQ = [re.compile(r'(\d+)\s*vars?\s*/\s*(\d+)\s*eqs?'),
         re.compile(r'"vars"\s*:\s*(\d+).*?"eqs"\s*:\s*(\d+)')]
BUDGET = [re.compile(r'\[(\d+(?:\.\d+)?)\s*s\]'), re.compile(r'\((\d+(?:\.\d+)?)\s*s\)'),
          re.compile(r'\bat\s+(\d+(?:\.\d+)?)\s*s\b'), re.compile(r'\b(\d{2,5})\s*s(?:ec)?\b')]

def classify(line):
    tags = []
    l = line
    if re.search(r'\bTIMEOUT\b|\bTIMED OUT\b|timed out|exit(?:ed with)?[ _]*(?:status )?124|\bstatus 124\b', l, re.I):
        tags.append('TIMEOUT')
    if re.search(r'\bOOM\b|oom[- _]kill|out of memory|memory exhaust', l, re.I):
        tags.append('OOM')
    if re.search(r'\bSIGKILL\b|exit[ _-]*137|exit -9|\bkilled\b', l, re.I):
        tags.append('KILLED')
    if re.search(r'no verdict|NOVERDICT|NO VERDICT|STALLED', l):
        tags.append('NO_VERDICT')
    if re.search(r'0-byte|zero-byte|out 0 B|\bout_bytes[ =:]*0\b', l, re.I):
        tags.append('ZERO_BYTE')
    return tags

def engine_of(line):
    for name, pat in ENGINES:
        if re.search(pat, line): return name
    return None

def numpair(line):
    for r in EQVAR:
        m = r.search(line)
        if m: return int(m.group(1)), int(m.group(2))
    for r in VAREQ:
        m = r.search(line)
        if m: return int(m.group(2)), int(m.group(1))
    return None, None

def budget_of(line):
    for r in BUDGET:
        m = r.search(line)
        if m: return float(m.group(1))
    return None

def phase2():
    reg = json.load(open(os.path.join(OUT, "REGISTER.json")))
    recs = reg["records"]
    by_base = collections.defaultdict(list)
    for r in recs:
        by_base[os.path.basename(r["path"])].append(r)

    # ---- collect candidate text files, de-mirrored across worktrees ----
    seen_files = {}
    for wt in sorted(os.listdir(WT)):
        root = os.path.join(WT, wt)
        if not os.path.isdir(root): continue
        for dp, dn, fn in os.walk(root):
            if '.git' in dp.split(os.sep): continue
            for f in fn:
                if not f.endswith(TEXT_EXT): continue
                p = os.path.join(dp, f)
                try:
                    if not os.path.isfile(p) or os.path.islink(p): continue
                    if os.path.getsize(p) > 20 * 1024 * 1024: continue
                    h = hashlib.md5(open(p, 'rb').read()).hexdigest()
                except Exception:
                    continue
                rel = os.path.relpath(p, root)
                if h in seen_files:
                    seen_files[h]["mirrors"].append(wt + '/' + rel)
                else:
                    seen_files[h] = {"path": p, "label": wt + '/' + rel, "mirrors": []}

    rows = []
    for h, info in sorted(seen_files.items(), key=lambda kv: kv[1]["label"]):
        p, label = info["path"], info["label"]
        try:
            txt = open(p, 'r', errors='replace').read()
        except Exception:
            continue
        is_tsv = p.endswith('.tsv')
        hdr = None
        for ln, line in enumerate(txt.split('\n'), 1):
            line = line.rstrip()
            if not line: continue
            if is_tsv and ln == 1 and 'verdict' in line:
                hdr = line.split('\t'); continue
            if CODEISH.search(line): continue
            tags = classify(line)
            if not tags: continue
            row = {"source_log": label, "line_no": ln,
                   "source_line": line.strip()[:400], "tags": tags,
                   "mirror_count": 1 + len(info["mirrors"])}
            eqs = vars_ = budget = wall = engine = system = None
            if is_tsv and hdr and '\t' in line:
                cells = line.split('\t')
                d = dict(zip(hdr, cells))
                system = d.get('system')
                try: eqs = int(d['generators'])
                except Exception: pass
                try: wall = float(d['seconds'])
                except Exception: pass
                row["verdict"] = d.get('verdict')
                row["peak_rss_kb"] = d.get('peak_rss_kb')
                row["out_bytes"] = d.get('out_bytes')
                engine = 'msolve'
            if system is None:
                m = MS_RE.search(line)
                if m: system = m.group(1)
            e2, v2 = numpair(line)
            if e2 is not None: eqs, vars_ = e2, v2
            budget = budget_of(line)
            engine = engine or engine_of(line)
            ms = re.search(r'max=(\d+)\s+params=(\d+)', line)
            if ms: row["sweep_shape"] = {"max": int(ms.group(1)), "params": int(ms.group(2))}
            row.update(system_named=system, engine=engine,
                       budget_or_wall_s=budget if budget else wall)
            # --- resolve against the register ---
            ch = n_v = n_e = exc = tr = None; matches = []
            if system:
                matches = by_base.get(os.path.basename(system), [])
            if matches:
                hs = {m.get("content_hash") for m in matches}
                ch = matches[0].get("content_hash") if len(hs) == 1 else None
                row["register_paths"] = sorted({m["worktree"] + '/' + m["path"] for m in matches})[:8]
                row["register_hash_ambiguous"] = len(hs) > 1
                m0 = matches[0]
                n_v, n_e = m0.get("n_vars"), m0.get("n_eqs")
                exc, tr = m0.get("excess"), m0.get("grading_torus_rank")
            row.update(system_path=(row.get("register_paths") or [None])[0],
                       content_hash=ch,
                       n_vars=n_v if n_v is not None else vars_,
                       n_eqs=n_e if n_e is not None else eqs,
                       excess=exc if exc is not None else
                              ((n_e - n_v) if (n_e is not None and n_v is not None)
                               else ((eqs - vars_) if (eqs is not None and vars_ is not None) else None)),
                       torus_rank=tr)
            rows.append(row)

    # ---- dedup into shapes ----
    def key(r):
        if r.get("content_hash"): return ("hash", r["content_hash"])
        if r.get("system_named"): return ("name", os.path.basename(r["system_named"]))
        if r.get("sweep_shape"):
            return ("sweep", r["sweep_shape"]["max"], r["sweep_shape"]["params"])
        if r.get("n_vars") and r.get("n_eqs"): return ("size", r["n_vars"], r["n_eqs"])
        return ("line", re.sub(r'\d+', '#', r["source_line"])[:120])
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault(key(r), []).append(r)
    shapes = []
    for k, g in groups.items():
        rep = next((x for x in g if x.get("content_hash")), g[0])
        shapes.append({
            "shape_key": list(k), "n_records": len(g),
            "system_path": rep.get("system_path"), "system_named": rep.get("system_named"),
            "content_hash": rep.get("content_hash"),
            "n_vars": rep.get("n_vars"), "n_eqs": rep.get("n_eqs"),
            "excess": rep.get("excess"), "torus_rank": rep.get("torus_rank"),
            "budget_or_wall_s": rep.get("budget_or_wall_s"),
            "engines": sorted({x["engine"] for x in g if x.get("engine")}),
            "tags": sorted({t for x in g for t in x["tags"]}),
            "source_logs": sorted({x["source_log"] for x in g})[:6],
            "source_line": rep["source_line"],
        })
    hard = [s for s in shapes if 'TIMEOUT' in s['tags'] or 'OOM' in s['tags'] or 'KILLED' in s['tags']]
    json.dump({"n_raw_records": len(rows),
               "n_dedup_shapes": len(shapes),
               "n_dedup_shapes_resource_failure": len(hard),
               "n_shapes_with_content_hash": len({s['content_hash'] for s in shapes if s['content_hash']}),
               "shapes": shapes, "raw_records": rows},
              open(os.path.join(OUT, "TIMEOUT_SHAPES.json"), "w"), indent=1)
    sys.stderr.write("TIMEOUT_SHAPES.json: %d raw records -> %d shapes (%d resource-failure)\n"
                     % (len(rows), len(shapes), len(hard)))
    return reg, recs, shapes, hard

def summarise(reg, recs, shapes, hard):
    sysr = [r for r in recs if r.get("kind") == "system"]
    outs = [r for r in recs if r.get("kind") == "msolve_output"]
    fails = [r for r in recs if not r.get("parse_ok") and r.get("kind") == "system"]
    byhash = collections.defaultdict(list)
    for r in recs:
        if r.get("content_hash"):
            byhash[r["content_hash"]].append(r["worktree"] + '/' + r["path"])
    dups = [{"hash": h, "n": len(v), "paths": sorted(v)}
            for h, v in byhash.items() if len(v) > 1]
    dups.sort(key=lambda d: -d["n"])
    # duplicates that are NOT just the 4x worktree mirror of the same rel path
    real_dups = [d for d in dups
                 if len({p.split('/', 1)[1] for p in d["paths"]}) > 1]
    ok = [r for r in sysr if r.get("parse_ok") and r.get("n_eqs") is not None]
    nonpos = [r for r in ok if r.get("excess") is not None and r["excess"] <= 0]
    tors = [r for r in ok if r.get("grading_torus_rank")]
    def lbl(r): return r["worktree"] + '/' + r["path"]
    # unique-by-hash view (collapse the 4x mirrors)
    uniq = {}
    for r in ok:
        uniq.setdefault(r["content_hash"], r)
    undecided = sorted([r for r in uniq.values() if (r.get("excess") or 0) > 0],
                       key=lambda r: (r["n_vars"], r["n_eqs"], r["size_bytes"]))[:20]
    L = []
    A = L.append
    A("# JC2 msolve system register -- summary\n")
    A("Generated from `%s` (read-only). Files: `REGISTER.json`, `TIMEOUT_SHAPES.json`, `register_build.py`.\n" % WT)
    A("## 1. Counts\n")
    A("| quantity | value |")
    A("|---|---|")
    A("| `.ms` files found | %d |" % len(recs))
    A("| input systems (parsed) | %d |" % len([r for r in sysr if r.get('parse_ok')]))
    A("| msolve *output* files misfiled as `.ms` | %d |" % len(outs))
    A("| parse failures (input systems) | %d |" % len(fails))
    A("| header-only (>5 MB) | %d |" % len([r for r in recs if r.get('hash_mode') == 'raw_ws' and r.get('kind') == 'system']))
    A("| distinct content hashes (all) | %d |" % len(byhash))
    A("| distinct content hashes (parsed systems) | %d |" % len(uniq))
    A("| duplicate hash groups | %d |" % len(dups))
    A("| ... of which cross-name (not just worktree mirrors) | %d |" % len(real_dups))
    A("| systems with excess <= 0 | %d (%d unique) |" % (len(nonpos), len({r['content_hash'] for r in nonpos})))
    A("| systems with torus rank > 0 | %d (%d unique) |" % (len(tors), len({r['content_hash'] for r in tors})))
    A("")
    A("**Redundancy**: %d files collapse to %d distinct systems -- a %.1fx duplication factor, "
      "almost all of it the four-way `canon`/`mailbox`/`p11`/`hunt` worktree mirror.\n"
      % (len(recs), len(byhash), len(recs) / max(1, len(byhash))))
    A("## 2. Cross-name duplicates (same mathematics, different file name)\n")
    if not real_dups: A("_none_\n")
    for d in real_dups[:40]:
        A("- `%s` (%d files, %d distinct names)" % (d["hash"][:16], d["n"],
          len({os.path.basename(p) for p in d["paths"]})))
        for p in sorted({os.path.basename(x) for x in d["paths"]})[:8]:
            A("    - %s" % p)
    A("")
    A("## 3. Systems with excess = n_eqs - n_vars <= 0 (an emptiness run there is vacuous)\n")
    if not nonpos: A("_none_\n")
    else:
        A("| system | n_vars | n_eqs | excess | char | files |")
        A("|---|---|---|---|---|---|")
        seen = set()
        for r in sorted(nonpos, key=lambda r: (r["excess"], r["n_vars"])):
            if r["content_hash"] in seen: continue
            seen.add(r["content_hash"])
            n = len(byhash[r["content_hash"]])
            A("| `%s` | %d | %d | %d | %s | %d |" % (lbl(r), r["n_vars"], r["n_eqs"],
              r["excess"], r.get("characteristic"), n))
    A("")
    A("## 4. Systems with grading torus rank > 0 (msolve solve mode cannot terminate; needs `-g 2` or a gauge)\n")
    if not tors: A("_none_\n")
    else:
        A("| system | rank | n_vars | n_eqs | excess | size_bytes | char | Rabinowitsch |")
        A("|---|---|---|---|---|---|---|---|")
        seen = set()
        for r in sorted(tors, key=lambda r: (-r["grading_torus_rank"], r["n_vars"])):
            if r["content_hash"] in seen: continue
            seen.add(r["content_hash"])
            A("| `%s` | %d | %d | %d | %d | %d | %s | %s |" % (lbl(r), r["grading_torus_rank"],
              r["n_vars"], r["n_eqs"], r["excess"], r["size_bytes"],
              r.get("characteristic"), r.get("has_rabinowitsch")))
    A("")
    A("## 5. The 20 smallest undecided systems with excess > 0\n")
    A("| # | system | n_vars | n_eqs | excess | torus | maxdeg | char | bytes |")
    A("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(undecided, 1):
        A("| %d | `%s` | %d | %d | %d | %s | %s | %s | %d |" % (i, lbl(r), r["n_vars"],
          r["n_eqs"], r["excess"], r.get("grading_torus_rank"), r.get("max_total_degree"),
          r.get("characteristic"), r["size_bytes"]))
    A("")
    A("## 6. Timeout shapes\n")
    A("| quantity | value |")
    A("|---|---|")
    A("| raw failure records in logs (after de-mirroring identical log files) | %d |" % json.load(open(os.path.join(OUT,'TIMEOUT_SHAPES.json')))["n_raw_records"])
    A("| deduplicated shapes (all failure kinds) | %d |" % len(shapes))
    A("| deduplicated shapes, TIMEOUT/OOM/KILLED only | %d |" % len(hard))
    A("| shapes resolvable to a registered system | %d |" % len([s for s in shapes if s["content_hash"]]))
    A("")
    A("Archive claims found, all mutually inconsistent and none enumerated:")
    A("")
    A("- `OPEN_ITEMS.md` / `wave6/CERTIFICATE_ROUTE.md`: **41** timeout shapes")
    A("- `AUDIT_EOD.md`: **33** virgin TIMEOUT shapes (+ a separate `(8,28) four`)")
    A("- `STATE_FULL.md`: **36** TIMEOUT")
    A("- `CATCHES.md`: **49** TIMEOUT records = **16** unique systems")
    A("")
    A("## 7. Parse failures\n")
    if not fails and not outs: A("_none_\n")
    for r in outs[:20]:
        A("- `%s` -- %s" % (lbl(r), r.get("parse_note")))
    for r in fails[:20]:
        A("- `%s` -- %s" % (lbl(r), r.get("parse_note")))
    open(os.path.join(OUT, "REGISTER_SUMMARY.md"), "w").write('\n'.join(L) + '\n')
    sys.stderr.write("REGISTER_SUMMARY.md written\n")
    return dups, real_dups, nonpos, tors, undecided, uniq

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'p2':
        summarise(*phase2())
    else:
        main()
