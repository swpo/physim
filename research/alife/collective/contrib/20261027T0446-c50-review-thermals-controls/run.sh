#!/bin/bash
# c50: copies of c49's world.py, cut.py, divmove.py were run from a scratch directory (cut.py writes into its cwd)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
S=${SCR:-/tmp/claude-0/tc}; mkdir -p $S; cp collective/contrib/20261027T0024-c49-thermals-controls/{world.py,cut.py,divmove.py} $S/
WORLD_P='{"dx":0.6666667}' python -m labkit.run $S/world.py --out $S/res15/seed21 --seeds 21 --size 192 192 --frames 600 --spf 25 --no-movie
python $S/divmove.py $S/res15/seed21 $S/world.py
(cd $S && python cut.py 21)
