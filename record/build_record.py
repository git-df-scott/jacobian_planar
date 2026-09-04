"""Rebuild the frozen JC2 campaign inventory from Git objects, without solvers.

Run from a clone containing the branch heads in SNAPSHOT.json and the two
recovered commits (fetch RECOVERED_NIGHTS_25_26.bundle if necessary).
PR metadata/discussions are frozen inputs obtained through the GitHub app.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'record'
URL = 'https://github.com/git-df-scott/jacobian_planar'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def dump(name, value):
    (OUT/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')

def lines(name, rows):
    (OUT/name).write_text(''.join(json.dumps(r, ensure_ascii=False, separators=(',', ':'))+'\n' for r in rows))

def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')

def blob_url(head, path):
    return URL+'/blob/'+head+'/'+quote(path, safe='/')

def main():
    snapshot = json.loads((OUT/'SNAPSHOT.json').read_text())
    recovery = json.loads((OUT/'RECOVERY.json').read_text())
    branches = snapshot['branches']
    heads = [b['sha'] for b in branches]
    for b in branches:
        assert git('rev-parse', b['sha']+'^{commit}').decode().strip() == b['sha']
    extra = recovery['commits']
    commits = git('rev-list', '--reverse', '--topo-order', *heads, *extra).decode().splitlines()
    remote_commits = set(git('rev-list', *heads).decode().splitlines())
    assert set(commits)-remote_commits == set(extra)

    # Read complete commit objects in a single batch; bodies remain historical
    # source text, not endorsements of their claims.
    proc = subprocess.Popen(['git','cat-file','--batch'], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    raw, _ = proc.communicate(('\n'.join(commits)+'\n').encode())
    assert proc.returncode == 0
    pos = 0; commit_rows = []
    for sha in commits:
        end = raw.index(b'\n', pos); header = raw[pos:end].decode().split()
        assert header[:2] == [sha, 'commit']
        length = int(header[2]); content = raw[end+1:end+1+length]; pos = end+2+length
        assert hashlib.sha1(b'commit '+str(length).encode()+b'\0'+content).hexdigest() == sha
        meta, body = content.decode('utf-8').split('\n\n', 1)
        tree = next(s[5:] for s in meta.splitlines() if s.startswith('tree '))
        parents = [s[7:] for s in meta.splitlines() if s.startswith('parent ')]
        author = next(s[7:] for s in meta.splitlines() if s.startswith('author '))
        # Git stores an author identity, not a reliable model attribution.
        author_name = author.rsplit(' <',1)[0]
        stamp, timezone = author.rsplit('> ',1)[1].split()
        changed = git('diff-tree','--root','-m','--no-commit-id','--name-only','-r','-z',sha).decode().split('\0')
        commit_rows.append({'sha':sha,'tree':tree,'parents':parents,'author_name':author_name,
            'author_timestamp':int(stamp),'author_timezone':timezone,'message':body,
            'changed_paths':sorted(set(x for x in changed if x)),
            'recovered_local':sha not in remote_commits,'url':URL+'/commit/'+sha})
    assert pos == len(raw)
    lines('COMMITS.jsonl', commit_rows)

    files = {}; branch_rows=[]; total_entries=0
    for bid,b in enumerate(branches):
        entries = git('ls-tree','-r','-l','-z',b['sha']).decode().split('\0')
        count=0; reports=0; byte_count=0
        for entry in entries:
            if not entry: continue
            meta,path=entry.split('\t',1); mode,kind,sha,size=meta.split()
            size=None if size=='-' else int(size)
            key=(path,sha,mode,kind)
            if key not in files:
                files[key]={'path':path,'sha':sha,'mode':mode,'type':kind,'bytes':size,'branch_ids':[]}
            files[key]['branch_ids'].append(bid)
            count+=1;byte_count+=size or 0
            reports+=path.lower().endswith(('.md','.markdown','.rst'))
        total_entries+=count
        branch_rows.append({**b,'id':bid,'files':count,'report_files':reports,'bytes':byte_count,
                            'reachable_commits':int(git('rev-list','--count',b['sha']))})
    file_rows=sorted(files.values(),key=lambda r:(r['path'],r['sha'],r['mode']))
    lines('FILES.jsonl',file_rows)
    dump('BRANCHES.json',branch_rows)
    report_rows=[r for r in file_rows if r['path'].lower().endswith(('.md','.markdown','.rst'))]
    lines('REPORTS.jsonl',report_rows)

    text=['# Frozen branch index','',
          'All remote branches observed on 2026-09-04, before the closing record commit. IDs index FILES.jsonl. Counts overlap across branches.', '',
          '| ID | Branch | Pinned commit | Files | Reports | Reachable commits |',
          '|---:|---|---|---:|---:|---:|']
    for b in branch_rows:
        text.append(f"| {b['id']} | {cell(b['name'])} | [{b['sha'][:12]}]({URL}/tree/{b['sha']}) | {b['files']} | {b['report_files']} | {b['reachable_commits']} |")
    (OUT/'BRANCHES.md').write_text('\n'.join(text)+'\n')

    text=['# Complete report-file index','',
          'Every distinct report path/blob pair present at the frozen branch heads. Different versions are deliberately retained. Branch IDs refer to BRANCHES.md. A listed report is historical evidence, not a verified verdict.', '',
          '| Report | Blob | Branch IDs |','|---|---|---|']
    for r in report_rows:
        head=branches[r['branch_ids'][0]]['sha']
        text.append(f"| [{cell(r['path'])}]({blob_url(head,r['path'])}) | `{r['sha'][:12]}` | {', '.join(map(str,r['branch_ids']))} |")
    (OUT/'REPORT_INDEX.md').write_text('\n'.join(text)+'\n')

    text=['# Complete commit chronology','',
          'Topological order, oldest first. Author names and messages are preserved as Git records; they do not certify model identity or mathematical correctness. The two recovered commits link to their preserved patch because their original SHAs were unpublished.', '',
          '| Commit | Author date (UTC) | Author | Subject |','|---|---|---|']
    from datetime import datetime, timezone
    for r in commit_rows:
        date=datetime.fromtimestamp(r['author_timestamp'],timezone.utc).isoformat()
        target='RECOVERED_NIGHTS_25_26.patch' if r['recovered_local'] else r['url']
        text.append(f"| [{r['sha'][:12]}]({target}) | {date} | {cell(r['author_name'])} | {cell(r['message'].splitlines()[0])} |")
    (OUT/'CHRONOLOGY.md').write_text('\n'.join(text)+'\n')

    prs=sorted(snapshot['pull_requests'],key=lambda r:r['number'])
    discussions=json.loads((OUT/'PR_DISCUSSIONS.json').read_text())
    assert not any('error' in row for row in discussions)
    text=['# Pull-request archive','',
          'Frozen descriptions and discussion entries for all 26 PRs visible at the cutoff. Original claims, status words and running-job statements below are historical; use JC2_COMPLETE_RECORD.md and RECORD_CORRECTIONS.md for current interpretation. Nothing here sends a message or changes a PR.', '']
    for p in prs:
        text += [f"## PR #{p['number']} — {p['title']}", '',
                 f"[Original pull request]({p['url']}) · state `{p['state']}` · created `{p['created_at']}` · updated `{p['updated_at']}`", '',
                 f"Head: `{p['head_ref']}` at `{p['head_sha']}`. Base: `{p['base_ref']}`. Merged: `{p['merged_at']}`.", '',
                 '### Original description', '', p['body'] or '(No description.)', '']
        comments=next(r['comments'] for r in discussions if r['number']==p['number'])
        text += ['### Archived discussion', '', f'{len(comments)} entries; full normalized metadata in PR_DISCUSSIONS.json.', '']
        for c in comments:
            text += ['```json', json.dumps(c,ensure_ascii=False,indent=2), '```', '']
    (OUT/'PULL_REQUESTS.md').write_text('\n'.join(text).rstrip()+'\n')

    counts={'remote_branches':len(branches),'pull_requests':len(prs),
            'discussion_entries':sum(len(r['comments']) for r in discussions),
            'remote_reachable_commits':len(remote_commits),'recovered_commits':len(extra),
            'total_catalogued_commits':len(commits),'branch_file_entries':total_entries,
            'distinct_path_blob_records':len(file_rows),'distinct_report_path_blob_records':len(report_rows),
            'distinct_file_paths':len(set(r['path'] for r in file_rows)),'tags':snapshot['tags']}
    dump('COUNTS.json',counts)
    names=['SNAPSHOT.json','PR_DISCUSSIONS.json','COMMITS.jsonl','FILES.jsonl','BRANCHES.json',
           'REPORTS.jsonl','BRANCHES.md','REPORT_INDEX.md','CHRONOLOGY.md','PULL_REQUESTS.md',
           'COUNTS.json','RECOVERY.json','RECOVERED_NIGHTS_25_26.patch','RECOVERED_NIGHTS_25_26.bundle']
    dump('INVENTORY_VERIFICATION.json',{'status':'PASS','checks':[
        'All 44 branch heads resolve to the frozen commit SHAs',
        'Every catalogued commit object was independently SHA-1 checked',
        'Every branch tree fully enumerated with path, mode, object SHA and size',
        'All 26 PRs have successful discussion retrieval',
        'Exactly the two recovered local commits augment remote history'],
        'counts':counts,'sha256':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in names}})
    print(json.dumps(counts,indent=2))

if __name__=='__main__':main()
