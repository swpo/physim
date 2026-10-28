#!/usr/bin/env bash
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs
W=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py
run() { WORLD_P="{\"dyn_noise\": $1}" .labenv/bin/python -m labkit.run $W --out $OUT/noise_$1_s$2 --seeds $2 --frames 160 --no-movie > $OUT/log_$1_$2.txt 2>&1; }
mkdir -p $OUT
for a in 0 0.001 0.003 0.01 0.03 0.1; do for s in 0 1 2; do echo "$a $s"; done; done | xargs -P 4 -n 2 bash -c "$(declare -f run); OUT=$OUT W=$W; run \"\$0\" \"\$1\""
echo done
