#!/usr/bin/env python
import subprocess, json, sys, time, itertools, os

SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, 'cells.jsonl')

def main():
    D = int(sys.argv[1]); tmo = int(sys.argv[2]); deadline = time.time() + int(sys.argv[3])
    pairs = [(2,1),(2,-1),(3,1),(3,-1),(4,1),(4,-1),(6,1),(6,-1),
             (2,3),(2,-3),(3,2),(3,-2),(4,3),(4,-3),(6,5),(4,2),(6,2),(6,3),(6,4),(2,-2),(3,3)]
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try:
                r = json.loads(line); done.add((r['n'],r['b'],r['p'],r['D']))
            except: pass
    with open(OUT,'a') as f:
        for n,b in pairs:
            for p in range(n):
                if time.time() > deadline:
                    print('DEADLINE'); return
                key = (n,b,p,D)
                if key in done: continue
                try:
                    cp = subprocess.run(['python', os.path.join(SP,'sweep.py'),
                                         str(n),str(b),str(p),str(D)],
                                        capture_output=True, text=True, timeout=tmo)
                    if cp.returncode==0 and cp.stdout.strip():
                        f.write(cp.stdout.strip()+'\n'); f.flush()
                        print(cp.stdout.strip()[:160])
                    else:
                        r = dict(n=n,b=b,p=p,D=D,status='error:'+cp.stderr[-120:])
                        f.write(json.dumps(r)+'\n'); f.flush(); print(r)
                except subprocess.TimeoutExpired:
                    r = dict(n=n,b=b,p=p,D=D,status='timeout')
                    f.write(json.dumps(r)+'\n'); f.flush(); print(r)

main()
