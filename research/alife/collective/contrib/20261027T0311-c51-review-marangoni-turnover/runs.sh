#!/bin/bash
# c51 review of c45 turnover tuning: p_dil 0.10 with REDIST (the best setting) and p_dil 0.20 on fresh seed 84, 150 frames; extract.py + turnover_stats.py unchanged
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/world.py; R=collective/contrib/20261027T0311-c51-review-marangoni-turnover; E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
TURNOVER_LOG=$R/redist.log.jsonl WORLD_P='{"p_dil":0.10,"REDIST":1}' python -m labkit.run $W --out $R/p0.10_redist --seeds 84 --size 128 128 --frames 150 --no-movie > $R/redist.log 2>&1 &
TURNOVER_LOG=$R/p020.log.jsonl WORLD_P='{"p_dil":0.20}' python -m labkit.run $W --out $R/p0.20 --seeds 84 --size 128 128 --frames 150 --no-movie > $R/p020.log 2>&1
wait
for d in p0.10_redist:redist p0.20:p020; do n=${d%%:*}; l=${d##*:}
  python $E $R/$n/frames.npz $W $n 1.0 $R/$n/table.json
  python collective/contrib/20261026T1858-c45-marangoni-turnover-tuning/turnover_stats.py $R/$n/table.json $R/$n/metrics.json $R/$l.log.jsonl > $R/$n/stats.txt
done
echo done > $R/done.txt
