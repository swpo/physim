#!/bin/sh
# One frozen truth member per bundle, re-simulated through the bundle's own oracle (one process at a time).
B=/home/user/evalwork/bundles
PY=/home/user/physim/.venv/bin/python
export OMP_NUM_THREADS=1
for pair in pm_main:c015 pm_formation:c006 vortex_main:c013 cips_main:c011 vortex_formation:c002 rods_main:c016 cips_formation:c002 rods_formation:c002; do
  k=${pair%%:*}; c=${pair#*:}
  [ -f $B/reports/verify_$k.json ] && continue
  $PY $B/scripts/gc_bundle.py verify --bundle $B/$k --case $c --out $B/reports/verify_$k.json || echo "FAIL $k"
done
