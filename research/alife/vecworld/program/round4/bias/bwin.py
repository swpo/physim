"""bwin -- designed windows and statistics of learned linear windows (numpy only; study `bias`)."""
import numpy as np

BS = 16


def win(h):
    return BS + 2 * int(h)


def tent_window():
    """The level-1 analogue of learned_phi2's tent: 1 on the 16-px block, 1/2 on an 8-px halo (outer product of
    the 1D profile [1/2 x 8, 1 x 16, 1/2 x 8]), applied to total mass c0 + c1 in raw units. (32, 32)."""
    p = np.concatenate([np.full(8, 0.5), np.ones(16), np.full(8, 0.5)])
    return np.outer(p, p)


def block_window(h):
    """The block-mass window (1 on the block, 0 on the halo) inside a (16 + 2h)^2 window."""
    w = np.zeros((win(h), win(h)))
    w[h:h + BS, h:h + BS] = 1.0
    return w


def embed(wsmall, w):
    """Centre a square window in a w x w frame (cropping if it is larger)."""
    n = wsmall.shape[0]
    out = np.zeros((w, w))
    if n <= w:
        o = (w - n) // 2
        out[o:o + n, o:o + n] = wsmall
    else:
        o = (n - w) // 2
        out[:] = wsmall[o:o + w, o:o + w]
    return out


def _cos(a, b):
    return float(abs(a.ravel() @ b.ravel()) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-300))


def span_alignment(W, P):
    Qw, _ = np.linalg.qr(W)
    Qp, _ = np.linalg.qr(P)
    return float(np.sum((Qp.T @ Qw) ** 2) / W.shape[1])


def window_stats(d):
    """d: npz with W (c, 2, w, w) in standardised-channel units, sd (2,), h. Raw-unit window Wr = W / sd."""
    W, sd, h = np.asarray(d["W"], float), np.asarray(d["sd"], float), int(d["h"])
    Wr = W / sd[None, :, None, None]
    w = Wr.shape[-1]
    blk = block_window(h)
    tnt = embed(tent_window(), w)
    both = lambda m: np.stack([m, m])
    out = {"h": h, "c": int(W.shape[0]), "per_channel": []}
    for k in range(W.shape[0]):
        v = Wr[k]
        av = np.abs(v)
        out["per_channel"].append({
            "cos_block_mass": _cos(v, both(blk)), "cos_tent": _cos(v, both(tnt)),
            "cos_block_c0": _cos(v, np.stack([blk, 0 * blk])), "cos_block_c1": _cos(v, np.stack([0 * blk, blk])),
            "share_abs_in_block": float(av[:, h:h + BS, h:h + BS].sum() / av.sum()),
            "channel_balance_c0": float(v[0].sum() / (v[0].sum() + v[1].sum())) if abs(v.sum()) > 1e-12 else None,
            "profile_x": v.sum((0, 1)).tolist(), "profile_y": v.sum((0, 2)).tolist()})
    Wf = Wr.reshape(W.shape[0], -1).T
    out["span_alignment_block_mass"] = span_alignment(Wf, both(blk).reshape(-1, 1))
    out["span_alignment_block_channels"] = span_alignment(Wf, np.stack([np.stack([blk, 0 * blk]), np.stack([0 * blk, blk])]).reshape(2, -1).T)
    out["span_alignment_tent"] = span_alignment(Wf, both(tnt).reshape(-1, 1))
    return out
