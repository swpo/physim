#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
O=/tmp/claude-0/se/runs2; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; DISC_LOG=$O/$n.s$s.disc.jsonl WORLD_P="$wp" python -m labkit.run /tmp/claude-0/se/world.py --out $O/$n/seed$s --seeds $s --size 128 128 --frames 320 --no-movie > $O/$n.s$s.out 2>&1; }
run S 90 '{"ARM":"S","disc_dt":50}' & run I 90 '{"ARM":"I","disc_dt":50}' ; wait
run S 91 '{"ARM":"S","disc_dt":50}' & run I 91 '{"ARM":"I","disc_dt":50}' ; wait
run S_mar0 90 '{"ARM":"S","mar":0,"disc_dt":50}' & run S_mar0 91 '{"ARM":"S","mar":0,"disc_dt":50}' ; wait
echo done
