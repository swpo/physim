#!/bin/bash
# c61: c58's trait3d world with a 4x longer-lived waste at the same reach (dw 0.002 -> 0.0005, Dw 1 -> 0.25: sqrt(Dw/dw) = 22 px), seed 7 / mut_seed 7
export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
T=/home/user/physim/research/alife/collective/contrib/20261027T2243-c59-trait3d-seed5-rarity/trait3c.py
WORLD_P='{"ew":0.25,"sw":0.4,"mut_dt":50,"mut_seed":7,"dw":0.0005,"Dw":0.25}' python $T m7_spec 7 10000 > m7_spec.log 2>&1 &
WORLD_P='{"ew":0.25,"sw":0,"mut_dt":50,"mut_seed":7,"dw":0.0005,"Dw":0.25}' python $T m7_blind 7 10000 > m7_blind.log 2>&1 &
wait; python vnov.py vnov_m7.json W=1000 m7=m7_spec.json:m7_blind.json; python vplot.py vnov_m7.json vnov_m7.png
