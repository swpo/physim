#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
W=collective/contrib/20261026T1800-c43-chasing-consumer/world.py; R=collective/contrib/20261027T0048-c49-review-chasing-consumer
WORLD_P='{"dt":0.1,"chih":0}' python -m labkit.run $W --out $R/rerun_chih0 --seeds 7 --frames 75 --dt 0.1 --lineage-k 5 --no-movie > $R/a.log 2>&1 &
WORLD_P='{"dt":0.1,"chih":10}' python -m labkit.run $W --out $R/rerun_chih10 --seeds 7 --frames 75 --dt 0.1 --lineage-k 5 --no-movie > $R/b.log 2>&1 &
python $(dirname $W)/free.py $R/free_s7.json 7 1000 2000 '[{"dt":0.1,"chih":0},{"dt":0.1,"chih":5},{"dt":0.1,"chih":10}]' > $R/free.log 2>&1 &
wait; echo ALLDONE
