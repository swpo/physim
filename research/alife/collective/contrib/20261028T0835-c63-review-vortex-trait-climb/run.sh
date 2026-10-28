#!/bin/bash
# c63 review of 20261027T1230-c58-vortex-trait-climb (world.py, trait.py copied unchanged), fresh seed 31 / mut_seed 31
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
WORLD_P='{"eps":0.3,"mut_dt":50,"mut_seed":31}' python trait.py t_s31_e0.3 31 6000 > t_31_sel.log 2>&1 &
WORLD_P='{"eps":0,"mut_dt":50,"mut_seed":31}' python trait.py t_s31_e0 31 6000 > t_31_neu.log 2>&1 &
wait
WORLD_P='{"eps":0.3,"mut_dt":50,"mut_seed":31}' OMP_NUM_THREADS=2 python -m labkit.run world.py --out pack_sel --seeds 31 --frames 1000 --spf 150 --no-movie
