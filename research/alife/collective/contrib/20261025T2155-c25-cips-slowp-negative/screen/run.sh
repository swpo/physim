#!/bin/bash
# usage: run.sh tag json  -> labkit run seed 0 (or $SEED), 128^2, t=3000
D="$(cd "$(dirname "$0")" && pwd)"; cd "$D/../../../.."; S=${SEED:-0}
WORLD_P="$2" python -m labkit.run "$D/../world.py" --out "$D/$1" --seeds $S --size 128 128 --frames ${FR:-300} --no-movie > "$D/$1.log" 2>&1
echo "$1 $2 $(grep -E '^- (components|replication)' "$D/$1/FACTS.md" | sed 's/(lineage[^)]*)//' | tr '\n' ' ')"
