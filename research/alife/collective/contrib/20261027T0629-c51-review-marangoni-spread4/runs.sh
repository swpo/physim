#!/bin/bash
# c51 review of c50 marangoni spread loop 4: E (escape discs, ARM S) and the identical-event twin (MARS 40/40/40) on fresh seed 504, T=2000;
# per-track tables (c00 extract.py), spread_stats.py (loop 1), pool.py (loop 4), all unchanged
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261027T0000-c50-marangoni-spread-loop1/world.py; R=collective/contrib/20261027T0629-c51-review-marangoni-spread4; S=504
run() { n=$1; wp=$2; MUT_LOG=$R/$n.s$S.mut.jsonl DISC_LOG=$R/$n.s$S.disc.jsonl WORLD_P="$wp" python -m labkit.run $W --out $R/${n}_s$S --seeds $S --size 128 128 --frames 400 --no-movie > $R/$n.out 2>&1; }
run E '{"ARM":"S"}' & run twin '{"ARM":"S","MARS":[40,40,40]}'; wait
for n in E twin; do
  python collective/contrib/20261026T1530-c00-marangoni-minority-lineages/files/extract.py $R/${n}_s$S/frames.npz $W ${n}_s$S 1.0 $R/${n}_s$S/table.json
  python collective/contrib/20261027T0000-c50-marangoni-spread-loop1/spread_stats.py $R/${n}_s$S/frames.npz $W $R/${n}_s$S/table.json $R/${n}_s$S/metrics.json $R/$n.s$S.mut.jsonl ${n}_s$S $R/out > $R/${n}_s$S/stats.txt 2>&1
done
python collective/contrib/20261027T0240-c50-marangoni-spread-paired4/pool.py $R/out 504 > $R/pool.txt 2>&1
echo done > $R/done.txt
