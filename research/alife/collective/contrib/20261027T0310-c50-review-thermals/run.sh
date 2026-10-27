#!/bin/bash
# c50 re-runs of 20261027T0040-c49-reacting-thermals-claim (outputs copied into rerun/)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py; O=${OUT:-/tmp/claude-0/th}
python -m labkit.run $W --out $O/pack --seeds 11 12 --frames 600 --spf 25 --no-movie
WORLD_P='{"g":0}' python -m labkit.run $W --out $O/g0 --seeds 11 --frames 600 --spf 25 --no-movie
WORLD_P='{"fork_t":400}' python -m labkit.run $W --out $O/fork --seeds 11 --frames 600 --spf 25 --no-movie
WORLD_P='{"dt":0.02}' python -m labkit.run $W --out $O/dthalf --seeds 11 --frames 600 --spf 50 --dt 0.02 --no-movie
for p in pack/seed11 pack/seed12 g0 dthalf fork; do python collective/contrib/20261027T0040-c49-reacting-thermals-claim/divmove.py $O/$p $W; done
