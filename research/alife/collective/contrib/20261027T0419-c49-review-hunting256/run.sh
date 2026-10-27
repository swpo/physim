#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=4
C=collective/contrib/20261026T2024-c46-hunting-predators-divide-256; R=collective/contrib/20261027T0419-c49-review-hunting256
python -m labkit.run $C/world.py --out $R/rerun256 --seeds 10 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/a.log 2>&1
python $C/splits3.py $R/rerun256/frames.npz $R/strict_pred8.png 10 1 100 8 > $R/strict_pred8.json
python $C/splits3.py $R/rerun256/frames.npz $R/strict_prey8.png 10 0 100 8 > $R/strict_prey8.json
echo ALLDONE
