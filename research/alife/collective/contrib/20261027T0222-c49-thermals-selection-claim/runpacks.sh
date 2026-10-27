#!/bin/bash
# labkit packs: mutation on, every cap starts as kind a; b favoured (eps -0.1) and the neutral twin (eps 0), seeds 0 1
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
C=collective/contrib/20261027T0222-c49-thermals-selection-claim; W=$C/world.py
WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $C/pack_sel --seeds 0 1 --frames 1200 --spf 25 --no-movie > $C/sel.log 2>&1 &
WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $C/pack_neutral --seeds 0 1 --frames 1200 --spf 25 --no-movie > $C/neu.log 2>&1
wait; echo ALLDONE
