#!/bin/bash
# mkevo.sh <id> <wqh> <noise> <kw> "<note>"
id=$1; wqh=$2; nz=$3; kw=$4; note=$5
P=../../.labenv/bin/python
$P -c "
import json, s_her
json.dump(s_her.her(kb=0.25, kh=0.0, kc=0.25, kw=$kw, wqh=$wqh), open('/tmp/claude-0/g_$id.json','w'))"
$P mkworld.py $id "xcell-her-noise0.3 (+ resource/maintenance idea from the lenia-multichannel and autopoiesis threads)" "xcell-her + additive activator noise $nz (marker loss at unequal division = in-run variation) + a membrane-trapped waste q (tau=40, D=2, K=$kw) as a maintenance cost that gives continual death and birth. The marker changes waste production by W[q,h]=$wqh. $note" /tmp/claude-0/g_$id.json --channels '["u (body)","m (CH membrane)","h (marker)","q (waste)"]' --render '[0,4,1,9]' --soup 10 --acts '[0]' --spf 200
cat >> worlds/$id/world.py <<PYEOF

_base_init = init


def init(seed, size):
    """Planted bodies + an h poke in a random half of them; activator noise switched on."""
    from scipy import ndimage
    S = _base_init(seed, size)
    F, dx = S["F"], 0.5
    z = F[0] - S["u0"][0]
    lab, k = ndimage.label(z > 0.5)
    cs = ndimage.center_of_mass(z, lab, range(1, k + 1))
    rng = np.random.default_rng(seed + 100)
    for j in rng.permutation(k)[:int(round(0.5 * k))]:
        poke(F, 1, cs[j][0] * dx, cs[j][1] * dx, 2.2, 2.5, dx)
    S["noise"] = $nz
    return S
PYEOF
