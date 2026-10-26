#!/bin/bash
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo
cd /home/user/physim/research/alife
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
PY=/home/user/labenv/bin/python
# wait for the seed-51 rerun already running
while pgrep -f "labkit.run .*rerun/seed51" >/dev/null; do sleep 5; done
echo "START rerun52 $(date +%T)"
( time $PY -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out $OUT/rerun/seed52 --seeds 52 --no-movie ) > $OUT/rerun/seed52.log 2>&1
echo "DONE rerun52 $(date +%T) rc=$?"
for s in 51 52; do
  echo "START walloff$s $(date +%T)"
  ( time $PY -m labkit.run $OUT/variants/active-nematic-cargo-walloff.py --out $OUT/controls/walloff_seed$s --seeds $s --no-movie ) > $OUT/controls/walloff_seed$s.log 2>&1
  echo "DONE walloff$s $(date +%T) rc=$?"
done
echo "START kappa0_51 $(date +%T)"
( time $PY -m labkit.run $OUT/variants/active-nematic-cargo-kappa0.py --out $OUT/controls/kappa0_seed51 --seeds 51 --no-movie ) > $OUT/controls/kappa0_seed51.log 2>&1
echo "DONE kappa0_51 $(date +%T) rc=$?"
echo "ALLDONE $(date +%T)"
