#!/bin/bash
# usage: screen.sh T outdir name1 'json1' name2 'json2' ...  (runs two at a time)
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=$1; D=$2; shift 2; mkdir -p $D
SEED=${SEED:-0}; SIZE=${SIZE:-128}
while [ $# -gt 0 ]; do
  n=$1; j=$2; shift 2
  WORLD_P="$j" python drive.py ${WORLD:-world.py} $D/$n --T $T --seed $SEED --size $SIZE &
  while [ $(jobs -r | wc -l) -ge ${PAR:-4} ]; do sleep 2; done
done
wait
