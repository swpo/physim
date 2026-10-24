#!/bin/bash
# mkevo3.sh <id> <arm> <kick_rate> (+ imposed dilution) "<extra genome kwargs as python>" "<note>"
id=$1; arm=$2; kr=$3; kw="$4"; note=$5
P=../../.labenv/bin/python
$P -c "
import json, evo
json.dump(evo.genome('$arm', $kw), open('/tmp/claude-0/g_$id.json','w'))"
$P mkworld.py $id "xcell-her (sprint 1); maintenance/turnover idea from lenia-multichannel mcfd-MIRd; 5-px mutation patches + neutral arm from active-droplets ad5" "Arm $arm of the sprint-2 evolution experiment. xcell-her minus its unused hdep channel plus one membrane-gated waste q (tau=40, D=2, K=0.15; turnover). Turnover is IMPOSED: chemostat-style dilution erases a random disk (radius 5) at Poisson rate KILL_RATE, identically in every arm. No marker is planted: h-on kinds arise only from rare cell-scale h kicks (Poisson, rate $kr per time unit, Gaussian disk sigma 1.5, amplitude 2.5, anywhere in the box). Only bodies (+ v, w dress) are planted. $note" /tmp/claude-0/g_$id.json --channels '["u (body)","m (CH membrane)","h (marker)","q (waste)"]' --render '[0,4,1,8]' --soup 10 --acts '[0]' --dress '[0,1]' --spf 200 --n 128
cat >> worlds/$id/world.py <<PYEOF

KICK_RATE = $kr      # marker kicks per unit time (whole box)
KILL_RATE, KILL_R = 0.1, 5.0   # imposed dilution: disk erasures per unit time, radius (units)
KICK_SIG, KICK_AMP = 1.5, 2.5
_base_init, _base_step = init, step


def init(seed, size):
    S = _base_init(seed, size)
    S["krng"] = np.random.default_rng(10_000 + seed)
    S["kicks"] = []
    S["kills"] = []
    return S


def step(S):
    S = _base_step(S)
    r = S["krng"]
    if r.random() < KICK_RATE * S["dt"]:
        L = S["N"] * S["dx"]
        y, x = r.uniform(0, L, 2)
        poke(S["F"], 1, y, x, KICK_AMP, KICK_SIG, S["dx"])
        S["kicks"].append((S["t"] * S["dt"], float(y), float(x)))
    if r.random() < KILL_RATE * S["dt"]:
        N, dx = S["N"], S["dx"]
        y, x = r.uniform(0, N, 2)
        yy = (np.arange(N)[:, None] - y + N / 2) % N - N / 2
        xx = (np.arange(N)[None, :] - x + N / 2) % N - N / 2
        damage(S, yy ** 2 + xx ** 2 < (KILL_R / dx) ** 2)
        S.setdefault("kills", []).append((S["t"] * S["dt"], float(y), float(x)))
    return S
PYEOF
