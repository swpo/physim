#!/bin/bash
# batch.sh WORLD PREFIX STEPS "seed list" [extra --set args]  (runs 2 at a time)
W=$1; P=$2; S=$3; L=$4; shift 4
for r in $L; do
  python threads/flow-lenia/scripts/screen.py $W threads/flow-lenia/screens/${P}_r$r.png --steps $S --set rule_seed=$r "$@" &
  while [ $(jobs -r | wc -l) -ge 2 ]; do wait -n; done
done; wait
