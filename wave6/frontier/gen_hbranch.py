import sys, subprocess, os
sys.path.insert(0,'/home/user/jacobian_planar/campaign/moduli_phase2/phase2_moduli/certify')
import importlib.util
spec=importlib.util.spec_from_file_location("s35",
  "/home/user/jacobian_planar/campaign/moduli_phase2/phase2_moduli/certify/session35_singular_modular_push.py")
# load only the code-builder without executing the session body
src=open(spec.origin).read()
ns={}
exec(src[src.index("def hbranch_code"):src.index("def slice3n_code")], ns)
K,hs,D,p = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
code=ns['hbranch_code'](K,hs,D,p)
# replace the slimgb call with a DUMP of the ideal generators
code=code.replace('ideal G = slimgb(E);\n"NEQS ", size(E);\n"DIMG ", dim(G);\n"UNIT ", (G[1]==1);',
                  '"NEQS ", size(E);\nint q; for(q=1;q<=size(E);q++){ "GEN", E[q]; }')
if 'GEN' not in code:
    code=code.replace('ideal G = slimgb(E);','int q; "NEQS ", size(E); for(q=1;q<=size(E);q++){ "GEN", E[q]; }')
    for junk in ['"NEQS ", size(E);\n','"DIMG ", dim(G);\n','"UNIT ", (G[1]==1);\n']:
        code=code.replace(junk,'',1)
open(sys.argv[5],'w').write(code)
print(f"built generator script for K={K} h={hs} D={D} p={p}")
