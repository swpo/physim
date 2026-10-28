#!/usr/bin/env bash
# detectability ensembles: usage run_detect.sh SEED FORM NOISE WINDOW "armsA" "armsB"   (two process lanes)
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex
PY=/home/user/physim/research/alife/.labenv/bin/python
SEED=$1; FORM=$2; NZ=$3; WIN=$4
lane() { for a in $1; do $PY $D/apparatus.py detect_run --seed $SEED --form $FORM --noise $NZ --window $WIN --arm $a; done; }
lane "$5" > $D/logs/detect_${SEED}_${FORM}${NZ}_laneA.txt 2>&1 &
lane "$6" > $D/logs/detect_${SEED}_${FORM}${NZ}_laneB.txt 2>&1 &
wait
echo DETECTDONE
