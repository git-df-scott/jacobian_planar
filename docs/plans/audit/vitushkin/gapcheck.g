CosetTableDefaultMaxLimit := 2000000;;
CheckCurve := function(G, singpts, compofgen, degs, m, Dmin, Dmax)
  local iso, Hfp, rr, Q, sz, L, H, D, hom, img, gi, gens, n, e, sp, s, sums, ok, Ltot, lst, results, k, nu, res, N, r, c, cnt, i, staylifts, idx, alpha, beta, fibre1, fibre2, kk, allbr;
  results := [];
  gens := [];   # one generator per component
  for i in [1..m] do Add(gens, GeneratorsOfGroup(G)[Position(compofgen, i)]); od;
  # k_i = branches of component i over singular points; nu = sum (r_p - 1)
  kk := List([1..m], i -> 0);
  nu := 0;
  for sp in singpts do
    nu := nu + sp.branches - 1;
    for c in sp.comps do kk[c] := kk[c] + 1; od;
  od;
  L := LowIndexSubgroupsFpGroup(G, Dmax);
  cnt := 0;
  for H in L do
    D := Index(G, H);
    if D < Dmin then continue; fi;
    hom := FactorCosetAction(G, H);
    img := Image(hom);
    if not IsTransitive(img, [1..D]) then continue; fi;
    cnt := cnt + 1;
    n := List(gens, g -> D - NrMovedPoints(Image(hom, g)));
    e := List(n, x -> D - x);
    res := rec(D := D, n := n, e := e, cycles := List(gens, g -> CycleStructurePerm(Image(hom, g))), group := StructureDescription(img));
    ok := true;
    if Minimum(n) < 1 then ok := false; res.fail := "n=0"; fi;
    fibre1 := D - Sum([1..m], i -> degs[i][1] * e[i]);
    fibre2 := D - Sum([1..m], i -> degs[i][2] * e[i]);
    res.chi := [fibre1, fibre2];
    if ok and (fibre1 > -1 or fibre2 > -1) then ok := false; res.fail := "fibre chi"; fi;
    if ok then
      sums := 0; lst := [];
      for sp in singpts do
        Ltot := Group(List(sp.mer, x -> Image(hom, x)));
        s := D - NrMovedPoints(Ltot);
        Add(lst, s); sums := sums + s;
      od;
      res.s := lst;
      res.euler := D*(1 - m + nu) + Sum([1..m], i -> n[i]*(1 - kk[i])) + sums;
      if res.euler <> 1 then ok := false; res.fail := "euler"; fi;
    fi;
    if ok then
      staylifts := [];
      for r in RightTransversal(G, H) do
        for i in [1..m] do
          c := r^-1 * gens[i] * r;
          if Image(hom, c) = Image(hom, c)^0 or 1^Image(hom, c) = 1 then Add(staylifts, c); fi;
        od;
      od;
      # H as fp group; quotient by normal closure of staying lifts
      iso := IsomorphismFpGroup(H);
      Hfp := Range(iso);
      rr := List(staylifts, x -> UnderlyingElement(Image(iso, x)));
      Q := FactorGroupFpGroupByRels(Hfp, rr);
      res.pi1_ab := AbelianInvariants(Q);
      if res.pi1_ab <> [] then
        ok := false; res.fail := "pi1(H1)";
      else
        sz := CALL_WITH_CATCH(Size, [Q]);
        if sz[1] = true then
          res.pi1_size := sz[2];
          if sz[2] <> 1 then ok := false; res.fail := "pi1"; fi;
        else
          res.pi1_size := "unknown";
        fi;
      fi;
    fi;
    res.ok := ok;
    Add(results, res);
  od;
  return rec(count := cnt, results := results, k := kk, nu := nu);
end;;

Report := function(r)
  local x, near;
  Print("k=", r.k, " nu=", r.nu, " transitive reps: ", r.count, "\n");
  for x in r.results do
    if x.ok then Print("*** SURVIVOR: ", x, "\n"); fi;
  od;
  near := Filtered(r.results, x -> not x.ok and x.fail <> "n=0");
  for x in near do
    Print("   D=", x.D, " n=", x.n, " cyc=", x.cycles, " ", x.group, " chi=", x.chi, " fail=", x.fail);
    if IsBound(x.s) then Print(" s=", x.s, " euler=", x.euler); fi;
    if IsBound(x.pi1_ab) then Print(" pi1ab=", x.pi1_ab); fi; if IsBound(x.pi1_size) then Print(" pi1size=", x.pi1_size); fi;
    Print("\n");
  od;
  Print("   (", Length(Filtered(r.results, x -> not x.ok and x.fail = "n=0")), " reps with a meridian acting freely)\n");
end;;
