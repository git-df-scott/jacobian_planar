import ast, glob, sys
# A check condition is CONSTANT if its AST contains no Name/Attribute/Call/Subscript/
# Comprehension nodes -- i.e. it is fully determined at parse time.
DYN = (ast.Name, ast.Call, ast.Attribute, ast.Subscript, ast.ListComp, ast.SetComp,
       ast.GeneratorExp, ast.DictComp, ast.Starred, ast.Await, ast.Lambda)
def is_const(node):
    for n in ast.walk(node):
        if isinstance(n, DYN): return False
    return True
def truth(node):
    try:
        return bool(eval(compile(ast.Expression(node), '<c>', 'eval'), {'__builtins__':{}}, {}))
    except Exception:
        return None
tot=0; hits=[]
for f in sorted(glob.glob('wave3/*.py')+glob.glob('certifiers/new/*.py')):
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
           and node.func.id in ('chk','check','rec') and len(node.args)>=2:
            tot+=1
            cond = node.args[1]
            if is_const(cond):
                hits.append((f,node.lineno,truth(cond),ast.unparse(cond)[:70],ast.unparse(node.args[0])[:80]))
            elif isinstance(cond, ast.IfExp) or (isinstance(cond,ast.Compare) and
                 any(isinstance(x,ast.Constant) for x in [cond.left]+list(cond.comparators))
                 and len([c for c in ast.walk(cond) if isinstance(c,DYN)])==0):
                hits.append((f,node.lineno,'?',ast.unparse(cond)[:70],ast.unparse(node.args[0])[:80]))
print("total check() calls scanned:", tot)
print("CONSTANT (parse-time-determined) conditions:", len(hits))
for h in hits: print("  %s:%d  value=%s  cond= %s\n        label= %s" % h)
