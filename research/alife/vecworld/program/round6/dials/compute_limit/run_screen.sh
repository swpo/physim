#!/bin/bash
# The state-given screen, one process at a time, restart-safe. usage: run_screen.sh <scratch dir>
S=$1
PY="/home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
HERE=$(cd "$(dirname "$0")" && pwd)
go() { # outfile, args...
  f=$S/$1; shift
  [ -f "$f" ] || OMP_NUM_THREADS=1 nice -n 10 $PY $HERE/screen_state.py "$@" --scratch $S 2>&1 | grep -v "^ *rollout"
}
go scr_base.npz base
go scr_b_none_dt1.npz branch --arm none --dtf 1
go scr_t_none.npz tiles --arm none
go scr_b_none_dt4.npz branch --arm none --dtf 4
go scr_b_aimed_dt1.npz branch --arm aimed --dtf 1
go scr_b_blind_dt1.npz branch --arm blind --dtf 1
go scr_t_aimed.npz tiles --arm aimed
go scr_b_aimed_dt4.npz branch --arm aimed --dtf 4
go scr_b_none_dt2.npz branch --arm none --dtf 2
echo SCREEN_DONE
