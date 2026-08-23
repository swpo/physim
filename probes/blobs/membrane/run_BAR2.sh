cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
xargs -n1 -P 7 -I@@ "$PY" runjob.py @@@ < specs/BAR2.list >> logs/queue_BAR2.log 2>&1
echo QUEUE_BAR2_DONE >> logs/queue_BAR2.log
