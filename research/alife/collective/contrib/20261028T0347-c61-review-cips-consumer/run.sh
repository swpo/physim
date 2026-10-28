#!/bin/bash
# c61 triage review of 20261026T1700-c43-cips-consumer (from research/alife)
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
O=collective/contrib/20261028T0347-c61-review-cips-consumer
python -m labkit.run collective/contrib/20261026T1700-c43-cips-consumer/world.py --out $O/rerun/seed57 --seeds 57 --frames 120 --lineage-k 5 --no-movie
python collective/contrib/20261027T1146-c55-pairtest-tool/pairtest.py $O/rerun/seed57 collective/contrib/20261026T1700-c43-cips-consumer/world.py $O/rerun/pairtest_s57.json --K 5
