import json, os, sys
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/complexity")
import assay_v2
g = json.load(open("/Users/spoho/Documents/prime/test/physim/probes/blobs/l0/complexity/genomes_v2/ds3_014.json"))
for wk in (1, 2):
    out = assay_v2.run_assay(g, seed=2, workers=wk, cap=2500.0,
                             results_path=None, tag=f"wk{wk}", verbose=True)
    print(f"workers={wk}: I={out['interest']:.2f} why={out['horizon']['why_stopped']}", flush=True)
print("WORKERTEST_DONE")
