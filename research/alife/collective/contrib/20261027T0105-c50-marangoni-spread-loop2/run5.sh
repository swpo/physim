#!/bin/bash
source <(sed -n "1,5p" /tmp/claude-0/sp/run2.sh)
run E 501 '{"ARM":"S"}' & run offfast 501 '{"ARM":"S","disc_v":0.16,"MARS":[0,0,0]}'; wait
run twin 501 '{"ARM":"S","MARS":[40,40,40]}' & run Cfast 501 '{"ARM":"I","disc_v":0.16}'; wait
echo done
