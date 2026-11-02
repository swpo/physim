"""Open every bundle the way a rollout does; explain any mismatch.  Run inside the physim environment
(e.g. `uv run python check_kit.py` from residency-environments/environments/physim)."""
import json
import sys
from pathlib import Path

from physim import labbundle as LB

kit = Path(__file__).resolve().parent
expected = json.loads((kit / "bundle_ids.json").read_text())
here = LB.implementation_identity()
bad = 0
for name, bid in expected.items():
    root = kit / "bundles" / name
    try:
        b = LB.open_bundle(root, profile="evaluation")
        assert b.manifest["bundle_id"] == bid, "bundle id differs from bundle_ids.json"
        b.check_runtime()
        for rec in b.suite["cases"]:
            b.truth(rec)
        print(f"ok   {name:18s} {bid[:30]}  {len(b.suite['cases'])} cases")
    except Exception as exc:
        bad += 1
        print(f"FAIL {name:18s} {type(exc).__name__}: {exc}")
        want = json.loads((root / "manifest.json").read_text())["objects"]["world"]["implementation"]
        for k in ("source_sha256", "dependencies"):
            for m, v in want[k].items():
                if here[k].get(m) != v:
                    print(f"     {k}.{m}: bundle wants {v}, this environment has {here[k].get(m)}")
sys.exit(1 if bad else 0)
