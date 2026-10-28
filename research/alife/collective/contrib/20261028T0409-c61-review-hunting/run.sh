#!/bin/bash
# c61 triage review of 20261026T2103-c46-hunting-ecology-claim (from research/alife)
export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
O=collective/contrib/20261028T0409-c61-review-hunting
python -m labkit.run collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py --out $O/rerun/seed58 --seeds 58 --size 256 256 --frames 120 --lineage-k 5 --no-movie
python collective/contrib/20261027T1146-c55-pairtest-tool/pairtest.py $O/rerun/seed58 collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py $O/rerun/pairtest_s58.json --K 5
