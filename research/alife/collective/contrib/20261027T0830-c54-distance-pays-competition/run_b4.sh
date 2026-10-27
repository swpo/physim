source /tmp/claude-0/c54/run.sh
until [ -f $O/E/seed602/metrics.json ] && [ -f $O/glob/seed602/metrics.json ]; do sleep 10; done
D='"ARM":"S","DEP":1,"dep_in":-0.7'
run off 600 "{$D,\"MARS\":[0,0,0]}" & run off 601 "{$D,\"MARS\":[0,0,0]}"; wait
W=/tmp/claude-0/c54/w2/world.py
for s in 610 611; do
run cdep $s "{$D,\"FOUNDER\":-2,\"mu\":0}" & run cdeptwin $s "{$D,\"FOUNDER\":-2,\"mu\":0,\"MARS\":[40,40,40]}"; wait
run cE $s '{"ARM":"S","FOUNDER":-2,"mu":0}' & run cEtwin $s '{"ARM":"S","FOUNDER":-2,"mu":0,"MARS":[40,40,40]}'; wait
done
