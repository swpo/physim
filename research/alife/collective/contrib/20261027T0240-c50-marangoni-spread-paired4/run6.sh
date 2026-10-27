#!/bin/bash
source <(sed -n "1,5p" /tmp/claude-0/sp/run2.sh)
run E 502 '{"ARM":"S"}' & run twin 502 '{"ARM":"S","MARS":[40,40,40]}'; wait
run E 503 '{"ARM":"S"}' & run twin 503 '{"ARM":"S","MARS":[40,40,40]}'; wait
echo done
