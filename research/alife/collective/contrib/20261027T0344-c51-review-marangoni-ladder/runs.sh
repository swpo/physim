#!/bin/bash
# c51 review of c45's Marangoni ladder: ladder (mar 20/40/60) and identical-event twin (all 40) on fresh seed 102, T=2000; extract.py + ladder_stats.py unchanged
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2018-c45-marangoni-ladder/world.py; R=collective/contrib/20261027T0344-c51-review-marangoni-ladder; E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
MUT_LOG=$R/ladder.mut.jsonl TURNOVER_LOG=$R/ladder.dil.jsonl WORLD_P='{}' python -m labkit.run $W --out $R/ladder_s102 --seeds 102 --size 128 128 --frames 400 --no-movie > $R/ladder.out 2>&1 &
MUT_LOG=$R/twin.mut.jsonl TURNOVER_LOG=$R/twin.dil.jsonl WORLD_P='{"MARS":[40,40,40]}' python -m labkit.run $W --out $R/twin_s102 --seeds 102 --size 128 128 --frames 400 --no-movie > $R/twin.out 2>&1
wait
for n in ladder twin; do
  python $E $R/${n}_s102/frames.npz $W $n 1.0 $R/${n}_s102/table.json
  python collective/contrib/20261026T2018-c45-marangoni-ladder/ladder_stats.py $R/${n}_s102/frames.npz $W $R/${n}_s102/table.json $R/${n}_s102/metrics.json $R/$n.mut.jsonl $n > $R/${n}_s102/stats.txt 2>&1
done
echo done > $R/done.txt
