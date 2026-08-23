cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 7 "$PY" runjob.py < specs/BC.list >> logs/queue_BC.log 2>&1
echo QUEUE_BC_DONE >> logs/queue_BC.log
