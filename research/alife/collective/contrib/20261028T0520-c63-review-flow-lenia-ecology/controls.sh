#!/bin/bash
# c63: food-source controls on fresh seed 21 (160^2, t=2000; switch at t=1000), run after the seed-22 re-run.
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261028T0520-c63-review-flow-lenia-ecology
while pgrep -f "rerun22" >/dev/null; do sleep 20; done
WORLD_P='{"ymode":"bodies"}' python -m labkit.run $R/ctrl_world.py --out $R/ctrl_bodies --seeds 21 --size 160 160 --frames 400 --no-movie > $R/ctrl_bodies.log 2>&1
WORLD_P='{"ymode":"film"}' python -m labkit.run $R/ctrl_world.py --out $R/ctrl_film --seeds 21 --size 160 160 --frames 400 --no-movie > $R/ctrl_film.log 2>&1
