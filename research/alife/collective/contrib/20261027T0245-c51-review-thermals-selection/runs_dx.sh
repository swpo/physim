#!/bin/bash
# 1.5x resolution (dx 2/3 on a 192^2 grid: same physical box) with the mutation disk scaled to the same physical radius (mut_r 9 px = 6 units), seed 6, both arms
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; R=collective/contrib/20261027T0245-c51-review-thermals-selection
SIZE=192 WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25,"dx":0.6666667,"mut_r":9}' python $R/heredity2_c51.py $R/her/m_s6_e-0.1_dx23 6 1200 > $R/her/log_s6_sel_dx23.txt 2>&1 &
SIZE=192 WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25,"dx":0.6666667,"mut_r":9}' python $R/heredity2_c51.py $R/her/m_s6_e0_dx23 6 1200 > $R/her/log_s6_neu_dx23.txt 2>&1
wait; echo done > $R/done.txt
