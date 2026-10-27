#!/bin/bash
# usage: an.sh arm seed
cd /home/user/physim/research/alife && export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
O=/tmp/claude-0/sp/runs; X=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py; a=$1; s=$2; o=/tmp/claude-0/sp/out
python $X $O/$a/seed$s/frames.npz /tmp/claude-0/sp/world.py ${a}_s$s 1.0 $o/${a}_s${s}_tab.json 2>/dev/null
python /tmp/claude-0/sp/spread_stats.py $O/$a/seed$s/frames.npz /tmp/claude-0/sp/world.py $o/${a}_s${s}_tab.json $O/$a/seed$s/metrics.json $O/$a.s$s.mut.jsonl ${a}_s$s $o > /dev/null
python /tmp/claude-0/sp/fate_kind.py $O/$a/seed$s/frames.npz /tmp/claude-0/sp/world.py $O/$a.s$s.disc.jsonl $o/${a}_s${s}_tab.json ${a}_s$s > $o/${a}_s${s}_fate.txt 2>&1
