cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 5 "$PY" runjob.py < specs/R4.list >> logs/queue_R4.log 2>&1
echo QUEUE_R4_DONE >> logs/queue_R4.log
