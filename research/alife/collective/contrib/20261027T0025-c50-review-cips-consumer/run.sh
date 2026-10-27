#!/bin/bash
cd /home/user/physim/research/alife
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
W=collective/contrib/20261026T1700-c43-cips-consumer/world.py; O=/tmp/claude-0/rv
while pgrep -f "sp/world.py" >/dev/null; do sleep 10; done
python -m labkit.run $W --out $O/pack/seed1717 --seeds 1717 --frames 120 --lineage-k 5 --no-movie > $O/pack.out 2>&1 &
WORLD_P='{"tcut":3000}' python -m labkit.run $W --out $O/efork/seed1717 --seeds 1717 --frames 80 --lineage-k 5 --no-movie > $O/efork.out 2>&1; wait
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $O/twin/seed1717 --seeds 1717 --frames 120 --lineage-k 5 --no-movie > $O/twin.out 2>&1 &
cd /tmp/claude-0/sp && SKIP1=1 bash -c 'source <(sed -n "1,5p" run2.sh); run Efast100 501 "{\"ARM\":\"S\",\"disc_v\":0.16,\"disc_dt\":100}"'
wait; echo done
