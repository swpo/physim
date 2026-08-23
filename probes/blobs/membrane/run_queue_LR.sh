cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
cat queue_LR.jsonl | while IFS= read -r line; do printf '%s\0' "$line"; done |   xargs -0 -n1 -P 7 -I{} sh -c "$PY runjob.py \"\$1\" >> logs/queue_LR.log 2>&1" _ {}
echo QUEUE_BAR_DONE >> logs/queue_LR.log
