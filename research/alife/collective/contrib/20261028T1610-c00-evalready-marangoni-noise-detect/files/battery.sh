#!/usr/bin/env bash
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni
job() {
  case $1 in
    base) P='{"dyn_noise":0}';;
    plain) P="{\"dyn_noise\":$2}";;
    phys) P="{\"dyn_noise\":$2,\"noise_fields\":[\"q1\",\"q2\"],\"cons_fields\":[\"phi\"],\"mult_fields\":[\"s\",\"c\"]}";;
  esac
  $D/runpack.sh b128_$1_$2 $3 100 128 "$P"
}
for x in "base 0 0" "base 0 1" "plain 0.01 0" "phys 0.01 0" "plain 0.03 0" "phys 0.03 0" "plain 0.01 1" "phys 0.01 1" "plain 0.03 1" "phys 0.03 1" "plain 0.003 0" "phys 0.003 0" "plain 0.1 0" "phys 0.1 0" "plain 0.003 1" "phys 0.003 1" "plain 0.1 1" "phys 0.1 1"; do
  job $x
done
echo BATTERY DONE
