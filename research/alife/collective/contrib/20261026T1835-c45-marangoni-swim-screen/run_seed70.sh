#!/bin/bash
# runs settings two at a time
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T0505-c34-nematic-marangoni/world.py
O=/tmp/claude-0/ms/runs
mkdir -p $O
run() { name=$1; seed=$2; wp=$3; [ -f $O/$name/seed$seed/metrics.json ] && return; WORLD_P="$wp" python -m labkit.run $W --out $O/$name/seed$seed --seeds $seed --size 128 128 --frames 200 --no-movie > $O/$name.s$seed.log 2>&1; }
SEED=${1:-70}
run base $SEED '{"CARGO":0}' & run mar60 $SEED '{"CARGO":0,"mar":60}' ; wait
run gm05 $SEED '{"CARGO":0,"gm":0.5}' & run gm2 $SEED '{"CARGO":0,"gm":2}' ; wait
run zeta1 $SEED '{"CARGO":0,"zeta":1.0}' & run kr006 $SEED '{"CARGO":0,"kr":0.006}' ; wait
run phib065 $SEED '{"CARGO":0,"phi_b":-0.65}'
echo done
