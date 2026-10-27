#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
C=collective/contrib/20261026T1924-c45-marangoni-turnover-long; W=$C/world.py; R=collective/contrib/20261027T0327-c49-review-marangoni-turnover/runs
E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
mkdir -p $R/dil_s83 $R/nodil_s83
TURNOVER_LOG=$R/dil_s83/dilution.log.jsonl WORLD_P='{"p_dil":0.10,"REDIST":1}' python -m labkit.run $W --out $R/dil_s83 --seeds 83 --size 128 128 --frames 400 --no-movie > $R/dil.log 2>&1 &
WORLD_P='{"p_dil":0.0}' python -m labkit.run $W --out $R/nodil_s83 --seeds 83 --size 128 128 --frames 400 --no-movie > $R/nodil.log 2>&1
wait
for n in dil_s83 nodil_s83; do python $E $R/$n/frames.npz $W $n 1.0 $R/$n/table.json; done
python $C/turnover_stats.py $R/dil_s83/table.json $R/dil_s83/metrics.json $R/dil_s83/dilution.log.jsonl 40 48 > $R/dil_s83/stats.txt
python $C/turnover_stats.py $R/nodil_s83/table.json $R/nodil_s83/metrics.json - 40 48 > $R/nodil_s83/stats.txt
python collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/analyze.py $R/heredity_s83.txt $R/dil_s83/table.json
echo ALLDONE
