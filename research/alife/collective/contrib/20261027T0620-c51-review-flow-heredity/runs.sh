#!/bin/bash
# c51 review of c49 flow heredity: heredity.py (copied with world.py) on seeds 8 and 9 for eps +0.1, 0, -0.1 (T=800), and a labkit pack at eps 0.1 on seed 8
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; R=collective/contrib/20261027T0620-c51-review-flow-heredity
for s in 8 9; do
  WORLD_P='{"eps":0.1}' python $R/heredity.py $R/her/h_s${s}_e0.1 $s 800 > $R/her/log_s${s}_p.txt 2>&1 &
  WORLD_P='{"eps":-0.1}' python $R/heredity.py $R/her/h_s${s}_e-0.1 $s 800 > $R/her/log_s${s}_m.txt 2>&1
  wait
  WORLD_P='{"eps":0}' python $R/heredity.py $R/her/h_s${s}_e0 $s 800 > $R/her/log_s${s}_0.txt 2>&1
done &
WORLD_P='{"eps":0.1}' python -m labkit.run $R/world.py --out $R/pack_eps0.1_s8 --seeds 8 --frames 800 --spf 25 --no-movie > $R/pack.log 2>&1
wait; echo done > $R/done.txt
