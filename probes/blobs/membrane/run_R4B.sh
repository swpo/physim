cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 4 "$PY" runjob.py < specs/R4B.list >> logs/queue_R4B.log 2>&1
echo QUEUE_R4B_DONE >> logs/queue_R4B.log
