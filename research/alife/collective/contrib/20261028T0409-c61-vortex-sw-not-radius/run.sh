#!/bin/bash
# c61: kernel width test, seed 15 / mut_seed 15, T=6000, standard waste, waste arm only at sw 0.4 and sw 0.8
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
for w in 0.4 0.8; do WORLD_P="{\"ew\":0.25,\"sw\":$w,\"mut_dt\":50,\"mut_seed\":15}" python $T w${w}_s15 15 6000 & done; wait
