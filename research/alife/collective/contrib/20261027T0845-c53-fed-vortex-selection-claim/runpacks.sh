#!/bin/bash
# labkit packs of the heredity world: b favoured (eps 0.2) and the neutral twin (eps 0), seeds 1 2, T=4500 (3 t frames)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
D=collective/contrib/20261027T0845-c53-fed-vortex-selection-claim
WORLD_P='{"eps":0.2,"mut_dt":50}' python -m labkit.run $D/world.py --out $D/pack_sel --seeds 1 2 --frames 1500 --spf 150 --no-movie > $D/pack_sel.log 2>&1 &
WORLD_P='{"eps":0,"mut_dt":50}' python -m labkit.run $D/world.py --out $D/pack_neutral --seeds 1 2 --frames 1500 --spf 150 --no-movie > $D/pack_neutral.log 2>&1
wait; echo ALLDONE
