#!/bin/bash
# dt-halved null ensembles for the fed vortices, after the behaviour queue (pid 4704) exits.
tail --pid=4704 -f /dev/null
/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity/scripts/q2.sh "null fv 0.003" "null fv 0.01" "null fv 0.001"
