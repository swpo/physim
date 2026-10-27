#!/bin/bash
# c53 review of 20261026T2216-c48-cips-gene-selection-interim: sel.py (copied unchanged with world.py) on fresh seed 7,
# a2 0.5 and the a2 0 twin (same event streams), swap_T 200, wash_T 1000, T=20000; labkit re-run of the a2 0.5 world, seed 7, T=12000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
R=collective/contrib/20261027T1029-c53-review-cips-gene-interim
OMP_NUM_THREADS=2 WORLD_P='{"a2":0.5,"swap_T":200,"wash_T":1000}' python -m labkit.run collective/contrib/20261026T2216-c48-cips-gene-selection-interim/world.py --out $R/pack --seeds 7 --frames 120 --no-movie > $R/pack.log 2>&1 &
cd $R
WORLD_P='{"a2":0.5,"swap_T":200,"wash_T":1000}' python sel.py 7 20000 sel_s7_a0.5 > sel_a05.log 2>&1 &
WORLD_P='{"a2":0.0,"swap_T":200,"wash_T":1000}' python sel.py 7 20000 sel_s7_a0.0 > sel_a0.log 2>&1 &
wait; echo ALLDONE
