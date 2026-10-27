#!/bin/bash
# loop 1b: linear fitness (fit lin, eps 0.2) favoured vs twin on seeds 1 2; labkit packs of the tanh arm and its twin (seed 1)
cd "$(dirname "$0")"; export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH OMP_NUM_THREADS=1
D=$PWD
WORLD_P='{"eps":0.2,"mut_dt":50,"fit":"lin"}' python trait.py l_s1_e0.2 1 6000 > l_1_sel.log 2>&1 &
WORLD_P='{"eps":0.2,"mut_dt":50,"fit":"lin"}' python trait.py l_s2_e0.2 2 6000 > l_2_sel.log 2>&1 &
cd /home/user/physim/research/alife
WORLD_P='{"eps":0.3,"mut_dt":50}' python -m labkit.run $D/world.py --out $D/pack_sel --seeds 1 --frames 2000 --spf 150 --no-movie > $D/pack_sel.log 2>&1 &
WORLD_P='{"eps":0,"mut_dt":50}' python -m labkit.run $D/world.py --out $D/pack_neutral --seeds 1 --frames 2000 --spf 150 --no-movie > $D/pack_neutral.log 2>&1 &
wait; echo ALLDONE
