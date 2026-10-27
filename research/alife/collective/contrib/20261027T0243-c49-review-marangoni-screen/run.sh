#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; O=collective/contrib/20261027T0243-c49-review-marangoni-screen/runs
E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
WORLD_P='{"CARGO":0}' python -m labkit.run $W --out $O/base/seed72 --seeds 72 --size 128 128 --frames 200 --no-movie > $O.base.log 2>&1 &
WORLD_P='{"CARGO":0,"mar":60}' python -m labkit.run $W --out $O/mar60/seed72 --seeds 72 --size 128 128 --frames 200 --no-movie > $O.mar60.log 2>&1
wait
for n in base mar60; do python $E $O/$n/seed72/frames.npz $W $n 1.0 $O/$n/seed72/table.json; done
echo ALLDONE
