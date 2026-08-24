cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 4 "$PY" runjob.py < specs/XVR.list >> logs/queue_XVR.log 2>&1
echo QUEUE_XVR_DONE >> logs/queue_XVR.log
