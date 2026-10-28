#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261028T1015-c63-review-digestion-ecology
python -m labkit.run $R/claim_world.py --out $R/rerun/seed83 --seeds 83 --size 128 128 --frames 120 --no-movie
