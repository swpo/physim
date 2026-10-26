set -x
run(){ WORLD_P="$2" python -m labkit.run collective/contrib/20261026T0655-c34-two-kinds-swap/world.py --out collective/contrib/wip-c37/twok/$1 --seeds $3 --no-movie > collective/contrib/wip-c37/twok/log_${1////_}.txt 2>&1; }
for s in 20 21; do
 run Aswims/s$s '{"mar":40.0,"marB":0.0}' $s &
 run neutral/s$s '{"mar":40.0,"marB":40.0}' $s &
 wait
 run Bswims/s$s '{"mar":0.0,"marB":40.0}' $s
done
