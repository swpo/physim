cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 4 "$PY" runjob.py < specs/R4D.list >> logs/queue_R4D.log 2>&1
echo QUEUE_R4D_DONE >> logs/queue_R4D.log
