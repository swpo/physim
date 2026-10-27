#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py; O=${OUT:-/tmp/claude-0/se3/runs}; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; rm -f $O/$n.s$s.disc.jsonl; DISC_LOG=$O/$n.s$s.disc.jsonl WORLD_P="$wp" python -m labkit.run $W --out $O/$n/seed$s --seeds $s --size 128 128 --frames 320 --no-movie > $O/$n.s$s.out 2>&1; }
run S 94 '{"ARM":"S"}' & run I 94 '{"ARM":"I"}' ; wait
run S_mar0 94 '{"ARM":"S","mar":0}'
echo done
