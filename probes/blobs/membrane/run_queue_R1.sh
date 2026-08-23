cd /Users/spoho/Documents/prime/test/physim/probes/blobs/membrane
PY=/Users/spoho/Documents/prime/test/physim/.venv/bin/python
export MPLBACKEND=Agg
cat queue_R1.jsonl | while IFS= read -r line; do printf '%s\0' "$line"; done |   xargs -0 -n1 -P 8 -I{} sh -c '$PY runjob.py "$1" >> logs/queue_R1.log 2>&1' _ {}
echo QUEUE_R1_DONE >> logs/queue_R1.log
