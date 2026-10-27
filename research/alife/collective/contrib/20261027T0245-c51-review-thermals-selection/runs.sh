#!/bin/bash
# c51 review of c49 thermals selection: heredity2 (author's analysis, size option added) on fresh seeds 6 and 7, both arms;
# labkit packs of both arms on seed 6; 1.5x resolution (dx 2/3, 192^2) heredity2 on seed 6, both arms
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
C=collective/contrib/20261027T0222-c49-thermals-selection-claim; R=collective/contrib/20261027T0245-c51-review-thermals-selection; W=$C/world.py
for s in 6 7; do
  WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25}' python $R/heredity2_c51.py $R/her/m_s${s}_e-0.1 $s 1200 > $R/her/log_s${s}_sel.txt 2>&1 &
  WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25}' python $R/heredity2_c51.py $R/her/m_s${s}_e0 $s 1200 > $R/her/log_s${s}_neu.txt 2>&1
  wait
done
WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $R/pack_sel --seeds 6 --frames 1200 --spf 25 --no-movie > $R/sel.log 2>&1 &
WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $R/pack_neutral --seeds 6 --frames 1200 --spf 25 --no-movie > $R/neu.log 2>&1
wait
echo stage2 > $R/stage2.txt
SIZE=192 WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25,"dx":0.6666667}' python $R/heredity2_c51.py $R/her/m_s6_e-0.1_dx23 6 1200 > $R/her/log_s6_sel_dx23.txt 2>&1 &
SIZE=192 WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25,"dx":0.6666667}' python $R/heredity2_c51.py $R/her/m_s6_e0_dx23 6 1200 > $R/her/log_s6_neu_dx23.txt 2>&1
wait; echo done > $R/done.txt
