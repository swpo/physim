#!/bin/sh
# harness_setup.sh IMAGE DIR -- replay the stock bash harness's set-up in a throwaway container that has NO
# network and a read-only root, from the two files tests/harness_setup_command.py wrote into DIR.
# The container gets no mount of a host folder (the program arrives on stdin), no privilege and no Docker socket;
# it is removed by its exact name. Prints one JSON line.
set -u
IMG=$1; DIR=$2; NAME=physim2-harness-setup-$$
CMD=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['command'])" "$DIR/setup.json")
TMP=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['tmp'])" "$DIR/setup.json")
SDIR=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['scripts_dir'])" "$DIR/setup.json")
docker run --rm -i --name "$NAME" --network none --read-only --tmpfs /tmp:rw,exec,nosuid,nodev,size=512m,mode=1777 \
  --env UV_OFFLINE=false --entrypoint sh "$IMG" -c "
    set -e
    mkdir -p '$SDIR' && cat > '$TMP'
    t0=\$(date +%s%N)
    out=\$( { $CMD ; } 2>/tmp/setup.err ) || { echo '{\"setup_exit\": 1}'; cat /tmp/setup.err >&2; exit 1; }
    t1=\$(date +%s%N)
    py=\$(printf '%s\n' \"\$out\" | tail -n 1)
    \"\$py\" -B $SDIR/*.py --help > /tmp/help.out 2>/tmp/help.err; rc=\$?
    routes=\$(cat /proc/net/route 2>/dev/null | wc -l)
    printf '{\"setup_exit\": 0, \"interpreter\": \"%s\", \"setup_ms\": %s, \"program_help_exit\": %s, \"program_help_lines\": %s, \"routes_in_the_box\": %s, \"tmp_kib_used\": %s, \"root_writable\": %s}\n' \
      \"\$py\" \$(( (t1 - t0) / 1000000 )) \$rc \$(wc -l < /tmp/help.out) \$(( routes > 0 ? routes - 1 : 0 )) \$(du -sk /tmp | cut -f1) \$( (touch /root/.probe 2>/dev/null && echo true) || echo false )
  " < "$DIR/program.py"
