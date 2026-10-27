#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
O=${OUT:-/tmp/claude-0/sp/runs}; W=${W:-collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py}; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; MUT_LOG=$O/$n.s$s.mut.jsonl DISC_LOG=$O/$n.s$s.disc.jsonl WORLD_P="$wp" python -m labkit.run $W --out $O/$n/seed$s --seeds $s --size 128 128 --frames 400 --no-movie > $O/$n.s$s.out 2>&1; }
S=${SEED:-500}
run E $S '{"ARM":"S"}' & run C $S '{"ARM":"I"}' ; wait
run twin $S '{"ARM":"S","MARS":[40,40,40]}' & run off $S '{"ARM":"S","MARS":[0,0,0]}' ; wait
echo done
