#!/bin/bash
# After run_after.sh: the coarse-step surrogate at x5 (250 / 4 is not an integer, so x4 cannot keep the tick time).
S=$1
PY="/home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
HERE=$(cd "$(dirname "$0")" && pwd)
while ! grep -q ALL_DONE $S/after.log; do sleep 10; done
go() { f=$S/$1; shift; [ -f "$f" ] || OMP_NUM_THREADS=1 nice -n 10 $PY $HERE/screen_state.py "$@" --scratch $S 2>&1 | grep -v "^ *rollout"; }
go scr_b_none_dt5.npz branch --arm none --dtf 5
go scr_b_aimed_dt5.npz branch --arm aimed --dtf 5
go scr_b_aimed_dt2.npz branch --arm aimed --dtf 2
echo ALL2_DONE
