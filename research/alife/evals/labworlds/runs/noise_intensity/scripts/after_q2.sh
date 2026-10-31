#!/bin/bash
# Second-seed behaviour packs, started only after the score queue (pid 4603) exits: one heavy process at a time.
tail --pid=4603 -f /dev/null
/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity/scripts/q1.sh "pm 0.003 0" "pm 0.003 1" "pm 0.01 1" "pm 0.03 1" "pm 0.1 1" "fv 0.001 3" "fv 0.003 4" "fv 0.01 4" "fv 0.03 4"
