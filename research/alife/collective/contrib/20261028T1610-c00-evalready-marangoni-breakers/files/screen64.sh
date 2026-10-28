#!/usr/bin/env bash
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/marangoni
job() {
  case $1 in
    base) P='{"dyn_noise":0}';;
    plain) P="{\"dyn_noise\":$2}";;
    phys) P="{\"dyn_noise\":$2,\"noise_fields\":[\"q1\",\"q2\"],\"cons_fields\":[\"phi\"],\"mult_fields\":[\"s\",\"c\"]}";;
  esac
  $D/runpack.sh scr64_$1_$2 0 100 64 "$P"
}
export -f job; export D
printf "base 0\nplain 0.1\nplain 0.3\nplain 1.0\nphys 0.1\nphys 0.3\nphys 1.0\n" | xargs -P 2 -n 2 bash -c 'job "$0" "$1"'
echo SCREEN DONE
