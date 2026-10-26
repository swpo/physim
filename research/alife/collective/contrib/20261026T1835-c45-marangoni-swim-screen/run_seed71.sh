#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T0505-c34-nematic-marangoni/world.py
O=/tmp/claude-0/ms/runs
run() { name=$1; seed=$2; wp=$3; [ -f $O/$name/seed$seed/metrics.json ] && return; WORLD_P="$wp" python -m labkit.run $W --out $O/$name/seed$seed --seeds $seed --size 128 128 --frames 200 --no-movie > $O/$name.s$seed.log 2>&1; }
run base 71 '{"CARGO":0}' & run mar60 71 '{"CARGO":0,"mar":60}' ; wait
run phib065 71 '{"CARGO":0,"phi_b":-0.65}' & run mar80 70 '{"CARGO":0,"mar":80}' ; wait
run mar80 71 '{"CARGO":0,"mar":80}'
echo done
