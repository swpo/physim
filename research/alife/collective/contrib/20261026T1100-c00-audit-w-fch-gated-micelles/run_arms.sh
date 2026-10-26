#!/bin/bash
# Runs the audit arms one at a time (claim settings: 100 frames, 128x128, spf 200).
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/fch-gated-micelles
CLAIM=collective/contrib/20261025T0816-c03-fch-gated-micelles/world.py
cd /home/user/physim/research/alife
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
run() { # world outdir seed
  t0=$(date +%s)
  /home/user/labenv/bin/python -B -m labkit.run "$1" --out "$2" --seeds "$3" --frames 100 --no-movie > "$2.log" 2>&1
  echo "$(basename $2) exit $? wall $(( $(date +%s) - t0 ))s" >> $OUT/runs.log
}
for job in "$@"; do
  case $job in
    rerun51) run $CLAIM $OUT/rerun/seed51 51;;
    rerun52) run $CLAIM $OUT/rerun/seed52 52;;
    walloff51) run $OUT/variants/walloff.py $OUT/controls/walloff_seed51 51;;
    walloff52) run $OUT/variants/walloff.py $OUT/controls/walloff_seed52 52;;
    homgate51) run $OUT/variants/homgate.py $OUT/controls/homgate_seed51 51;;
    betaoff51) run $OUT/variants/betaoff.py $OUT/controls/betaoff_seed51 51;;
    *) w=$(echo $job | sed 's/_seed.*//'); s=$(echo $job | sed 's/.*_seed//'); run $OUT/variants/$w.py $OUT/controls/${w}_seed$s $s;;
  esac
done
