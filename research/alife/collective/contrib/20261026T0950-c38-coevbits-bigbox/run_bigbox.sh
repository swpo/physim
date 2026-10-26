export PATH=/home/user/physim/research/alife/.labenv/bin:$PATH NUMBA_NUM_THREADS=1
P='{"w":10,"L":192.0,"G":96,"Np0":2250,"Nq0":68}'
for s in 0 1 2; do MAXLOG=6000000 python drivebits.py big $s 200000 "$P" & done; wait
for s in 0 1 2; do p0=$(python -c "import json;print(json.load(open('d2/big_s$s.json'))['mean_success'])"); MAXLOG=6000000 python drivebits.py bigN $s 200000 "${P%\}},\"neutral\":1,\"p0\":$p0}" & done; wait
