"""blobkit._batteryproc — the battery pool worker, in a deliberately tiny
module (blobkit 0.3.1).

run_assay_batch's ProcessPoolExecutor uses the SPAWN context (forking after
JAX/CUDA init is undefined and killed workers on GPU hosts — the 0.3.0 fleet
bug). A spawned worker imports the module that defines its function: keeping
the function HERE (instead of in assay_batch) means workers import only
blobkit.__init__ + this module + (inside the call) metrics_v2/assay_v2 —
i.e. the numpy/scipy metrics chain. Never jax, never sim_gpu, never the
executor machinery.
"""


def battery_worker(args):
    """LOCKED battery + LOCKED criteria for one lane (CPU, pool-safe).
    Exceptions are captured per lane (a no_blobs-style battery crash on one
    lane must not abort the other B-1 lanes; the singles path lets it
    propagate to the caller — pod_lib.evaluate catches it there)."""
    from . import metrics_v2 as MV2               # jax-free import chain
    from .assay_v2 import horizon_criteria
    rec, genome = args
    try:
        out = MV2.full_battery(dict(rec), genome=genome)
        crit = horizon_criteria(rec, genome, D=out["D"])
        return out, crit, None
    except Exception as e:                        # contained, reported per lane
        return None, None, repr(e)[:300]
