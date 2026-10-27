source /tmp/claude-0/c54/run.sh
until grep -q done /tmp/claude-0/c54/rev2.log; do sleep 10; done
W=/tmp/claude-0/c54/w2/world.py
D='"ARM":"S","DEP":1,"dep_in":-0.7,"mu":0'
run m40dep 620 "{$D,\"FOUNDER\":1}" & run m60dep 620 "{$D,\"FOUNDER\":2}"; wait
run m40dep 621 "{$D,\"FOUNDER\":1}" & run m60dep 621 "{$D,\"FOUNDER\":2}"; wait
run m40E 620 '{"ARM":"S","mu":0,"FOUNDER":1}' & run m60E 620 '{"ARM":"S","mu":0,"FOUNDER":2}'; wait
echo done
