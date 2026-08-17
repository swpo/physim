
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest")
from ff_core import *
from hier_metrics import save_strip

for tag, kw in [
    ("A_hom_rare",  dict(Lam=5,  theta=0.6, M=3, D=4, gsig=0.0)),
    ("B_hom_mid",   dict(Lam=30, theta=0.6, M=3, D=4, gsig=0.0)),
    ("C_het_mid",   dict(Lam=30, theta=0.6, M=3, D=4, gsig=0.7)),
    ("D_het_many",  dict(Lam=150,theta=0.6, M=3, D=4, gsig=0.7)),
]:
    out = run(L=64, T=30000, g=1e-3, seed=0, **kw)
    res = measure(out, drop=6000)
    print("%-11s rt=%4.1fs B=[%.2f,%.2f] F=%.4f top=%s r2=%.3f tp=%s" % (
        tag, out["runtime"], res["B_lo"], res["B_hi"], res["meanF_mean"],
        res["top_model"], res["top_r2"],
        {k: (round(v,1) if isinstance(v,float) else v) for k,v in res["top_params"].items()}))
    print("            nev=%d szmax=%s szmed=%s tau1=%s tau2=%s tau3=%s sep21=%s sep32=%s" % (
        res["n_events"], res["size_max"], res.get("size_med"),
        None if res["tau1"] is None else round(res["tau1"],1),
        None if res["tau2"] is None else round(res["tau2"],1),
        None if res["tau3"] is None else round(res["tau3"],1),
        None if res["sep21"] is None else round(res["sep21"],1),
        None if res["sep32"] is None else round(res["sep32"],1)))
    print("            pl=%s" % (res["pl"],))
    np.save("/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/logs/mB_%s.npy" % tag, out["meanB"])
