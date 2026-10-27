#!/bin/bash
# c51 review of c46 predators divide: world defaults on fresh seeds 14 and 15 at 256^2, t=12000, --lineage-k 5; strict test splits3.py (predator channel, 8 px) and fate.py (predator daughters' fate)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2024-c46-hunting-predators-divide-256/world.py; R=collective/contrib/20261027T0430-c51-review-predators-divide
for s in 14 15; do python -m labkit.run $W --out $R/pack256_s$s --seeds $s --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/pack_s$s.log 2>&1 & done; wait
for s in 14 15; do
  python collective/contrib/20261026T2024-c46-hunting-predators-divide-256/splits3.py $R/pack256_s$s/frames.npz $R/pack256_s$s/strict_pred.png 1 1 100 8 > $R/pack256_s$s/strict_pred.txt 2>&1
  python $R/fate.py $R/pack256_s$s 0.25 > $R/pack256_s$s/fate.txt 2>&1
done
echo done > $R/done.txt
