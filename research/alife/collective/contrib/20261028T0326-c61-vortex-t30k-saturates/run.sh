#!/bin/bash
# c61: T=30000 pair of c58's trait3d world on seed 6 / mut_seed 6, standard waste, 1 thread each (~4 h each with 4-6 jobs on 4 cores)
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":6}' python $T s6_spec 6 30000 > s6_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":6}' python $T s6_blind 6 30000 > s6_blind.log 2>&1 &
wait
V=/home/user/physim/research/alife/collective/contrib/20261028T0105-c61-vortex-long-memory-travels
python $V/vnov.py vnov_s6.json W=2000 s6=s6_spec.json:s6_blind.json; python $V/vplot.py vnov_s6.json s6.png; python persist.py 2000 s6=s6_spec.json s6tw=s6_blind.json
