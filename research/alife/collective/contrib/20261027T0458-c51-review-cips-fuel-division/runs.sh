#!/bin/bash
# c51 review of c48 fuel-powered division: labkit packs of the claimed world (defaults) and the fuel-independent control (react_const 1) on fresh seed 2, 192^2, t=12000;
# then fork.py (copied with an identical copy of world.py next to it, as fork.py loads world.py from its own directory) seed 2, fork at t=8000, 500 t after
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2102-c48-cips-fuel-powered-division/world.py; R=collective/contrib/20261027T0458-c51-review-cips-fuel-division
python -m labkit.run $W --out $R/pack_s2 --seeds 2 --frames 120 --no-movie > $R/pack.log 2>&1 &
WORLD_P='{"react_const":1}' python -m labkit.run $W --out $R/pack_const_s2 --seeds 2 --frames 120 --no-movie > $R/pack_const.log 2>&1
wait
PYTHONPATH=$PWD python $R/fork.py 2 8000 500 $R/fork_s2 > $R/fork.log 2>&1
echo done > $R/done.txt
