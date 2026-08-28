
import os, time
os.environ["BLOBKIT_SKIP_LOCK"] = "1"

def main():
    from concurrent.futures.process import BrokenProcessPool
    import blobkit.assay_batch as ABM
    from blobkit import worlds

    class SabotagedPool:
        def __init__(self):
            self.calls = 0
            self._broken = False
        def map(self, fn, payloads):
            self.calls += 1
            self._broken = "sabotage"
            raise BrokenProcessPool("sabotage")
        def shutdown(self, wait=True, cancel_futures=False):
            if wait and self._broken:
                raise RuntimeError("would deadlock: shutdown(wait=True) on broken pool")
            self.shut = (wait, cancel_futures)

    sab = SabotagedPool()
    import concurrent.futures as CF
    orig = CF.ProcessPoolExecutor
    class FakePPE:
        def __new__(cls, *a, **k):
            return sab
    ABM.ProcessPoolExecutor = FakePPE

    g = worlds.load("m0")
    outs = ABM.run_assay_batch([(g, 7), (g, 3)], dtype="f32", verbose=False,
                               battery_procs=2, cap=2500.0)
    ABM.ProcessPoolExecutor = orig
    for o in outs:
        print("out:", round(o["interest"], 2), o["horizon"]["T_used"],
              o["horizon"]["why_stopped"])
        assert o["horizon"]["why_stopped"] in ("static", "converged")
    assert sab.calls == 1, sab.calls
    assert getattr(sab, "shut", None) == (False, True), getattr(sab, "shut", None)
    print("BROKEN-POOL FALLBACK TEST PASS (serial fallback + non-waiting shutdown)")

if __name__ == "__main__":
    main()
