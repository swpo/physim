#!/usr/bin/env bash
# noise dose-response battery: labkit packs of fv_noise.py, one --out per (form, sd, seed), 2 processes at a time
# usage: sweep.sh FRAMES "form sd seed" ...   forms: A additive om+Y | B additive om + proportional Y | F additive Y only | G proportional Y only
cd /home/user/physim/research/alife
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/fedvortex
PY=/home/user/physim/research/alife/.labenv/bin/python
SPL=/home/user/physim/research/alife/collective/contrib/20261027T0712-c53-fed-vortex-claim/splits.py
FR=$1; shift
run() {
  form=$1; sd=$2; seed=$3
  case $form in
    A) WP="{\"dyn_noise\": $sd}";;
    B) WP="{\"dyn_noise\": $sd, \"noise_fields\": [\"om\"], \"mult_fields\": [\"Y\"]}";;
    F) WP="{\"dyn_noise\": $sd, \"noise_fields\": [\"Y\"]}";;
    G) WP="{\"dyn_noise\": $sd, \"noise_fields\": [], \"mult_fields\": [\"Y\"]}";;
  esac
  o=$D/packs/${form}${sd}_s${seed}
  s0=$(date +%s)
  WORLD_P="$WP" $PY -m labkit.run $D/fv_noise.py --out $o --seeds $seed --frames $FR --spf 150 --no-movie > $D/logs/pack_${form}${sd}_s${seed}.txt 2>&1
  $PY $SPL $o > $D/logs/splits_${form}${sd}_s${seed}.txt 2>&1
  echo "$form $sd $seed wall $(( $(date +%s) - s0 ))s" >> $D/logs/sweep_done.txt
}
export -f run; export D PY SPL FR
printf '%s\n' "$@" | xargs -P 2 -I{} bash -c 'run {}'
echo SWEEPDONE >> $D/logs/sweep_done.txt
