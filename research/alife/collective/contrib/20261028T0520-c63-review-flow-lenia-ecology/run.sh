#!/bin/bash
# c63 review of 20261028T0344-c62-flow-lenia-ecology-s-claim (claim_world.py = its world.py, unchanged; defaults = noise start)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261028T0520-c63-review-flow-lenia-ecology
python -m labkit.run $R/claim_world.py --out $R/rerun/seed21 --seeds 21 --size 160 160 --frames 600 --no-movie   # (written to rerun/, moved)
python -m labkit.run $R/claim_world.py --out $R/rerun/seed22 --seeds 22 --size 160 160 --frames 600 --no-movie
WORLD_P='{"pred_on":0}' python -m labkit.run $R/claim_world.py --out $R/twin/seed21 --seeds 21 --size 160 160 --frames 600 --no-movie
./$R/controls.sh     # ctrl_bodies, ctrl_film (ctrl_world.py, seed 21, t=2000, switch at t=1000)
python $R/analysis/record.py 22 160 3000 rec22.npz && python $R/analysis/predstrip.py rec22.npz $R/analysis/strips_s22.png $R/analysis/splits_s22.json 8
