#!/bin/bash
# packs for the claim: flow (3 seeds), g=0 twin (2 seeds), fuel fork at t=400 (2 seeds), dt/2 (seed 0); frames every 1 t
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
C=collective/contrib/20261027T0040-c49-reacting-thermals-claim; W=$C/world.py
python -m labkit.run $W --out $C/pack --seeds 0 1 2 --frames 600 --spf 25 --no-movie > $C/pack.log 2>&1 &
WORLD_P='{"g":0}' python -m labkit.run $W --out $C/pack_g0 --seeds 0 1 --frames 600 --spf 25 --no-movie > $C/pack_g0.log 2>&1
wait
WORLD_P='{"fork_t":400}' python -m labkit.run $W --out $C/pack_fork --seeds 0 1 --frames 600 --spf 25 --no-movie > $C/pack_fork.log 2>&1 &
WORLD_P='{"dt":0.02}' python -m labkit.run $W --out $C/pack_dthalf --seeds 0 --frames 600 --spf 50 --dt 0.02 --no-movie > $C/pack_dthalf.log 2>&1
wait
echo ALLDONE
