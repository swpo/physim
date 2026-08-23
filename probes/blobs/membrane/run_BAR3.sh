cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 7 "$PY" runjob.py < specs/BAR3.list >> logs/queue_BAR3.log 2>&1
echo QUEUE_BAR3_DONE >> logs/queue_BAR3.log
