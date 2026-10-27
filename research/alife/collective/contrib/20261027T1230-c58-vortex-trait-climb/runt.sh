#!/bin/bash
# continuous trait: favoured (eps 0.3) and identical-draw neutral twin (eps 0), whole-vortex mutation dm 0.4 every 50 t, T=6000
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 1 2; do
  WORLD_P='{"eps":0.3,"mut_dt":50}' python trait.py t_s${sd}_e0.3 $sd 6000 > t_${sd}_sel.log 2>&1 &
  WORLD_P='{"eps":0,"mut_dt":50}' python trait.py t_s${sd}_e0 $sd 6000 > t_${sd}_neu.log 2>&1 &
done
wait; echo ALLDONE
