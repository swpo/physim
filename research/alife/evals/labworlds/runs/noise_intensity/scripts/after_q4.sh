#!/bin/bash
# PM dt-halved nulls, then the remaining second-seed behaviour packs, after the FV null queue (pid 6047) exits.
tail --pid=6047 -f /dev/null
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity/scripts
$D/q2.sh "null pm 0.01" "null pm 0.03"
$D/q1.sh "pm 0.03 1" "pm 0.1 1" "fv 0.003 4" "fv 0.01 4" "fv 0.03 4"
