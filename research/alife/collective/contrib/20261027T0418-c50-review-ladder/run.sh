#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T2018-c45-marangoni-ladder/world.py; O=${OUT:-/tmp/claude-0/ld/runs}; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; rm -f $O/$n.s$s.*.jsonl; MUT_LOG=$O/$n.s$s.mut.jsonl TURNOVER_LOG=$O/$n.s$s.dil.jsonl WORLD_P="$wp" python -m labkit.run $W --out $O/$n/seed$s --seeds $s --size 128 128 --frames 400 --no-movie > $O/$n.s$s.out 2>&1; }
run ladder 104 '{}' & run twin 104 '{"MARS":[40,40,40]}' ; wait
echo done
