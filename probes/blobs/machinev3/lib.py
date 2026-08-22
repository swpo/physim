"""machinev3/lib.py — combined-world builder + placement + tow measurement.

World = block direct-sum (operators_lib._block_merge) of:
  g1 = engine_10748 (act E=0; chans v_e=0, w_e=1)
  g2 = s2_128_26    (acts C=1, dead=2; chans c0=2, c1t=3, c2=4)
Coupling moves (one per variant) are applied to the merged W/K by name.
"""
import copy, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOBS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(BLOBS, "l0", "stage2", "lib"))
sys.path.insert(0, os.path.join(BLOBS, "l0", "evolve"))
import genome as G
import operators_lib as OPS

POKE_AMP, POKE_SIG = 2.0, 3.0
ENGINE_PATH = os.path.join(BLOBS, "l0", "stage3", "engine_10748.json")
MERGED_PATH = os.path.join(BLOBS, "l0", "stage2", "merged_results.json")
RESULTS = os.path.join(HERE, "results.json")

# merged-world indices
ACT_E, ACT_C, ACT_D = 0, 1, 2
CH_VE, CH_WE, CH_C0, CH_C1T, CH_C2 = 0, 1, 2, 3, 4


def load_parts():
    eng = json.load(open(ENGINE_PATH))
    for r in json.load(open(MERGED_PATH)):
        if isinstance(r, dict) and r.get("cand") == "s2_128_26_uni":
            return eng, copy.deepcopy(r["genome"])
    raise RuntimeError("cargo genome not found")


def engine_variant(eng, variant="base"):
    e = copy.deepcopy(eng)
    if isinstance(variant, dict):
        e["acts"][0]["Du"] *= variant.get("Du_mul", 1.0)
        e["chans"][0]["D"] *= variant.get("Dv_mul", 1.0)
        e["chans"][0]["tau"] *= variant.get("tauv_mul", 1.0)
        e["chans"][1]["D"] *= variant.get("Dw_mul", 1.0)
        return e
    if variant == "du11":
        e["acts"][0]["Du"] *= 1.1
    elif variant == "du11_dv09":
        e["acts"][0]["Du"] *= 1.1
        e["chans"][0]["D"] *= 0.9
    elif variant == "du09":
        e["acts"][0]["Du"] *= 0.9
    elif variant == "dv110":
        e["chans"][0]["D"] *= 1.1
    elif variant == "du09_dv110":
        e["acts"][0]["Du"] *= 0.9
        e["chans"][0]["D"] *= 1.1
    elif variant != "base":
        raise ValueError(variant)
    return e


def build_world(coupling="none", eta=0.0, engine="base", cargo_mod=None):
    """Merged genome + one named coupling move.
    Moves (eta sign as given; cargo K rows are all +, x>0 suppresses u_C):
      none        : pure direct sum (control)
      xv_sym      : W[v_e,C]=eta and W[c0,E]=eta   (operators cross_edge)
      e2c_c0      : W[c0,E]=eta                    (engine writes cargo spacer c0)
      e2c_c2      : W[c2,E]=eta                    (engine writes strong repeller c2)
      e2c_c1t     : W[c1t,E]=eta                   (engine writes binder tanh)
      c2e_v       : W[v_e,C]=eta                   (cargo writes engine slow v)
      mimic       : W[c,E]=eta*W[c,C] for c in {c0,c1t,c2} (engine = weak pseudo-cargo)
      kx_e        : K[E,c0]=eta                    (engine u feels cargo spacer)
      kw_c        : K[C,w_e]=eta                   (cargo feels engine wide w; +plow/-tractor)
      mimic_kw    : mimic@0.6 + K[C,w_e]=eta
    """
    eng, cargo = load_parts()
    eng = engine_variant(eng, engine)
    M, dims = OPS._block_merge(eng, cargo)
    W = np.asarray(M["W"], float); K = np.asarray(M["K"], float)
    if coupling == "none":
        pass
    elif coupling == "xv_sym":
        W[CH_VE, ACT_C] = eta; W[CH_C0, ACT_E] = eta
    elif coupling == "e2c_c0":
        W[CH_C0, ACT_E] = eta
    elif coupling == "e2c_c2":
        W[CH_C2, ACT_E] = eta
    elif coupling == "e2c_c1t":
        W[CH_C1T, ACT_E] = eta
    elif coupling == "c2e_v":
        W[CH_VE, ACT_C] = eta
    elif coupling == "mimic":
        for ch in (CH_C0, CH_C1T, CH_C2):
            W[ch, ACT_E] = eta * W[ch, ACT_C]
    elif coupling == "e2c_c0c1t":
        W[CH_C0, ACT_E] = eta; W[CH_C1T, ACT_E] = eta
    elif coupling == "e2c_c0c2":
        W[CH_C0, ACT_E] = eta; W[CH_C2, ACT_E] = eta
    elif coupling == "e2c_c1tc2":
        W[CH_C1T, ACT_E] = eta; W[CH_C2, ACT_E] = eta
    elif coupling == "kx_e":
        K[ACT_E, CH_C0] = eta
    elif coupling == "kw_c":
        K[ACT_C, CH_WE] = eta         # cargo u reads engine long-range w (+: plow, -: tractor)
    elif coupling == "mimic_kw":
        for ch in (CH_C0, CH_C1T, CH_C2):
            W[ch, ACT_E] = 0.6 * W[ch, ACT_C]
        K[ACT_C, CH_WE] = eta
    else:
        raise ValueError(coupling)
    if cargo_mod:
        # applied AFTER coupling wiring: mimic imprint keeps ORIGINAL W values
        W[CH_C2, ACT_C] *= cargo_mod.get("Wc2_mul", 1.0)
        W[CH_C0, ACT_C] *= cargo_mod.get("Wc0_mul", 1.0)
        K[ACT_C, CH_C2] *= cargo_mod.get("Kc2_mul", 1.0)
        K[ACT_C, CH_C1T] *= cargo_mod.get("Ktanh_mul", 1.0)
    M["W"] = W.tolist(); M["K"] = K.tolist()
    ev = engine if isinstance(engine, str) else "dials" + json.dumps(engine, sort_keys=True)
    M["id"] = f"mv3_{ev}_{coupling}_{eta}"
    M["provenance"] = dict(kind="machinev3", op="block_sum+" + coupling,
                           eta=eta, engine=engine,
                           parents=["engine_10748", "s2_128_26_uni"])
    probs = G.validate(M)
    if probs:
        raise RuntimeError(f"validate: {probs}")
    return M


def place_engine(F, g, x, y, dx, kick_px=0.5, dress=0.6):
    """Kicked+dressed engine poke at (x,y): channel shadows displaced -x
    (a1_poke dressed-kick convention) -> engine travels +x."""
    N = F.shape[1]; L = N * dx
    W = np.asarray(g["W"], float); na = len(g["acts"])
    F = G.poke(F, g, ACT_E, x, y, POKE_AMP, POKE_SIG, dx)
    c = (np.arange(N) + 0.5) * dx
    dyy = G.min_image(c - y, L)[:, None]
    dxx = G.min_image(c - (x - kick_px), L)[None, :]
    bump = POKE_AMP * np.exp(-(dyy ** 2 + dxx ** 2) / (2 * POKE_SIG ** 2))
    for ci, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and W[ci, ACT_E] != 0.0:
            F[na + ci] += dress * W[ci, ACT_E] * bump
    return F


def place_cargo(F, g, x, y, dx, dress=0.6):
    """Dressed cargo poke (stack_probe convention)."""
    N = F.shape[1]
    W = np.asarray(g["W"], float); na = len(g["acts"])
    F0 = F[ACT_C].copy()
    F = G.poke(F, g, ACT_C, x, y, POKE_AMP, POKE_SIG, dx)
    bump = F[ACT_C] - F0
    for ci, ch in enumerate(g["chans"]):
        if ch["g"] == "id" and W[ci, ACT_C] != 0.0:
            F[na + ci] += dress * W[ci, ACT_C] * bump
    return F


def sep_series(r, n_cargo=1):
    """t, xe, ye, xc_com, sep(E,nearest C), nce, ncc from a run record."""
    t = np.asarray(r["t"], float)
    nce = np.asarray(r[f"ncomp{ACT_E}"], int)
    ncc = np.asarray(r[f"ncomp{ACT_C}"], int)
    n = min(len(t), len(nce), len(ncc), len(r[f"pos{ACT_E}"]), len(r[f"pos{ACT_C}"]))
    xe = np.full(n, np.nan); ye = np.full(n, np.nan)
    xc = np.full(n, np.nan); sep = np.full(n, np.nan)
    for k in range(n):
        pe = r[f"pos{ACT_E}"][k]; pc = r[f"pos{ACT_C}"][k]
        if len(pe) >= 1:
            xe[k] = pe[0][1]; ye[k] = pe[0][0]
        if len(pc) >= 1:
            xc[k] = np.mean([p[1] for p in pc])
        if len(pe) >= 1 and len(pc) >= 1:
            L = r["L"]
            sep[k] = min(np.hypot(G.min_image(p[0] - pe[0][0], L),
                                  G.min_image(p[1] - pe[0][1], L)) for p in pc)
    return dict(t=t[:n], xe=xe, ye=ye, xc_com=xc, sep=sep,
                nce=nce[:n], ncc=ncc[:n])


def append(rec):
    return G.append_result(rec, path=RESULTS)


def strip_png(r, g, path, fields=(ACT_E, ACT_C), title=""):
    """Save last-field snapshot strip if fields were saved."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return False
    F = r.get("fields")
    if F is None:
        return False
    fig, axs = plt.subplots(1, len(fields), figsize=(4 * len(fields), 4))
    if len(fields) == 1:
        axs = [axs]
    for ax, fi in zip(axs, fields):
        im = ax.imshow(F[fi], origin="lower", cmap="magma")
        ax.set_title(f"f{fi}")
        fig.colorbar(im, ax=ax, shrink=0.7)
    fig.suptitle(title)
    fig.savefig(path, dpi=80, bbox_inches="tight")
    plt.close(fig)
    return True


# ------------------------------------------------------------- rail/dock
def add_rail(M, k_rail=1.0):
    """Append a FROZEN channel (tau=1e12, D=0, never driven: W row zeros) to
    genome M; engine reads it via K[E,rail]=k_rail, cargo is blind (K=0).
    The channel keeps its IC exactly (drive 0, decay 1e-12/tu) = static
    potential S(x,y) in-genome. Vacuum exact wherever S=0."""
    M = copy.deepcopy(M)
    na = len(M["acts"])
    M["chans"].append(dict(tau=1e12, D=0.0, g="id", thr=0.0, sc=1.0))
    W = np.asarray(M["W"], float); K = np.asarray(M["K"], float)
    Wn = np.vstack([W, np.zeros((1, na))])
    Kn = np.hstack([K, np.zeros((na, 1))])
    Kn[ACT_E, -1] = k_rail
    M["W"] = Wn.tolist(); M["K"] = Kn.tolist()
    M["provenance"]["rail"] = dict(k_rail=k_rail)
    M["id"] += "_rail"
    return M


def rail_ic(F, g, dx, y0=48.0, amp=0.35, sig=5.0, x_dock=None, dock_w=2.0,
            dock_amp=None):
    """Write S(x,y) into the LAST channel: lane groove amp*(1-gauss(y-y0))
    plus optional dock wall dock_amp*sigmoid((x-x_dock)/dock_w)."""
    N = F.shape[1]; L = N * dx
    c = (np.arange(N) + 0.5) * dx
    dy = min_image_arr(c - y0, L)
    S = amp * (1.0 - np.exp(-dy[:, None] ** 2 / (2 * sig ** 2)))
    S = np.broadcast_to(S, (N, N)).copy()
    if x_dock is not None:
        da = amp if dock_amp is None else dock_amp
        S += da / (1.0 + np.exp(-(c[None, :] - x_dock) / dock_w))
    F[-1] = S
    return F


def min_image_arr(d, L):
    return (d + L / 2) % L - L / 2
