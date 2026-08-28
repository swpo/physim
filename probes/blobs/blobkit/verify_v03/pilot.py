"""verify_v03 pilot: CPU-jax speed check, f32+f64, 4 lanes, 250tu."""
import os, time, json
os.environ.setdefault("BLOBKIT_RESULTS", "")
from blobkit import worlds
from blobkit.soup import sim_gpu as SG

def timed(dtype):
    jobs = [(worlds.WORLDS[w](), s) for w, s in
            [("m0", 7), ("m4", 1), ("m4", 2), ("coex", 2)]]
    t0 = time.time()
    SS = SG.init_soup_gpu_batch(jobs, dtype=dtype)
    t1 = time.time()
    SG.advance_gpu_batch(SS, 250.0)
    t2 = time.time()
    SG.advance_gpu_batch(SS, 500.0)
    t3 = time.time()
    return dict(dtype=dtype, init=round(t1-t0,1), first250=round(t2-t1,1),
                second250=round(t3-t2,1),
                tu_per_s_warm=round(250*4/(t3-t2),1))

out = [timed("f32"), timed("f64")]
json.dump(out, open(os.path.join(os.path.dirname(__file__), "pilot.json"), "w"), indent=1)
print(json.dumps(out))
