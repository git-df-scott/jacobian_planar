import sys
import uz_ext_run as R
m = int(sys.argv[1])
base = {('q%d' % a): 0 for a in range(m+1, 9)}
base['q%d' % m] = 1
print(f"=== deg q = {m} branch (a_14_8 = 0, outside subcase 2)")
R.main('bq%d.out' % m, base=base, tagpfx='br%d' % m)
