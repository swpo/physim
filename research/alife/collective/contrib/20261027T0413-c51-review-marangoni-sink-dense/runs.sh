#!/bin/bash
# c51 review of c45 dense sink escape: arms S and I (mar 40) and S at mar 0, disc_dt 50, fresh seed 97, T=1600; extract.py + fate.py (dense version, writes /tmp/claude-0/se/sel_<label>.json) unchanged
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; mkdir -p /tmp/claude-0/se
W=collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/world.py; R=collective/contrib/20261027T0413-c51-review-marangoni-sink-dense; E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
run() { n=$1; wp=$2; DISC_LOG=$R/$n.disc.jsonl WORLD_P="$wp" python -m labkit.run $W --out $R/$n --seeds 97 --size 128 128 --frames 320 --no-movie > $R/$n.out 2>&1; }
post() { n=$1; python $E $R/$n/frames.npz $W $n 1.0 $R/$n/table.json; python collective/contrib/20261026T2123-c45-marangoni-sink-escape-dense/fate.py $R/$n/frames.npz $W $R/$n.disc.jsonl $R/$n/table.json c51$n > $R/$n/fate.txt 2>&1; cp /tmp/claude-0/se/sel_c51$n.json $R/$n/sel.json; }
run S_s97 '{"ARM":"S","disc_dt":50}' & run I_s97 '{"ARM":"I","disc_dt":50}'; wait
post S_s97 & post I_s97; wait
run S_mar0_s97 '{"ARM":"S","mar":0,"disc_dt":50}'; post S_mar0_s97
echo done > $R/done.txt
