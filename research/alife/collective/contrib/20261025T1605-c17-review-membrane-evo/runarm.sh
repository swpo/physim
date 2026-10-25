arm=$1; shift; for s in "$@"; do python -m labkit.run $R/world_$arm.py --out $R/$arm/seed$s --seeds $s --frames 160 --spf 250 --no-movie > /dev/null 2>&1; echo "$arm $s done"; done
