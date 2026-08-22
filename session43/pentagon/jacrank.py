import sys, random
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p

def interp_linear_coeff(f_at, npts):
    """Given f(0..npts-1) over F_p for a poly of deg<npts, return coeff of t^1."""
    # Newton divided differences -> expand to power basis
    xs=list(range(npts)); ys=f_at[:]
    coef=ys[:]
    for j in range(1,npts):
        for i in range(npts-1,j-1,-1):
            coef[i]=(coef[i]-coef[i-1])*pow(xs[i]-xs[i-j],p-2,p)%p
    # expand newton form  sum coef[k] * prod_{i<k}(t-xs[i])  -> power basis, need t^1
    poly=[0]*(npts+1); poly[0]=1; res=[0]*(npts+1)
    cur=[1]+[0]*npts   # product polynomial
    for k in range(npts):
        for d in range(npts+1):
            res[d]=(res[d]+coef[k]*cur[d])%p
        # cur *= (t - xs[k])
        new=[0]*(npts+1)
        for d in range(npts):
            new[d+1]=(new[d+1]+cur[d])%p
            new[d]=(new[d]-cur[d]*xs[k])%p
        cur=new
    return res[1]

def jacobian(base, npts=11):
    b=conditions(base)
    J=[]
    for v in VARS:
        col=[]
        vals=[]
        for t in range(npts):
            d=dict(base); d[v]=(base[v]+t)%p
            vals.append(conditions(d))
        for c in range(66):
            col.append(interp_linear_coeff([vals[t][c] for t in range(npts)],npts))
        J.append(col)
    return [[J[vi][c] for vi in range(len(VARS))] for c in range(66)], b

def rank(rows,ncols):
    rows=[r[:] for r in rows]; r=0; piv=[]
    for c in range(ncols):
        sel=next((i for i in range(r,len(rows)) if rows[i][c]%p),None)
        if sel is None: continue
        rows[r],rows[sel]=rows[sel],rows[r]
        inv=pow(rows[r][c],p-2,p)
        rows[r]=[(x*inv)%p for x in rows[r]]
        for i in range(len(rows)):
            if i!=r and rows[i][c]%p:
                f=rows[i][c]
                rows[i]=[(rows[i][j]-f*rows[r][j])%p for j in range(len(rows[i]))]
        piv.append(c); r+=1
        if r==len(rows): break
    return r

for seed in (2,9):
    rnd=random.Random(seed)
    base={v:rnd.randrange(p) for v in VARS}
    J,b=jacobian(base)
    r=rank(J,len(VARS))
    # also rank of [J | F] : tells whether F is in the column span of the differentials
    aug=[J[c]+[b[c]] for c in range(66)]
    ra=rank(aug,len(VARS)+1)
    print(f"seed {seed}: rank(Jacobian 66x59) = {r} ; rank([J|F]) = {ra}")
