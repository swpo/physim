#!/bin/bash
# the with-predator arm on the same seed and grid as the twin (seed 16, 256^2, t=12000)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out collective/contrib/20261027T0519-c51-review-hunting-controls/pack256_s16 --seeds 16 --size 256 256 --frames 120 --lineage-k 5 --no-movie > collective/contrib/20261027T0519-c51-review-hunting-controls/pack256.log 2>&1
echo done > collective/contrib/20261027T0519-c51-review-hunting-controls/done2.txt
