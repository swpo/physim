#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
O=/tmp/claude-0/se/runs; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; DISC_LOG=$O/$n.s$s.disc.jsonl WORLD_P="$wp" python -m labkit.run /tmp/claude-0/se/world.py --out $O/$n/seed$s --seeds $s --size 128 128 --frames 320 --no-movie > $O/$n.s$s.out 2>&1; }
run S 90 '{"ARM":"S"}' & run I 90 '{"ARM":"I"}' ; wait
run S 91 '{"ARM":"S"}' & run I 91 '{"ARM":"I"}' ; wait
run S_mar0 90 '{"ARM":"S","mar":0}'
echo done
