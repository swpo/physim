import os, sys, json
os.environ["JAX_PLATFORMS"] = "cpu"
os.chdir("/tmp/blobkit_smoke/bundle")
json.dump(dict(island=0, out_dir="out", sim_backend="gpu_batch",
               record_mode="device", apply_mode="async"),
          open("island_config.json", "w"))
os.makedirs("out", exist_ok=True)
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "lib"))
import pod_lib as PL
cfg = PL.config()
if cfg.get("record_mode") == "device":
    from blobkit.soup import devrec_proto as _DR
    _DR.install(async_apply=(cfg.get("apply_mode") == "async"))
    print("hook fired: devrec installed")
from blobkit.soup import driver as DRV, devrec_proto as DR
wrapped = DRV.run_chunks is not DR._STATE["orig"] and DR._STATE["orig"] is not None
print("driver wrapped:", wrapped)
DR.uninstall()
print("HOOK_SMOKE:", "PASS" if wrapped else "FAIL")
