cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg PYQ=$PY
cat queue_PULL.jsonl | while IFS= read -r line; do printf '%s\0' "$line"; done |   xargs -0 -n1 -P 7 -I{} sh -c "$PY runjob.py \"\$1\" >> logs/queue_PULL.log 2>&1" _ {}
echo QUEUE_PULL_DONE >> logs/queue_PULL.log
