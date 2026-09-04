set -u
for s in wave4/w4_case2_selftest.py wave4/w4_gf.py wave4/w4_gf_Q.py wave4/w4_msformat.py \
         wave4/w4_edge_reconciliation.py wave4/w4_edge_eliminant_structure.py \
         wave4/w4_case2_json_audit.py wave4/w4_scan_ms_artifacts.py \
         pent/w5_pent_recursion_check.py pent/w5_pent_export_check.py \
         h2/w5_h2_controls.py h2/w5_h2_target_provenance.py h2/w5_h2_polygon_consistency.py \
         h2/w5_h2_changelog.py gghv_audit/w5_gghv_certifier.py gghv_audit/w5_pairs_105_124.py \
         lift/lift_pipeline.py ; do
  echo "=== $s"
  d=$(dirname $s); b=$(basename $s)
  (cd $d && timeout 900 python3 $b > /tmp/reg_$b.log 2>&1; echo "exit=$?")
  grep -E "^\s+\[(PASS|FAIL)\]|checks passed|/[0-9]+ (checks|controls)" /tmp/reg_$b.log | tail -4
  grep -c "\[FAIL\]" /tmp/reg_$b.log | sed 's/^/  FAILS: /'
done
