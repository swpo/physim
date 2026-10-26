# (c29) one line per screen run: WORLD_P, labkit L rim/core and membrane-like count, final bodies, persistent splits, generation, merges, motion
cd "$(dirname "$0")/screen"
for r in base chi3 chi4 DL24 chi3DL24 chi3kd08 chi4kd08 chi4kd12 chi4kd08dL01 chi5kd08 chi5kd12 chi5mu10 chi5mu10kd12 chi5mu125 chi6mu10 chi7mu10; do
  f=$r/FACTS.md
  echo "$r | $(grep -o '"N".*}' $f | head -1) | L $(grep -o 'radial L link.*' $f | grep -o 'rim/core [0-9.]*\|[0-9]*/[0-9]* membrane-like' | tr '\n' ' ') | $(grep -o 'components: final [0-9]*' $f) | $(grep -o 'persistent splits [0-9]*' $f), $(grep -o 'max generation [0-9]*, merges [0-9]*' $f) | $(grep -o 'motion:.*' $f | cut -c9-)"
done
