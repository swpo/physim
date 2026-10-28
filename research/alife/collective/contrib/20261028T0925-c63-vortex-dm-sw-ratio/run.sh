#!/bin/bash
# c63: dm/sw = 2 (dm 0.8, sw 0.4) on seeds 15 and 16 (mut_seed = seed), T=6000 then resumed to T=12000, and kind-blind twins (sw 0, dm 0.4) to T=6000.
# c58's trait3d world.py, c61's checkpointed trait3c.py; dm/sw 0.5 and 1 on seed 15 are 20261028T0624 (d02_s04) and c61's w0.4_s15.
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261028T0118-c61-vortex-t30k-interim/trait3c.py
for s in 15 16; do
  WORLD_P="{\"ew\":0.25,\"sw\":0.4,\"dm\":0.8,\"mut_dt\":50,\"mut_seed\":$s}" python $T d08_s04_$s $s 6000 &
  WORLD_P="{\"ew\":0.25,\"sw\":0,\"dm\":0.4,\"mut_dt\":50,\"mut_seed\":$s}" python $T d04_blind_$s $s 6000 &
done; wait
for s in 15 16; do WORLD_P="{\"ew\":0.25,\"sw\":0.4,\"dm\":0.8,\"mut_dt\":50,\"mut_seed\":$s}" python $T d08_s04_$s $s 12000 & done; wait
# (seed 15 outputs were named d08_s04 / d04_blind)
