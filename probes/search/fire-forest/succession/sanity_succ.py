
import sys, numpy as np
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search")
sys.path.insert(0, "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession")
from sf_core import run
from sf_measure import measure4, gates4
from hier_metrics import save_strip
SD = "/Users/spoho/Documents/prime/test/physim/probes/search/fire-forest/succession"

# defaults: g=2e-3, gT=1e-4 (R=0.05), mu=1.5e-5 (W=0.15), kapT=1.5, Tm=0.45, rhoT=0.03
base = dict(g=2e-3, gT=1e-4, mu=1.5e-5, kapT=1.5, Tm=0.45, rhoT=0.03)
for init in ("savanna", "forest", "mixed"):
    out = run(L=64, T_ticks=50000, seed=0, init=init, snap_times=(2000, 25000, 49000), **base)
    res = measure4(out, drop=10000)
    print("== init=%s rt=%.1fs" % (init, out["runtime"]))
    print("  T: %.3f -> %.3f  fracF_end=%.3f drift=%.3f" % (
        res["T_start"], res["T_end"], res["fracF_end"], res["fracF_last20_drift"]))
    print("  L3: %s r2=%.3f tau3=%s | FRI grass=%s (n=%d) forest=%s (n=%d)" % (
        res["L3_model"], res["L3_r2"],
        "%.0f" % res["tau3"] if res["tau3"] else "-",
        "%.0f" % res["fri_grass_med"] if res["fri_grass_med"] else "-", res["n_fri_grass"],
        "%.0f" % res["fri_forest_med"] if res["fri_forest_med"] else "-", res["n_fri_forest"]))
    print("  L4: model=%s r2=%.3f relax=tau %s r2 %.3f | nev=%d tau1=%s tau2=%s" % (
        res["L4_model"], res["L4_r2"],
        "%.0f" % res["L4_relax"]["tau"] if res["L4_relax"]["tau"] else "-",
        res["L4_relax"]["r2"], res["n_events"],
        "%.1f" % res["tau1"] if res["tau1"] else "-",
        "%.0f" % res["tau2"] if res["tau2"] else "-"))
    print("  seps: 21=%s 32=%s 43=%s span41=%s" % tuple(
        ("%.1f" % res[k]) if res.get(k) else "-" for k in ("sep21","sep32","sep43","span41")))
    sn = out["snaps"]; ts = sorted(sn)
    save_strip([sn[t][2] for t in ts], SD + "/strips/sanity_%s_T.png" % init,
               titles=["T t=%d" % t for t in ts], cmap="YlGn", vmax=1.0)
    save_strip([sn[t][0] for t in ts], SD + "/strips/sanity_%s_B.png" % init,
               titles=["B t=%d" % t for t in ts], cmap="Greens", vmax=1.0)
    np.save(SD + "/logs/sanity_%s_meanT.npy" % init, out["meanT"])
    np.save(SD + "/logs/sanity_%s_phi.npy" % init, out["phi"])
    np.save(SD + "/logs/sanity_%s_fracF.npy" % init, out["fracForest"])
print("done")
