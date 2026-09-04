# Dicritical test (Orevkov): every component of the escaping curve R is a copy of C,
# unramified over the smooth part of S.  Nodes = (strand j, escaping cycle C of the
# meridian of j); loop k moves (j, C) to (j', w^-1(C)).  Components of R are the
# orbits; each must have chi = d(1 - k_i), exactly 1 - Nsing punctures at singular
# points (so chi + Nsing = 1), be unibranch there, and have one place at infinity.
DicriticalTest := function(hom, D, compofgen, m, kk, longitudes, fibres)
  local alpha, i, j, jj, w, C, C2, cyc, nodes, parent, find, union, k, x, y, moves, comps, O, d, Nsing, ok, res, cl, Lp, orbs, b, hit, lb, s, infmove, cnt, allres, fails, gensG;
  gensG := GeneratorsOfGroup(Source(hom));
  alpha := List([1..m], i -> Length(Filtered(compofgen, c -> c = i)));
  cyc := List([1..Length(compofgen)], j -> List(Filtered(Cycles(Image(hom, gensG[j]), [1..D]), c -> Length(c) > 1), Set));
  nodes := [];
  for j in [1..Length(compofgen)] do for C in cyc[j] do Add(nodes, [j, C]); od; od;
  if nodes = [] then return rec(fails := ["no escaping sheets"], comps := []); fi;
  parent := [1..Length(nodes)];
  find := function(x) while parent[x] <> x do x := parent[x]; od; return x; end;
  union := function(x, y) parent[find(x)] := find(y); end;
  moves := [];
  for k in [1..Length(longitudes)] do
    moves[k] := [];
    for x in [1..Length(nodes)] do
      j := nodes[x][1]; C := nodes[x][2];
      if longitudes[k][j] = fail then return rec(fails := ["longitude undefined"], comps := []); fi;
      jj := longitudes[k][j].to; w := Image(hom, longitudes[k][j].w);
      C2 := OnSets(C, w^-1);
      y := Position(nodes, [jj, C2]);
      if y = fail then C2 := OnSets(C, w); y := Position(nodes, [jj, C2]); fi;
      if y = fail then return rec(fails := ["transport is not a cycle"], comps := []); fi;
      moves[k][x] := y; union(x, y);
    od;
  od;
  comps := Set(List([1..Length(nodes)], find));
  allres := []; fails := [];
  for O in comps do
    O := Filtered([1..Length(nodes)], x -> find(x) = O);
    i := compofgen[nodes[O[1]][1]];
    d := Length(O) / alpha[i];
    res := rec(comp := i, d := d);
    if not IsInt(d) then Add(fails, "d"); Add(allres, res); continue; fi;
    Nsing := 0; ok := true;
    for k in [1..Length(fibres)] do
      for cl in Filtered(fibres[k], c -> c.singular) do
        Lp := Group(List(cl.mer, x -> Image(hom, x)));
        orbs := Filtered(Orbits(Lp, [1..D]), o -> Length(o) > 1);
        for b in orbs do
          hit := Filtered(O, x -> (nodes[x][1] - 1) in cl.positions and IsSubset(b, nodes[x][2]));
          if hit = [] then continue; fi;
          Nsing := Nsing + 1;
          lb := 0; s := Set(hit);
          while s <> [] do
            lb := lb + 1; x := s[1]; y := x;
            repeat RemoveSet(s, y); y := moves[k][y]; until not y in s;
          od;
          if lb > 1 then ok := false; fi;
        od;
      od;
    od;
    infmove := [1..Length(nodes)];
    for k in [1..Length(moves)] do infmove := List(infmove, x -> moves[k][x]); od;
    cnt := 0; s := Set(O);
    while s <> [] do cnt := cnt + 1; x := s[1]; y := x; repeat RemoveSet(s, y); y := infmove[y]; until not y in s; od;
    res.Nsing := Nsing; res.unibranch := ok; res.places_inf := cnt; res.chi := d * (1 - kk[i]);
    res.line := ok and cnt = 1 and res.chi + Nsing = 1;
    if not res.line then Add(fails, res); fi;
    Add(allres, res);
  od;
  return rec(fails := fails, comps := allres);
end;;
