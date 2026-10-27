#!/bin/bash
# c51 review of c45's Marangoni swim screen: base (mar 40) vs mar 60 on fresh seeds 76 and 77, CARGO 0, 128^2, T=1000; per-track tables with c00's extract.py, summary with c45's stats.py
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T0505-c34-nematic-marangoni/world.py; R=collective/contrib/20261027T0300-c51-review-marangoni-screen; E=collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py
for s in 76 77; do
  WORLD_P='{"CARGO":0}' python -m labkit.run $W --out $R/base/seed$s --seeds $s --size 128 128 --frames 200 --no-movie > $R/base_s$s.log 2>&1 &
  WORLD_P='{"CARGO":0,"mar":60}' python -m labkit.run $W --out $R/mar60/seed$s --seeds $s --size 128 128 --frames 200 --no-movie > $R/mar60_s$s.log 2>&1
  wait
  python $E $R/base/seed$s/frames.npz $W base$s 1.0 $R/base$s.json
  python $E $R/mar60/seed$s/frames.npz $W mar60$s 1.0 $R/mar60$s.json
done
python collective/contrib/20261026T1835-c45-marangoni-swim-screen/stats.py $R/stats.txt base76:$R/base76.json:$R/base/seed76/metrics.json mar60_76:$R/mar6076.json:$R/mar60/seed76/metrics.json base77:$R/base77.json:$R/base/seed77/metrics.json mar60_77:$R/mar6077.json:$R/mar60/seed77/metrics.json
echo done > $R/done.txt
