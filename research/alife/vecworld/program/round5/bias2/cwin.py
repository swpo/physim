"""cwin -- statistics of learned linear windows over 4 level-0 fields (numpy only; study `bias2`).

A window W (c, 4, w, w) is in standardised-field units; the raw-unit window is W / sd[field]. Per latent channel
and field: the L2 share of the window in standardised units (how much of the window's energy sits on that field),
the cosine of the field's window to the flat block window and to the tent (1 on the block, 1/2 on the 8-px halo),
the share of |weight| inside the block, and the net (summed) raw weight.
"""
import numpy as np

BS = 16


def block_window(h):
    w = np.zeros((BS + 2 * h, BS + 2 * h))
    w[h:h + BS, h:h + BS] = 1.0
    return w


def tent_window(h):
    """Tent restricted to an h-px halo frame: 1 on the block, 1/2 on the halo (h = 8: round 4's tent)."""
    p = np.concatenate([np.full(h, 0.5), np.ones(BS), np.full(h, 0.5)])
    return np.outer(p, p)


def _cos(a, b):
    return float(a.ravel() @ b.ravel() / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-300))


def window_stats(d, fields):
    W, sd, h = np.asarray(d["W"], float), np.asarray(d["sd"], float), int(d["h"])
    blk, tnt = block_window(h), tent_window(h)
    out = {"h": h, "c": int(W.shape[0]), "per_channel": []}
    for k in range(W.shape[0]):
        e = (W[k] ** 2).sum((1, 2))
        row = {"l2_share_std_units": dict(zip(fields, (e / max(e.sum(), 1e-300)).tolist())), "fields": {}}
        for f, name in enumerate(fields):
            v = W[k, f] / sd[f]
            av = np.abs(v)
            row["fields"][name] = {"cos_block": _cos(v, blk), "cos_tent": _cos(v, tnt),
                                   "share_abs_in_block": float(av[h:h + BS, h:h + BS].sum() / max(av.sum(), 1e-300)),
                                   "net_raw_weight": float(v.sum()),
                                   "profile_x": v.sum(0).tolist(), "profile_y": v.sum(1).tolist()}
        out["per_channel"].append(row)
    return out
