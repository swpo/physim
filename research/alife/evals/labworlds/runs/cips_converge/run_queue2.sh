#!/usr/bin/env bash
# Second sequential queue (the first was stopped at its 30-min background limit during the N288 seed-5 run).
cd "$(dirname "$0")"
P=/home/user/physim/research/alife/.labenv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
{ time ( $P capab.py 5 0.1 288 5000 2500 600 s5_dt0.1_N288 && $P capab.py 6 0.1 288 5000 2500 600 s6_dt0.1_N288 ) ; } > out/step8.log 2>&1
( $P timing.py 0.1 192 300; $P timing.py 0.1 288 200; $P timing.py 0.1 384 100 ) > out/timing.log 2>&1
{ time $P capab.py 5 0.1 384 5000 2500 600 s5_dt0.1_N384 ; } > out/step9.log 2>&1
echo queue2-done >> out/step9.log
