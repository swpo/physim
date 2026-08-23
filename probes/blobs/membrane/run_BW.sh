cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 6 "$PY" runjob.py < specs/BW.list >> logs/queue_BW.log 2>&1
echo QUEUE_BW_DONE >> logs/queue_BW.log
