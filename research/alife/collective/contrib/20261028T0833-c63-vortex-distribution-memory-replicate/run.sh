#!/bin/bash
# c63: replicate of 20261028T0700-c63-vortex-distribution-memory with other random-feature frequencies (rff_seed 1), seed 6, T=6000
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
export WORLD_DIR=/home/user/physim/research/alife/collective/contrib/20261028T0700-c63-vortex-distribution-memory
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":6,"wmode":"rff","rff_seed":1}' python /home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py r6b_rff 6 6000
