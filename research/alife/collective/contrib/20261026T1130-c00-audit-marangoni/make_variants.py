import sys
src, out = sys.argv[1], sys.argv[2]
w = open(src).read()
def rep(t, a, b, n=1):
    assert t.count(a) == n, (a, t.count(a)); return t.replace(a, b)
# (2) wall-off by shadow: s2 = same rod-only source, decay, diffusion and advection as s, no adsorption drift; cargo sees s2.
v = rep(w, '"name": "active-nematic-marangoni"', '"name": "active-nematic-marangoni-walloff"')
v = rep(v, '"channels": ["phi (droplet)", "order |Q|", "surfactant s", "cargo c"]',
        '"channels": ["phi (droplet)", "order |Q|", "surfactant s", "cargo c", "shadow s2 (no adsorption; couples cargo)"]')
v = rep(v, '"radial_channels": [0, 1, 2, 3]', '"radial_channels": [0, 1, 2, 3, 4]')
v = rep(v, '"s": np.zeros((H, W)), "c": np.zeros((H, W))}', '"s": np.zeros((H, W)), "c": np.zeros((H, W)), "s2": np.zeros((H, W))}')
v = rep(v, '''    if P["CARGO"]:
        s["c"] = _cargo(s["c"], sf, vx, vy, phi, dt, P["dx"])''',
'''    # AUDIT wall-off: shadow s2, identical source (rod pixels), decay, diffusion (implicit) and advection as s,
    # but without the adsorption drift Ds chis s grad w. The cargo is coupled to s2; s (with its drift) still drives Marangoni.
    s2 = s["s2"]; S2h = fft2(s2)
    src2 = (P["ks"] * (phi > 0) if P["src_mode"] == "rod" else P["ks"] * 0.5 * (1 + np.clip(phi, -1, 1))) - P["kds"] * s2
    S2h = (S2h + dt * (-(1j * kx * fft2(vx * s2) + 1j * ky * fft2(vy * s2)) + fft2(src2)) * da) / (1 + dt * P["Ds"] * k2)
    if P["CARGO"]:
        s["c"] = _cargo(s["c"], s2, vx, vy, phi, dt, P["dx"])
    s["s2"] = np.maximum(ifft2(S2h).real, 0)''')
v = rep(v, 'return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2), s["s"], s["c"]]).astype(np.float32)',
        'return np.stack([s["phi"], np.sqrt(s["q1"] ** 2 + s["q2"] ** 2), s["s"], s["c"], s["s2"]]).astype(np.float32)')
open(out + "/active-nematic-marangoni-walloff.py", "w").write(v)
# (3) chis = 0 (no adsorption of s itself; bodies change because s drives Marangoni)
v = rep(w, '"name": "active-nematic-marangoni"', '"name": "active-nematic-marangoni-chis0"')
v = rep(v, 'P["chis"] = 5.0', 'P["chis"] = 0.0  # AUDIT: chis 5 -> 0')
open(out + "/active-nematic-marangoni-chis0.py", "w").write(v)
# (4) coupling off: kappa = 0
v = rep(w, '"name": "active-nematic-marangoni"', '"name": "active-nematic-marangoni-kappa0"')
v = rep(v, 'CARGO=1, Dc=1.0, kc=0.02, kcd=0.005, kappa=20.0, mar=40.0)', 'CARGO=1, Dc=1.0, kc=0.02, kcd=0.005, kappa=0.0, mar=40.0)  # AUDIT: kappa 20 -> 0')
open(out + "/active-nematic-marangoni-kappa0.py", "w").write(v)
