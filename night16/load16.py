"""night16 -- load the 57 PERIODS-VANISHING survivors from night15 (read-only)."""
import json, os
from fractions import Fraction as Fr

N15 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night15')


def survivors():
    recs = json.load(open(os.path.join(N15, 'screen15_records.json')))
    return [r for r in recs if r['period_verdict'] == 'VANISHING']


def Pdict(rec):
    out = {}
    for k, v in rec['P'].items():
        i, j = (int(t) for t in k.split(','))
        out[(i, j)] = Fr(int(v[0]), int(v[1]))
    return out
