"""Re-seal every lab bundle after a formatting-only change to labworld.py / labbundle.py.

Uses each recipe's own manifest writer (gc_bundle.write_manifest with Inputs from the bundle's source suite;
fedvortex via reseal_fedvortex.py separately). checks.json and every data file stay as they are; only the
world implementation hashes and the ids built on them change. Then: open both profiles, check_runtime,
every truth readable, and member 0 of the last case re-simulated bit for bit (gc_bundle.verify).
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
sys.path.insert(0, "/home/user/swpo/residency-environments/scripts/physim/labworlds")
import gc_bundle as G
from physim import labbundle as LB

ROOT = Path("/home/user/evalwork/bundles")
out = {}
for name in sys.argv[1:]:
    b = ROOT / name
    before = json.loads((b / "manifest.json").read_text())
    data_before = {r["path"]: r["sha256"] for r in before["files"]}
    suite_dir = Path(json.loads((ROOT / "work" / name / "build.json").read_text())["suite_dir"])
    manifest = G.write_manifest(b, G.Inputs(suite_dir))
    data_after = {r["path"]: r["sha256"] for r in manifest["files"]}
    ev = LB.open_bundle(b, profile="evaluation"); ev.check_runtime()
    for rec in ev.suite["cases"]:
        ev.truth(rec)
    LB.open_bundle(b, profile="simulation").check_runtime()
    last = ev.suite["cases"][-1]["request"]["id"]
    v = G.verify(b, last, ROOT / "work" / name / "reseal_verify.json")
    out[name] = dict(old=before["bundle_id"], new=manifest["bundle_id"], data_files_unchanged=data_before == data_after,
                     resim_case=last, bit_identical=v["bit_identical"], cpu_s=round(v["cpu_s"], 1))
    print(name, json.dumps(out[name]), flush=True)
p = ROOT / "work" / "reseal_all.json"
prev = json.loads(p.read_text()) if p.exists() else {}
prev.update(out)
p.write_text(json.dumps(prev, indent=1))
