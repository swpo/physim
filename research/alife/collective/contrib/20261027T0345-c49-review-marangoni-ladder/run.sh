#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
C=collective/contrib/20261026T2018-c45-marangoni-ladder; W=$C/world.py; O=collective/contrib/20261027T0345-c49-review-marangoni-ladder/runs
E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
mkdir -p $O/ladder_s102 $O/twin_s102
MUT_LOG=$O/ladder_s102/mutations.log.jsonl TURNOVER_LOG=$O/ladder_s102/dilution.log.jsonl WORLD_P='{}' python -m labkit.run $W --out $O/ladder_s102 --seeds 102 --size 128 128 --frames 400 --no-movie > $O/l.log 2>&1 &
MUT_LOG=$O/twin_s102/mutations.log.jsonl TURNOVER_LOG=$O/twin_s102/dilution.log.jsonl WORLD_P='{"MARS":[40,40,40]}' python -m labkit.run $W --out $O/twin_s102 --seeds 102 --size 128 128 --frames 400 --no-movie > $O/t.log 2>&1
wait
for n in ladder_s102 twin_s102; do python $E $O/$n/frames.npz $W $n 1.0 $O/$n/table.json; python $C/ladder_stats.py $O/$n/frames.npz $W $O/$n/table.json $O/$n/metrics.json $O/$n/mutations.log.jsonl $n > $O/$n/stats.txt 2>&1; done
echo ALLDONE
