#!/bin/bash
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo
cd /home/user/physim/research/alife
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
until grep -q ALLDONE $OUT/queue.log 2>/dev/null; do sleep 10; done
echo "START res15_51 $(date +%T)"
( time WORLD_P='{"dx": 0.6666667, "noise_area": true}' /home/user/labenv/bin/python -m labkit.run collective/contrib/20261026T0405-c34-nematic-cargo/world.py --out $OUT/controls/res15_seed51 --seeds 51 --size 192 192 --frames 120 --no-movie ) > $OUT/controls/res15_seed51.log 2>&1
echo "DONE res15_51 $(date +%T)"
