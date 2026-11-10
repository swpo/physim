"""RED TEAM, offline and small: what the worker allocates when it parses ONE predictor reply.

_rules.read_reply (public/_rules.py:91-95) refuses a reply whose declared uncompressed size exceeds
8 * max_values + 4096 * (members + 1): the allowance GROWS with the number of members. A reply made of many
4096-byte members of uint8 zeros passes for any count, each member becomes a float64 array 8 times larger in the
worker's process, and the driver lets 64 MiB of reply through (public/_item.py --max-reply-mib). This script
builds such a reply with a SMALL member count, measures the worker-side cost, and scales it to 64 MiB.
Nothing is sent anywhere; run with the port's venv:  python redteam/reply_bomb_offline.py [members]
"""
import io
import json
import os
import resource
import sys
import time
import zipfile

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from physim2_env.public import _rules  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
buf = io.BytesIO()
np.save(buf, np.zeros(4096 - 128, np.uint8))
member = buf.getvalue()
assert len(member) == 4096
raw = io.BytesIO()
with zipfile.ZipFile(raw, "w", zipfile.ZIP_DEFLATED) as z:
    for i in range(n):
        z.writestr(f"level{i}.npy", member)
raw = raw.getvalue()
max_values = 4 * 32 * (5 * 6 + 2 * 3)                        # what grading.py:110 allows for the ring exam
r0, t0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss, time.time()
out = _rules.read_reply(raw, max_values)
dt, r1 = time.time() - t0, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
held = sum(a.nbytes for a in out.values())
per = len(raw) / n
full = int((64 << 20) / per)
print(json.dumps({"members": n, "reply_bytes": len(raw), "accepted_by_read_reply": True, "arrays_held_mib": round(held / 2 ** 20, 1),
                  "rss_growth_mib": round((r1 - r0) / 1024, 1), "seconds": round(dt, 2), "reply_bytes_per_member": round(per, 1),
                  "members_in_a_64_mib_reply": full, "extrapolated_arrays_gib": round(full * held / n / 2 ** 30, 1),
                  "extrapolated_seconds": round(full * dt / n)}))
