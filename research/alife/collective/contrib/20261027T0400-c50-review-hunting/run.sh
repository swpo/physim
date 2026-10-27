#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
C=collective/contrib/20261026T2103-c46-hunting-ecology-claim; W=$C/world.py; O=${OUT:-/tmp/claude-0/hu}
[ -f $O/pack/seed7/metrics.json ] || python -m labkit.run $W --out $O/pack/seed7 --seeds 7 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $O/pack.log 2>&1 &
[ -f $O/twin/seed7/metrics.json ] || WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $O/twin/seed7 --seeds 7 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $O/twin.log 2>&1
wait
cd $C; WORLD_P='{"fork_t":6000}' python drive.py world.py $O/efork_fork --T 7500 --seed 7 --size 128 &
python drive.py world.py $O/efork_fed --T 7500 --seed 7 --size 128; wait
echo done
