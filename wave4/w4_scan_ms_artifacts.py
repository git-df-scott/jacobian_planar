"""Run the msolve-input validator (w4_msformat.validate) over every .ms file
in the tree, including the campaign's own, and print the ones with hazards."""
import sys, glob, os
sys.path.insert(0,'/home/user/jacobian_planar/wave4')
import w4_msformat as F
tot=0
for pat in ('wave4/artifacts/*.ms','symslice/artifacts/*.ms','wave0/*.ms','wave1/*.ms'):
    for f in sorted(glob.glob('/home/user/jacobian_planar/'+pat)):
        try:
            probs=F.validate(f)
        except Exception as e:
            probs=[(-1,f'validator error: {e}')]
        if probs:
            tot+=1
            kinds=set(m.split('(')[0].strip() for _,m in probs)
            print(f"{os.path.relpath(f,'/home/user/jacobian_planar')}: {len(probs)} problems; kinds={sorted(kinds)[:3]}")
print('files with problems:',tot)
