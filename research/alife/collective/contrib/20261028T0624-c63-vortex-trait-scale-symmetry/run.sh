#!/bin/bash
# c63: scale test on c61's seed 15 (20261028T0409-c61-vortex-sw-not-radius ran dm 0.4 at sw 0.4 and 0.8)
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"dm":0.2,"mut_dt":50,"mut_seed":15}' python $T d02_s04 15 6000 &
WORLD_P='{"ew":0.25,"sw":0.8,"dm":0.8,"mut_dt":50,"mut_seed":15}' python $T d08_s08 15 6000 &
wait
