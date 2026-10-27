#!/bin/bash
# fed-vortex claim packs (world defaults = dividing regime): 3 seeds T=3000; no-advection twin; fuel fork at t=2000; world dt/2
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
D=collective/contrib/20261027T0712-c53-fed-vortex-claim; W=$D/world.py
python -m labkit.run $W --out $D/pack --seeds 0 1 2 --frames 1000 --spf 150 --no-movie > $D/pack.log 2>&1 &
( WORLD_P='{"adv":0}' python -m labkit.run $W --out $D/pack_noadv --seeds 0 1 --frames 1000 --spf 150 --no-movie > $D/pack_noadv.log 2>&1
  WORLD_P='{"fork_t":2000}' python -m labkit.run $W --out $D/pack_fork --seeds 0 1 --frames 750 --spf 150 --no-movie > $D/pack_fork.log 2>&1 )
wait
WORLD_P='{"dt":0.01}' python -m labkit.run $W --out $D/pack_dthalf --seeds 0 --frames 1000 --spf 300 --dt 0.01 --no-movie > $D/pack_dthalf.log 2>&1
echo ALLDONE
