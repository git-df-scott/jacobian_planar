#!/usr/bin/env python3
"""Build/check the separate September 5 supplement; never alter frozen catalogs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PARENT = '5206d825b1e4baf6524b7af0febad58d9f1af4f5'
ARCHIVE = 'efff2dc5c31a71030ccf931d22b9cd2047c0e172'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()

def build():
    paths = set()
    for n in range(4, 13):
        paths.update(ROOT.glob(f'ASTRA_{n}_*.md'))
        paths.update(p for p in (ROOT / f'astra{n}').rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    for name in ['JC2_COMPLETE_RECORD.md', 'README.md', 'ASTRA_STATE.md',
                 'ASTRA_HANDOFF.md', 'ASTRA_RUN_LOG.md', 'GRADED_FRONTIER.md',
                 'RECORD_CORRECTIONS.md', 'record/README.md', 'record/build_continuation.py']:
        paths.add(ROOT / name)
    rows = []
    for p in sorted(paths):
        b = p.read_bytes()
        blob = hashlib.sha1(f'blob {len(b)}\0'.encode() + b).hexdigest()
        rows.append({'path': p.relative_to(ROOT).as_posix(), 'bytes': len(b),
                     'sha256': hashlib.sha256(b).hexdigest(), 'git_blob_sha1': blob})
    commits = []
    for sha in git('rev-list', '--reverse', f'{ARCHIVE}..{PARENT}').splitlines():
        commits.append({'sha': sha, 'subject': git('show', '-s', '--format=%s', sha),
                        'tree': git('show', '-s', '--format=%T', sha)})
    data = {'scope': 'September 5 continuation through Astra 12; separate from frozen September 4 inventory',
            'archive_branch_parent': ARCHIVE, 'research_parent_before_closeout': PARENT,
            'closeout_commit': 'The commit containing this manifest; deliberately not self-referenced by SHA.',
            'inventory_policy': 'All Astra 4–12 report and directory files, plus listed canonical reports. Excludes generated manifest/index themselves and Python caches. Git blob SHA is calculated from current bytes, including newly added files.',
            'prior_continuation_commits': commits, 'file_count': len(rows), 'files': rows}
    out = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    md = '''# September 5 continuation — complete artifact index

This supplement covers Astra 4–12 and the consolidated campaign documents.
The September 4 branch/file/commit catalogs remain frozen and unchanged.
For results, scope, corrections, and unresolved equations, read
[the full report](../JC2_COMPLETE_RECORD.md). No counterexample was found.

The commit containing this index adds Astra 12 and the mass-report closeout
after the research parent below. The prior continuation commits are listed
separately; the new commit cannot contain its own hash. File hashes cover
current bytes, including new artifacts. The generated index and JSON manifest
exclude themselves to avoid self-referential checksums.

Rebuild: `python record/build_continuation.py`.
Check: `python record/build_continuation.py --check`.
These commands check inventory integrity, not mathematical proofs.

## Prior September 5 research commits

| Commit | Subject |
|---|---|
'''
    for c in commits:
        md += f"| [{c['sha'][:12]}](https://github.com/git-df-scott/jacobian_planar/commit/{c['sha']}) | {c['subject']} |\n"
    md += f'\n## Artifact inventory — {len(rows)} files\n\n'
    md += 'Full SHA-256 and Git blob hashes are in [CONTINUATION_FILES.json](CONTINUATION_FILES.json).\n\n| File | Bytes | SHA-256 prefix |\n|---|---:|---|\n'
    for r in rows:
        md += f"| [{r['path']}](../{r['path']}) | {r['bytes']} | `{r['sha256'][:16]}` |\n"
    return {'record/CONTINUATION_FILES.json': out, 'record/CONTINUATION_INDEX.md': md}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for name, text in build().items():
        p = ROOT / name
        if args.check:
            assert p.read_text() == text, f'Stale inventory: {name}'
        else:
            p.write_text(text)
    print('PASS continuation inventory' if args.check else 'Wrote continuation inventory')
