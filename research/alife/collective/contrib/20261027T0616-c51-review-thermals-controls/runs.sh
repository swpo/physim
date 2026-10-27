#!/bin/bash
# c51 review of c49 thermals controls: 1.5x resolution (dx 2/3, 192^2) seed 3; T=2000 seed 3; local cut (cut.py, copied with world.py) seeds 3 and 4
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261027T0024-c49-thermals-controls/world.py; R=collective/contrib/20261027T0616-c51-review-thermals-controls
WORLD_P='{"dx":0.6666667}' python -m labkit.run $W --out $R/pack_res15_s3 --seeds 3 --size 192 192 --frames 600 --spf 25 --no-movie > $R/res15.log 2>&1 &
python -m labkit.run $W --out $R/pack_long_s3 --seeds 3 --frames 2000 --spf 25 --no-movie > $R/long.log 2>&1
wait
(cd $R && python cut.py 3 > cut3.log 2>&1) & (cd $R && python cut.py 4 > cut4.log 2>&1); wait
for d in pack_res15_s3 pack_long_s3; do python collective/contrib/20261027T0024-c49-thermals-controls/divmove.py $R/$d $W > $R/$d/divmove.txt; done
echo done > $R/done.txt
