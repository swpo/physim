#!/bin/bash
# usage: run.sh NAME SEED FRAMES WRAP_JSON_EXTRA   (WORLD_P CARGO=0; flow dump to runs/NAME/seedS/flow.npz)
O=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/paperexp/marangoni-bistability
name=$1; seed=$2; frames=$3; extra=${4:-}
out=$O/runs/$name/seed$seed; mkdir -p $out
[ -f $out/metrics.json ] && exit 0
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
w="{\"dump\":\"$out/flow.npz\"${extra:+,$extra}}"
echo "WRAP=$w" > $O/logs/$name.s$seed.log
start=$(date +%s)
WORLD_P='{"CARGO":0}' WRAP="$w" /home/user/labenv/bin/python -m labkit.run $O/wrap_world.py --out $out --seeds $seed \
  --size 128 128 --frames $frames --spf 50 --lineage-k 40 --no-movie >> $O/logs/$name.s$seed.log 2>&1
echo "elapsed $(( $(date +%s) - start )) s" >> $O/logs/$name.s$seed.log
