#!/bin/bash
# c53 review of 20261026T2316-c48-cips-gene-selection-negative: sel.py (copied unchanged with world.py) on fresh seed 7, a2 -0.1
# (ancestors g2) and the a2 0 twin, swap_T 100, wash_T 1000, T=16000 (the finding ran 25000); labkit re-run of the a2 -0.1 world, seed 7, T=12000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1 PYTHONPATH=$PWD
R=collective/contrib/20261027T1101-c53-review-cips-gene-negative; P='"swap_T":100,"wash_T":1000,"inoc_kind":2'
OMP_NUM_THREADS=2 WORLD_P="{\"a2\":-0.1,$P}" python -m labkit.run collective/contrib/20261026T2316-c48-cips-gene-selection-negative/world.py --out $R/pack --seeds 7 --frames 120 --no-movie > $R/pack.log 2>&1 &
cd $R
WORLD_P="{\"a2\":-0.1,$P}" python sel.py 7 16000 sel2_s7_a-0.1 > sel_t.log 2>&1 &
WORLD_P="{\"a2\":0.0,$P}" python sel.py 7 16000 sel2_s7_a0.0 > sel_0.log 2>&1 &
wait; echo ALLDONE
