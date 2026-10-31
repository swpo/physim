#!/usr/bin/env bash
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/packs
W=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/pm_noise.py
run() {
  if [ "$1" = phi ]; then P="{\"dyn_noise\": $2, \"noise_fields\": [\"phi\"]}"; else P="{\"dyn_noise\": $2, \"noise_fields\": [\"phi\"], \"mult_fields\": [\"S\", \"K\", \"L\"]}"; fi
  WORLD_P="$P" .labenv/bin/python -m labkit.run $W --out $OUT/$1_$2_s$3 --seeds $3 --frames 160 --no-movie > $OUT/log_$1_$2_$3.txt 2>&1; }
for mode in phi mult; do for a in 0.01 0.03 0.1; do for s in 0 1 2; do echo "$mode $a $s"; done; done; done | xargs -P 4 -n 3 bash -c "$(declare -f run); OUT=$OUT W=$W; run \"\$0\" \"\$1\" \"\$2\""
echo done
