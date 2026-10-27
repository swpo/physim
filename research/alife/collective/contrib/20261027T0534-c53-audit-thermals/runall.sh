#!/bin/bash
# c53 audit runs: fresh seeds 31 32 (claimed world), fuel fork at t=400 on 31 32, dt/2 seed 33, 1.5x grid seed 34,
# passive-thermal fork (A=0,h=0 at t=300) and burn-off fork (A=0 at t=300) on seed 31
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
D=collective/contrib/20261027T0534-c53-audit-thermals; W=collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py; W2=$D/world.py
python -m labkit.run $W --out $D/rerun --seeds 31 32 --frames 600 --spf 25 --no-movie > $D/rerun.log 2>&1 &
WORLD_P='{"fork_t":400}' python -m labkit.run $W --out $D/fork --seeds 31 32 --frames 600 --spf 25 --no-movie > $D/fork.log 2>&1
wait
WORLD_P='{"dt":0.02}' python -m labkit.run $W --out $D/dthalf --seeds 33 --frames 600 --spf 50 --dt 0.02 --no-movie > $D/dthalf.log 2>&1 &
WORLD_P='{"fork2_t":300,"fork2":{"A":0,"h":0}}' python -m labkit.run $W2 --out $D/passive --seeds 31 --frames 450 --spf 25 --no-movie > $D/passive.log 2>&1
WORLD_P='{"fork2_t":300,"fork2":{"A":0}}' python -m labkit.run $W2 --out $D/noburn --seeds 31 --frames 450 --spf 25 --no-movie > $D/noburn.log 2>&1
wait
WORLD_P='{"nu":0.675,"kT":0.225,"kY":4.5,"hyper":0.0050625,"g":0.75,"L":6.0,"dt":0.025}' python -m labkit.run $W --out $D/res15 --seeds 34 --size 192 192 --frames 600 --spf 40 --dt 0.025 --min-area 14 --no-movie > $D/res15.log 2>&1
echo ALLDONE
