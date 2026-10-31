#!/usr/bin/env bash
# Sequential queue (one heavy process at a time). Waits for the running half-noise ensemble (pid $1) first.
cd "$(dirname "$0")"
P=/home/user/physim/research/alife/.labenv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
[ -n "$1" ] && tail -f /dev/null --pid="$1"
{ time $P cconv.py ens c001:dt0.1:N288:Y c002:dt0.1:N288:Y ; } > out/step6.log 2>&1
{ time ( $P capab.py 5 0.1 192 5000 2500 600 s5_dt0.1_N192 && $P capab.py 6 0.1 192 5000 2500 600 s6_dt0.1_N192 ) ; } > out/step7.log 2>&1
{ time ( $P capab.py 5 0.1 288 5000 2500 600 s5_dt0.1_N288 && $P capab.py 6 0.1 288 5000 2500 600 s6_dt0.1_N288 ) ; } > out/step8.log 2>&1
( $P timing.py 0.1 192 300; $P timing.py 0.1 288 200; $P timing.py 0.1 384 100 ) > out/timing.log 2>&1
echo queue-done >> out/step8.log
