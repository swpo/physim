#!/bin/bash
# c51 review of c45 sink escape: arms S and I (mar 40) and S at mar 0 on fresh seed 97, T=1600; extract.py + fate.py unchanged
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2053-c45-marangoni-sink-escape/world.py; R=collective/contrib/20261027T0357-c51-review-marangoni-sink; E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
run() { n=$1; wp=$2; DISC_LOG=$R/$n.disc.jsonl WORLD_P="$wp" python -m labkit.run $W --out $R/$n --seeds 97 --size 128 128 --frames 320 --no-movie > $R/$n.out 2>&1; }
post() { n=$1; python $E $R/$n/frames.npz $W $n 1.0 $R/$n/table.json; python collective/contrib/20261026T2053-c45-marangoni-sink-escape/fate.py $R/$n/frames.npz $W $R/$n.disc.jsonl $R/$n/table.json $n > $R/$n/fate.txt 2>&1; }
run S_s97 '{"ARM":"S"}' & run I_s97 '{"ARM":"I"}'; wait
post S_s97 & post I_s97; wait
run S_mar0_s97 '{"ARM":"S","mar":0}'; post S_mar0_s97
echo done > $R/done.txt
