cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 2 "$PY" runjob.py < specs/R4E.list >> logs/queue_R4E.log 2>&1
echo QUEUE_R4E_DONE >> logs/queue_R4E.log
