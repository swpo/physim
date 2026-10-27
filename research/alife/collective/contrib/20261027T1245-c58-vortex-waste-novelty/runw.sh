#!/bin/bash
# kind-specific waste (ew 0.25, sw 0.4) vs kind-blind waste (sw 0), seeds 1 2, T=6000, whole-vortex mutation +-0.4 every 50 t;
# the eps 0 neutral twin (no waste effect) with the same draws is 20261027T1230-c58-vortex-trait-climb/t_s*_e0.json
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 1 2; do
  WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50}' python trait.py w_s${sd}_spec $sd 6000 > w_${sd}_spec.log 2>&1 &
  WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50}' python trait.py w_s${sd}_blind $sd 6000 > w_${sd}_blind.log 2>&1 &
done
wait; echo ALLDONE
