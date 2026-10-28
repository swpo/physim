#!/bin/bash
# c63: permanent distribution memory (dw 0) on seed 6 / mut_seed 6; world.py of 20261028T0700-c63-vortex-distribution-memory
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
export WORLD_DIR=/home/user/physim/research/alife/collective/contrib/20261028T0700-c63-vortex-distribution-memory
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":6,"wmode":"rff","dw":0.0}' python $T p6_rff 6 6000 &     # analysed at the t=5250 checkpoint
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":6,"dw":0.0}' python $T p6_blind 6 6000 &
wait
