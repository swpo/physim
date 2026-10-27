#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
O=/tmp/claude-0/sp/runs; mkdir -p $O
run() { n=$1; s=$2; wp=$3; [ -f $O/$n/seed$s/metrics.json ] && return; MUT_LOG=$O/$n.s$s.mut.jsonl DISC_LOG=$O/$n.s$s.disc.jsonl WORLD_P="$wp" python -m labkit.run /tmp/claude-0/sp/world.py --out $O/$n/seed$s --seeds $s --size 128 128 --frames 400 --no-movie > $O/$n.s$s.out 2>&1; }
run Efast 501 '{"ARM":"S","disc_v":0.16}' & run twinfast 501 '{"ARM":"S","disc_v":0.16,"MARS":[40,40,40]}' ; wait
run Efast100 501 '{"ARM":"S","disc_v":0.16,"disc_dt":100}' & run twinfast100 501 '{"ARM":"S","disc_v":0.16,"disc_dt":100,"MARS":[40,40,40]}' ; wait
echo done
