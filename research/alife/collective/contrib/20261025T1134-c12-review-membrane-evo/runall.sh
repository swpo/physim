for s in 31 32 33; do
  for a in up twin down; do python -m labkit.run $R/world_$a.py --out $R/arm_$a/seed$s --seeds $s --frames 160 --spf 250 --no-movie > /dev/null 2>&1 & done; wait
done
