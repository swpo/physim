#!/bin/sh
# RED TEAM, by hand (two plain containers of the exam image, no verifiers): does one box's predictor user starve
# another box's predictor of processes? RLIMIT_NPROC is counted per uid across every container that shares the
# host's user namespace, and the driver gives every predictor uid 1000 and the limit 256 (public/_item.py:260).
# The victim predictor starts ONE thread (a thread counts as a process for RLIMIT_NPROC).
# usage: sh nproc_cross_box.sh <vfport dir> <agentenv dir>
# RECORD OF A FIXED FINDING (R6), for the cloud container only; not rerun after the host-safety audit. The driver
# now needs the box marker, the route variable and a uid from 20000-59999 before it drops to a uid, and --no-box
# to run a predictor at all without them, so the `--uid 1000` calls below end in "refused" on today's driver.
# Host safety (audit B5): the two containers get names of this call's own (no `docker rm -f` of a fixed name
# that somebody else might be using), nothing of the host is mounted, and each is removed by exactly its name.
set -u
VF=$1; AE=$2; IMG=physim2-ring:1
SFX=$(od -An -N4 -tx1 /dev/urandom | tr -d ' \n')
X=rt-x-$SFX; Y=rt-y-$SFX
docker run -d --name $Y --entrypoint sleep $IMG infinity >/dev/null || exit 1
docker exec $Y mkdir -p /runtime /w/submission /w/physim2
docker cp $VF/physim2_env/public/_item.py $Y:/runtime/item.py
docker cp $AE/physim2/predict_runner.py $Y:/w/physim2/predict_runner.py
docker exec -i $Y sh -c 'cat > /w/submission/predict.py' <<'PY'
import threading

import numpy as np


def predict(h, p, q, n, s):
    t = threading.Thread(target=len, args=("",))     # one thread, as any JAX or BLAS predictor starts
    t.start()
    t.join()
    return {l: np.zeros((n, len(ts), {1: 6, 2: 3}[l])) for l, ts in q.items()}
PY
docker exec -i $Y python3 - <<'PY'
import json

import numpy as np

np.savez('/runtime/request.npz', history=np.zeros((17, 6)), prefix=np.zeros((16, 24)), test=np.zeros((32, 24)),
         queries=json.dumps({'1': [1, 2], '2': [16]}), n_samples=4, seed=0)
PY
RUN="docker exec $Y python3 -I -B /runtime/item.py --submission /w/submission --runner /w/physim2/predict_runner.py --request /runtime/request.npz --cpu 30 --wall 60 --mem-gib 4 --uid 1000"
echo "alone:        $($RUN | python3 -c 'import sys,json; r=json.loads(sys.stdin.readline()); print({k: r.get(k) for k in ("ok","why","returncode")}, r.get("stderr","")[-90:])')"
# the other box: a predictor-like process (uid 1000, NPROC 256) holding as many sleeping children as it may
docker run -d --name $X --entrypoint python3 $IMG -c "
import os, resource, time
resource.setrlimit(resource.RLIMIT_NPROC, (256, 256)); os.setgroups([]); os.setgid(1000); os.setuid(1000)
n = 0
try:
    while True:
        if os.fork() == 0:
            time.sleep(25); os._exit(0)
        n += 1
except OSError:
    pass
open('/tmp/n', 'w').write(str(n)); time.sleep(25)" >/dev/null
sleep 3
echo "other box holds $(docker exec $X cat /tmp/n) sleeping processes of uid 1000"
echo "meanwhile:    $($RUN | python3 -c 'import sys,json; r=json.loads(sys.stdin.readline()); print({k: r.get(k) for k in ("ok","why","returncode","driver_error")}, r.get("stderr","")[-90:])')"
docker rm -f $X >/dev/null 2>&1
sleep 1
echo "afterwards:   $($RUN | python3 -c 'import sys,json; r=json.loads(sys.stdin.readline()); print({k: r.get(k) for k in ("ok","why","returncode")}, r.get("stderr","")[-90:])')"
docker rm -f $Y >/dev/null 2>&1
