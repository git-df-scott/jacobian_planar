# Group-first screen.  For each transitive group T of degree D and conjugacy class C of
# meridian candidates (>=1 fixed point, >=1 moved point), compute achievable (s, o) at a
# (2,k)-cusp (pairs a,b in C with the k-braid relation) and at a node (commuting pairs),
# then look for singularity multisets (cusps k_i, nu nodes) of an irreducible S with
# Euler = 1 and chi(R) >= 1.
SizeScreen([4000,]);;
braidrel := function(a, b, k)   # (ab)^((k-1)/2) a = (ba)^((k-1)/2) b  for k odd
  local w1, w2, i;
  w1 := a^0; w2 := a^0;
  for i in [1..(k-1)/2] do w1 := w1*a*b; w2 := w2*b*a; od;
  return w1*a = w2*b;
end;;
so := function(a, b, D)
  local H;
  H := Group(a, b);
  return [D - NrMovedPoints(H), Length(Filtered(Orbits(H, [1..D]), o -> Length(o) > 1))];
end;;
found := [];;
for D in [4..10] do
  for T in AllTransitiveGroups(NrMovedPoints, D) do
    for C in ConjugacyClasses(T) do
      a := Representative(C);
      n := D - NrMovedPoints(a); e := D - n;
      if n < 1 or e < 1 then continue; fi;
      if not IsTransitive(Group(AsList(C)), [1..D]) then continue; fi;   # meridians must generate
      cyc := Length(Filtered(Cycles(a, [1..D]), c -> Length(c) > 1));
      cusp := rec();
      for k in [3, 5, 7] do
        cusp.(k) := Set(List(Filtered(AsList(C), b -> b <> a and braidrel(a, b, k)), b -> so(a, b, D)));
      od;
      node := Set(List(Filtered(AsList(C), b -> b <> a and a*b = b*a), b -> so(a, b, D)));
      if node = [] then continue; fi;
      # multisets: cusps from {3,5,7} up to 3, nodes 1..3
      for nc in [1..3] do
        for ks in UnorderedTuples([3, 5, 7], nc) do
          opts := List(ks, k -> cusp.(k));
          if ForAny(opts, o -> o = []) then continue; fi;
          for nu in [1..3] do
            kS := nc + 2*nu;
            need := 1 - D*nu - n*(1 - kS);
            baseR := cyc * (1 - kS);
            for ch in Cartesian(Concatenation(opts, List([1..nu], i -> node))) do
              ssum := Sum(ch, x -> x[1]); osum := Sum(ch, x -> x[2]);
              if ssum = need and baseR + osum >= 1 then
                Add(found, rec(D := D, T := StructureDescription(T), cyc := CycleStructurePerm(a), n := n, cusps := ks, nodes := nu, s := List(ch, x -> x[1]), chiR := baseR + osum));
              fi;
            od;
          od;
        od;
      od;
    od;
  od;
  Print("D=", D, " done, found so far ", Length(found), "\n");
od;
seen := [];;
for f in found do
  key := [f.D, f.T, f.cyc, f.cusps, f.nodes];
  if key in seen then continue; fi;
  Add(seen, key);
  Print(f.D, " ", f.T, " cyc=", f.cyc, " n=", f.n, " cusps=", f.cusps, " nodes=", f.nodes, " s=", f.s, " chiR=", f.chiR, "\n");
od;
QUIT;
