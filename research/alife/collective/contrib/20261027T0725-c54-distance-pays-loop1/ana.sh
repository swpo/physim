#!/bin/bash
# usage: ana.sh name seed   (runs in /tmp/claude-0/c54/runs)
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
O=${OUT:-/tmp/claude-0/c54/runs}; A=$O/ana; mkdir -p $A
W=collective/contrib/20261027T0725-c54-distance-pays-loop1/world.py
X=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
S=collective/contrib/20261027T0000-c50-marangoni-spread-loop1/spread_stats.py
n=$1; s=$2; d=$O/$n/seed$s
python $X $d/frames.npz $W ${n}_s$s 1.0 $A/${n}_s$s.table.json > /dev/null
touch $O/$n.s$s.mut.jsonl
python $S $d/frames.npz $W $A/${n}_s$s.table.json $d/metrics.json $O/$n.s$s.mut.jsonl ${n}_s$s $A > /dev/null
tail -n +1 $A/${n}_s$s.txt | sed -n '/^mutation/,/^descend/p'
