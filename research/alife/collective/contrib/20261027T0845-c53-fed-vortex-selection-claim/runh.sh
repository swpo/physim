#!/bin/bash
# fed-vortex heredity: heredity.py on seeds 1 2 3, b favoured (eps 0.2) and the identical-draw neutral twin (eps 0),
# every vortex labelled a at t=300, mutation every 50 t (one random eating pixel, disk r=6), T=4500
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
for sd in 1 2 3; do
  WORLD_P='{"eps":0.2,"mut_dt":50}' python heredity.py m_s${sd}_e0.2 $sd 4500 > h_${sd}_sel.log 2>&1 &
  WORLD_P='{"eps":0,"mut_dt":50}' python heredity.py m_s${sd}_e0 $sd 4500 > h_${sd}_neu.log 2>&1 &
  while [ $(jobs -r | wc -l) -ge 4 ]; do sleep 2; done
done
wait; echo ALLDONE
