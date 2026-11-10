# cclaims -- the claims of the study `bias2`, read by cinterp.py (exec'd in its namespace: claim, cfg, hand, ana, ext,
# ceil, agree, pair). Every {placeholder} is filled from a result file; see cinterp.py for the source forms.
# Written on 10 Nov 2026 after r5-bias2-004 (membrane, gliders) and r5-bias2-005 (vortex) returned.
# Names: L0 / N0 = linear / nonlinear local encoder, block only; L8 / N8 = with an 8-px halo; U = dense encoder with
# 64 c x 64 c whitening; Uc = dense encoder with the local encoders' per-channel whitening. clos = closure with a
# global linear head, local = closure with one shared local rule ("local law"), recon = reconstruction.
G_, V_, M_ = "gliders", "vortex", "membrane"


def pr(w, nm):
    return hand(w, nm[5:], "nontriv", "participation_ratio") if nm.startswith("hand_") else cfg(w, nm, "nontriv", "participation_ratio")


def bms(w, nm):
    return hand(w, nm[5:], "nontriv", "box_mean_var_share", 0) if nm.startswith("hand_") else cfg(w, nm, "nontriv", "box_mean_var_share", 0)


def seed(w, nm):
    return cfg(w, nm, "seed_agreement", "loc1_mean")


def share(w, nm, f):
    return cfg(w, nm, "field_shares", 0, f)


def zfrom(w, nm, target, mode="loc1"):
    return cfg(w, nm, "agreement", target, mode, "Z_from_H")


def hfrom(w, nm, target, mode="loc1"):
    return cfg(w, nm, "agreement", target, mode, "H_from_Z")


def pz(w, a, b, h):
    return pair(w, a, b, h, "z")


# ------------------------------------------------------------------ the anchor: gliders (mass conserved)
claim("G1 (anchor, gliders; block-only encoders, per-block readout, both directions). Closure and the local law learn block mass: "
      "R2 {a_ll} (linear local law), {a_lc} (linear closure), {a_nl} (nonlinear local law), {a_nc} (nonlinear closure); seed agreement "
      "{s_ll}, {s_lc}, {s_nl}, {s_nc}. The window of the linear local law is flat (flat share of its smooth part {dc}). Nonlinear "
      "reconstruction is not mass: R2 {a_nr} with its best block design, seed agreement {s_nr}, ceiling at h = 4 {c_nr} against {c_m} "
      "for block mass. Round 4's row is reproduced with new seeds and the per-block readout.",
      {"a_ll": agree(G_, "L0_local_c1", "mass_h0"), "a_lc": agree(G_, "L0_clos_c1", "mass_h0"), "a_nl": agree(G_, "N0_local_c1", "mass_h0"),
       "a_nc": agree(G_, "N0_clos_c1", "mass_h0"), "s_ll": seed(G_, "L0_local_c1"), "s_lc": seed(G_, "L0_clos_c1"),
       "s_nl": seed(G_, "N0_local_c1"), "s_nc": seed(G_, "N0_clos_c1"), "dc": ext(G_, "windows", "L0_local_c1", "all_fields", "dc"),
       "a_nr": agree(G_, "N0_recon_c1", "c1_h0"), "s_nr": seed(G_, "N0_recon_c1"), "c_nr": ceil(G_, "N0_recon_c1", 4),
       "c_m": ceil(G_, "hand_mass_h0", 4)})
claim("G2 (gliders, tent). With an 8-px halo the linear local law's latent agrees with the tent-windowed mass at R2 {t_m} and with "
      "block mass at {b_m} (tent-windowed c0 {t_c0}); nonlinear {tn_m} and {bn_m}. Effective dimension falls from {pr0} to {pr8}.",
      {"t_m": agree(G_, "L8_local_c1", "mass_h8"), "b_m": agree(G_, "L8_local_c1", "mass_h0"), "t_c0": agree(G_, "L8_local_c1", "c0_h8"),
       "tn_m": agree(G_, "N8_local_c1", "mass_h8"), "bn_m": agree(G_, "N8_local_c1", "mass_h0"), "pr0": pr(G_, "L0_local_c1"),
       "pr8": pr(G_, "L8_local_c1")}, {"pr0": 1, "pr8": 1})
claim("G3 (gliders, learned against hand at no lower effective dimension). Against the most closed hand design that keeps at least "
      "as many effective dimensions and fits the same receptive field, the learned latents gain little: linear local law ({pr}) "
      "{a4} at h = 4 and {a16} at h = 16 (paired z {za4}, {za16}; the closed-form slow feature, {pr_sfa}); nonlinear local law "
      "{b16} at h = 16 (z {zb16}); with the halo ({prn8}) {c16} at h = 16 against the 8-px tent of c0 ({pr_c8}; z {zc16}). Against "
      "the next smoother hand window they lose: linear local law against the 4-px mass tent ({pr_h4}) {d4} at h = 4 (z {zd4}); "
      "nonlinear halo local law against the 16-px tent ({pr_h16}) {e16} (z {ze16}). The learned latents sit on the mass family's "
      "trade-off between ceiling and effective dimension.",
      {"pr": pr(G_, "L0_local_c1"), "pr_sfa": pr(G_, "hand_sfa_c1"), "a4": pair(G_, "L0_local_c1", "hand_sfa_c1", 4),
       "a16": pair(G_, "L0_local_c1", "hand_sfa_c1", 16), "za4": pz(G_, "L0_local_c1", "hand_sfa_c1", 4),
       "za16": pz(G_, "L0_local_c1", "hand_sfa_c1", 16), "b16": pair(G_, "N0_local_c1", "hand_sfa_c1", 16),
       "zb16": pz(G_, "N0_local_c1", "hand_sfa_c1", 16), "prn8": pr(G_, "N8_local_c1"), "pr_c8": pr(G_, "hand_c0_h8"),
       "c16": pair(G_, "N8_local_c1", "hand_c0_h8", 16), "zc16": pz(G_, "N8_local_c1", "hand_c0_h8", 16),
       "pr_h4": pr(G_, "hand_mass_h4"), "d4": pair(G_, "L0_local_c1", "hand_mass_h4", 4), "zd4": pz(G_, "L0_local_c1", "hand_mass_h4", 4),
       "pr_h16": pr(G_, "hand_mass_h16"), "e16": pair(G_, "N8_local_c1", "hand_mass_h16", 16), "ze16": pz(G_, "N8_local_c1", "hand_mass_h16", 16)},
      {k: 1 for k in ("pr", "pr_sfa", "za4", "za16", "zb16", "prn8", "pr_c8", "zc16", "pr_h4", "zd4", "pr_h16", "ze16")})
claim("G4 (gliders, controls with the same training settings). The dense encoder with full whitening trained for closure is less closed "
      "than block mass ({du4} at h = 4, z {zu4}) and is not a per-block variable (per-block R2 with mass {u_loc}, all-block ridge "
      "{u_glob}). With per-channel whitening it collapses onto one mode (first principal component {pc1} of the variance) with ceiling "
      "{cuc} at h = 16: with total mass constant there is no predictable global number. The box mean carries {bm} of the variance of the "
      "linear closure latent (1/64 = 0.016 for independent blocks).",
      {"du4": pair(G_, "U_clos_c1", "hand_mass_h0", 4), "zu4": pz(G_, "U_clos_c1", "hand_mass_h0", 4),
       "u_loc": agree(G_, "U_clos_c1", "mass_h0"), "u_glob": agree(G_, "U_clos_c1", "mass_h0", "glob"),
       "pc1": ext(G_, "global", "Uc_clos_c1", "pc1_share"), "cuc": ceil(G_, "Uc_clos_c1", 16), "bm": bms(G_, "L0_clos_c1")},
      {"zu4": 1, "u_loc": 4, "bm": 4})

# ------------------------------------------------------------------ the fed-vortex world (nothing conserved)
claim("V1 (vortex, hand block means). Closure ceilings at h = 16: vorticity {om}, label difference b - a {dab}, label-weighted vorticity "
      "{kb}, label b {b}, fuel {Y}, label a {a}, |vorticity| {absom}, a + b {lab}, enstrophy {ens}. Nothing is conserved: the box mean of "
      "block vorticity moves in time by {tv_om} of the independent-block value (0 for a conserved total), that of b - a by {tv_dab}.",
      {"om": ceil(V_, "hand_om_h0", 16), "dab": ceil(V_, "hand_dab_h0", 16), "kb": ceil(V_, "hand_kb_h0", 16), "b": ceil(V_, "hand_b_h0", 16),
       "Y": ceil(V_, "hand_Y_h0", 16), "a": ceil(V_, "hand_a_h0", 16), "absom": ceil(V_, "hand_absom_h0", 16),
       "lab": ceil(V_, "hand_lab_h0", 16), "ens": ceil(V_, "hand_ens_h0", 16),
       "tv_om": hand(V_, "om_h0", "nontriv", "box_mean_time_var_x64", 0), "tv_dab": hand(V_, "dab_h0", "nontriv", "box_mean_time_var_x64", 0)},
      {"tv_om": 2, "tv_dab": 1})
claim("V2 (vortex, what linear closure finds). The linear block-only closure latent is a per-block linear function of the four block means "
      "(R2 {zf}; local law {zf_l}) with weight on fuel and the labels and none on vorticity (shares of its variance: Y {sY}, a {sa}, "
      "b {sb}, vorticity {som}; R2 of block vorticity from the latent {om_in}). It equals the closed-form slow feature (linear SFA fitted "
      "on the other half): R2 both ways {sfa} (local law {sfa_l}); seed agreement {sd}. No single hand design matches it: best block "
      "design {kb} (label-weighted vorticity), its 8-px tent {kbt}.",
      {"zf": zfrom(V_, "L0_clos_c1", "fields"), "zf_l": zfrom(V_, "L0_local_c1", "fields"), "sY": share(V_, "L0_clos_c1", "Y"),
       "sa": share(V_, "L0_clos_c1", "a"), "sb": share(V_, "L0_clos_c1", "b"), "som": share(V_, "L0_clos_c1", "om"),
       "om_in": hfrom(V_, "L0_clos_c1", "om_h0"), "sfa": agree(V_, "L0_clos_c1", "sfa_c1"), "sfa_l": agree(V_, "L0_local_c1", "sfa_c1"),
       "sd": seed(V_, "L0_clos_c1"), "kb": agree(V_, "L0_clos_c1", "kb_h0"), "kbt": agree(V_, "L0_clos_c1", "kb_h8")})
claim("V3 (vortex, the latent is mostly a box-scale mode). Effective dimension of the linear closure latent {pr} of 64 (block vorticity "
      "{pr_om}, block fuel {pr_Y}); the box mean carries {bm} of its variance, and that box mean is a linear function of the box means "
      "of the four fields (R2 {r_f}; of label b alone {r_b}, of fuel alone {r_Y}). Its autocorrelation is {ac20} over 20 ticks and "
      "{ac80} over 80. The nonlinear encoders go further: box-mean share {bm_n0} (N0 closure, effective dimension {pr_n0}), {bm_n8l} "
      "(N8 local law, {pr_n8l}).",
      {"pr": pr(V_, "L0_clos_c1"), "pr_om": pr(V_, "hand_om_h0"), "pr_Y": pr(V_, "hand_Y_h0"), "bm": bms(V_, "L0_clos_c1"),
       "r_f": ext(V_, "global", "L0_clos_c1", "r2_g_from_box", "fields"), "r_b": ext(V_, "global", "L0_clos_c1", "r2_g_from_box", "b"),
       "r_Y": ext(V_, "global", "L0_clos_c1", "r2_g_from_box", "Y"), "ac20": ext(V_, "global", "L0_clos_c1", "g_autocorr", "20"),
       "ac80": ext(V_, "global", "L0_clos_c1", "g_autocorr", "80"), "bm_n0": bms(V_, "N0_clos_c1"), "pr_n0": pr(V_, "N0_clos_c1"),
       "bm_n8l": bms(V_, "N8_local_c1"), "pr_n8l": pr(V_, "N8_local_c1")},
      {"pr": 1, "pr_om": 1, "pr_Y": 1, "pr_n0": 1, "pr_n8l": 1, "r_f": 4})
claim("V4 (vortex, the control without locality). The dense encoder with per-channel whitening trained for closure puts {pc1} of its "
      "variance on one mode, a global number with closure ceiling {c16} at h = 16; that number is predicted from the box means of the "
      "four fields at R2 {r_f} (label b alone {r_b}). With full 64 x 64 whitening the dense encoder is less closed than block vorticity "
      "({du} at h = 16, z {zu}) and than the linear local encoder ({dl}, z {zl}), and is not a per-block variable (seed agreement {sd}).",
      {"pc1": ext(V_, "global", "Uc_clos_c1", "pc1_share"), "c16": ceil(V_, "Uc_clos_c1", 16),
       "r_f": ext(V_, "global", "Uc_clos_c1", "r2_g_from_box", "fields"), "r_b": ext(V_, "global", "Uc_clos_c1", "r2_g_from_box", "b"),
       "du": pair(V_, "U_clos_c1", "hand_om_h0", 16), "zu": pz(V_, "U_clos_c1", "hand_om_h0", 16),
       "dl": pair(V_, "U_clos_c1", "L0_clos_c1", 16), "zl": pz(V_, "U_clos_c1", "L0_clos_c1", 16), "sd": seed(V_, "U_clos_c1")},
      {"zu": 1, "zl": 1, "sd": 4})
claim("V5 (vortex, closure against the hand designs). Same receptive field, h = 16: the linear closure latent equals block vorticity "
      "({c} against {c_om}; paired {d_om}, z {z_om}) with {pr} effective dimensions against {pr_om}; the nonlinear one is above it "
      "({dn}, z {zn}) with {prn0}; with the 8-px halo nonlinear closure ({prn}) is {dh} (z {zh}) above the 8-px vorticity tent "
      "({pr_om8}). Any window: the 16-px vorticity tent ({pr_om16} effective dimensions, ceiling {c_om16}) equals the most closed "
      "local latent (N8 closure: {t16}, z {zt16}) and is above the others (N0 closure {tn0}, z {ztn0}; L0 closure {tl0}, z {ztl0}). "
      "Against the tent-smoothed label difference of about its own effective dimension ({pr16}) N8 closure is {n16} (z {zn16}) at "
      "h = 16 and {n2} at h = 2. Nothing learned beats tent-smoothed vorticity; closure buys its ceilings with effective dimension.",
      {"c": ceil(V_, "L0_clos_c1", 16), "c_om": ceil(V_, "hand_om_h0", 16), "d_om": pair(V_, "L0_clos_c1", "hand_om_h0", 16),
       "z_om": pz(V_, "L0_clos_c1", "hand_om_h0", 16), "pr": pr(V_, "L0_clos_c1"), "pr_om": pr(V_, "hand_om_h0"),
       "dn": pair(V_, "N0_clos_c1", "hand_om_h0", 16), "zn": pz(V_, "N0_clos_c1", "hand_om_h0", 16), "prn0": pr(V_, "N0_clos_c1"),
       "prn": pr(V_, "N8_clos_c1"), "dh": pair(V_, "N8_clos_c1", "hand_om_h8", 16), "zh": pz(V_, "N8_clos_c1", "hand_om_h8", 16),
       "pr_om8": pr(V_, "hand_om_h8"), "pr_om16": pr(V_, "hand_om_h16"), "c_om16": ceil(V_, "hand_om_h16", 16),
       "t16": pair(V_, "N8_clos_c1", "hand_om_h16", 16), "zt16": pz(V_, "N8_clos_c1", "hand_om_h16", 16),
       "tn0": pair(V_, "N0_clos_c1", "hand_om_h16", 16), "ztn0": pz(V_, "N0_clos_c1", "hand_om_h16", 16),
       "tl0": pair(V_, "L0_clos_c1", "hand_om_h16", 16), "ztl0": pz(V_, "L0_clos_c1", "hand_om_h16", 16), "pr16": pr(V_, "hand_dab_h16"),
       "n16": pair(V_, "N8_clos_c1", "hand_dab_h16", 16), "zn16": pz(V_, "N8_clos_c1", "hand_dab_h16", 16),
       "n2": pair(V_, "N8_clos_c1", "hand_dab_h16", 2)},
      {k: 1 for k in ("z_om", "pr", "pr_om", "zn", "prn0", "prn", "zh", "pr_om8", "pr_om16", "zt16", "ztn0", "ztl0", "pr16", "zn16")})
claim("V8 (vortex, what the objective rewards). The closure objectives reward the share of the latent's variance that is predicted, "
      "ceiling x (1 - oracle share), not the ceiling. That share at h = 4 and h = 16: nonlinear closure {n4}, {n16}; linear closure "
      "{l4}, {l16}; block vorticity {o4}, {o16}; block fuel {y4}, {y16}; block b - a {d4}, {d16}. The latents the encoders found "
      "are more predictable than every block mean; they are also far lower-dimensional.",
      {"n4": ana(V_, "configs", "N0_clos_c1", "raw_r2", 2), "n16": ana(V_, "configs", "N0_clos_c1", "raw_r2", 4),
       "l4": ana(V_, "configs", "L0_clos_c1", "raw_r2", 2), "l16": ana(V_, "configs", "L0_clos_c1", "raw_r2", 4),
       "o4": ana(V_, "hand", "om_h0", "raw_r2", 2), "o16": ana(V_, "hand", "om_h0", "raw_r2", 4),
       "y4": ana(V_, "hand", "Y_h0", "raw_r2", 2), "y16": ana(V_, "hand", "Y_h0", "raw_r2", 4),
       "d4": ana(V_, "hand", "dab_h0", "raw_r2", 2), "d16": ana(V_, "hand", "dab_h0", "raw_r2", 4)})
claim("V6 (vortex, reconstruction and predictable content). Linear reconstruction learns block fuel (R2 {a_r}; with the halo {a_r8}; "
      "seed agreement {s_r}) and is less closed than the hand block fuel ({d4} at h = 4, z {z4}); nonlinear reconstruction matches no "
      "design (best {a_n}, seed agreement {s_n}; ceiling at h = 4 {c_n}). Closure keeps less predictable content at h = 1 than the hand "
      "designs: I_capt {i_c} nats for the linear closure latent against {i_Y} for block fuel and {i_om} for block vorticity.",
      {"a_r": agree(V_, "L0_recon_c1", "Y_h0"), "a_r8": agree(V_, "L8_recon_c1", "Y_h0"), "s_r": seed(V_, "L0_recon_c1"),
       "d4": pair(V_, "L0_recon_c1", "hand_Y_h0", 4), "z4": pz(V_, "L0_recon_c1", "hand_Y_h0", 4), "a_n": agree(V_, "N0_recon_c1", "om_h0"),
       "s_n": seed(V_, "N0_recon_c1"), "c_n": ceil(V_, "N0_recon_c1", 4), "i_c": cfg(V_, "L0_clos_c1", "I_capt", 0),
       "i_Y": hand(V_, "Y_h0", "logdet", "I_capt", 0), "i_om": hand(V_, "om_h0", "logdet", "I_capt", 0)},
      {"z4": 1, "i_c": 0, "i_Y": 0, "i_om": 0})
claim("V7 (vortex, two numbers per block). With c = 2 the linear closure latent also holds block vorticity (R2 of block vorticity from "
      "the latent {om2} against {om1} at c = 1) and still the fuel and label mode (R2 of b - a {dab2}); seed agreement {sd}; ceiling at "
      "h = 16 {c2} ({c1} at c = 1).",
      {"om2": hfrom(V_, "L0_clos_c2", "om_h0"), "om1": hfrom(V_, "L0_clos_c1", "om_h0"), "dab2": hfrom(V_, "L0_clos_c2", "dab_h0"),
       "sd": seed(V_, "L0_clos_c2"), "c2": ceil(V_, "L0_clos_c2", 16), "c1": ceil(V_, "L0_clos_c1", 16)})

# ------------------------------------------------------------------ the phase-membrane world (nothing conserved)
claim("M1 (membrane, hand block means). Closure ceilings at h = 16 (640 time units): catalyst K {K}, phi K {phiK}, phase phi {phi}, cell "
      "area {area}, substrate S {S}, links L {L}, wall {wall}; at h = 4 all but the wall are {K4}-{S4}. Block K is anticorrelated with "
      "itself over 16 ticks (persistence ceiling {pK}), as expected for a growth and division cycle of about 46 ticks.",
      {"K": ceil(M_, "hand_K_h0", 16), "phiK": ceil(M_, "hand_phiK_h0", 16), "phi": ceil(M_, "hand_phi_h0", 16), "area": ceil(M_, "hand_area_h0", 16),
       "S": ceil(M_, "hand_S_h0", 16), "L": ceil(M_, "hand_L_h0", 16), "wall": ceil(M_, "hand_wall_h0", 16), "K4": ceil(M_, "hand_area_h0", 4),
       "S4": ceil(M_, "hand_S_h0", 4), "pK": hand(M_, "K_h0", "persistence_ceiling", 4)})
claim("M2 (membrane, what linear closure finds). The linear block-only closure latent is not a block mean: R2 from the four block means "
      "{zf} (from the 3 x 3 neighbourhood of them {zf9}). Its window is a gradient filter: of the smooth part of the window the flat "
      "share is {dc} and the linear-gradient share {dip} (phi {d_phi}, K {d_K}, L {d_L}, S {d_S}); in each of the 4 replicas the K "
      "gradient is opposite to the phi gradient (cosines {cK}) and the L gradient parallel ({cL}): a spatial gradient of phi - K + L "
      "(variance shares phi {s_phi}, K {s_K}, L {s_L}, S {s_S}). The direction differs between replicas (window cosine {wc}; seed "
      "agreement {sd}) while the ceilings do not (seed difference at h = 16 {sdiff}). Its box mean carries {bm} of its variance.",
      {"zf": zfrom(M_, "L0_clos_c1", "fields"), "zf9": zfrom(M_, "L0_clos_c1", "fields", "loc9"),
       "dc": ext(M_, "windows", "L0_clos_c1", "all_fields", "dc"), "dip": ext(M_, "windows", "L0_clos_c1", "all_fields", "dipole"),
       "d_phi": ext(M_, "windows", "L0_clos_c1", "fields", "phi", "dipole"), "d_K": ext(M_, "windows", "L0_clos_c1", "fields", "K", "dipole"),
       "d_L": ext(M_, "windows", "L0_clos_c1", "fields", "L", "dipole"), "d_S": ext(M_, "windows", "L0_clos_c1", "fields", "S", "dipole"),
       "cK": ext(M_, "windows", "L0_clos_c1", "dipole_cos_with_first_field", "K"),
       "cL": ext(M_, "windows", "L0_clos_c1", "dipole_cos_with_first_field", "L"), "s_phi": share(M_, "L0_clos_c1", "phi"),
       "s_K": share(M_, "L0_clos_c1", "K"), "s_L": share(M_, "L0_clos_c1", "L"), "s_S": share(M_, "L0_clos_c1", "S"),
       "wc": ext(M_, "windows", "L0_clos_c1", "replica_cos_smooth"), "sd": seed(M_, "L0_clos_c1"),
       "sdiff": cfg(M_, "L0_clos_c1", "ceiling_G_seed_diff", 4), "bm": bms(M_, "L0_clos_c1")}, {"bm": 4})
claim("M3 (membrane, learned closure is more closed than every hand design at long horizons). Paired ceiling differences to block K at "
      "h = 8 and 16: linear closure {l8} (z {zl8}) and {l16} (z {zl16}); nonlinear closure {n8} (z {zn8}) and {n16} (z {zn16}). Against "
      "hand windows of lower effective dimension, which favours the hand side: linear closure ({pr_l}) against the 8-px tent of K "
      "({pr_k8}) {lt16} (z {zlt16}); nonlinear halo closure ({pr_n8}) against the 16-px tent ({pr_k16}) {nt16} (z {znt16}); nonlinear "
      "halo local law against the 8-px tent {nl16} (z {znl16}). At h = 1 and 2 the closure latents are below block K by at most {lo}. "
      "Ceilings at h = 16: {c_l}, {c_n}, {c_n8}, {c_n8l} against {c_K}; the most closed hand design of any window "
      "or width at h = 16 is {best} with {c_best}.",
      {"l8": pair(M_, "L0_clos_c1", "hand_K_h0", 8), "zl8": pz(M_, "L0_clos_c1", "hand_K_h0", 8), "l16": pair(M_, "L0_clos_c1", "hand_K_h0", 16),
       "zl16": pz(M_, "L0_clos_c1", "hand_K_h0", 16), "n8": pair(M_, "N0_clos_c1", "hand_K_h0", 8), "zn8": pz(M_, "N0_clos_c1", "hand_K_h0", 8),
       "n16": pair(M_, "N0_clos_c1", "hand_K_h0", 16), "zn16": pz(M_, "N0_clos_c1", "hand_K_h0", 16), "pr_l": pr(M_, "L0_clos_c1"),
       "pr_k8": pr(M_, "hand_K_h8"), "lt16": pair(M_, "L0_clos_c1", "hand_K_h8", 16), "zlt16": pz(M_, "L0_clos_c1", "hand_K_h8", 16),
       "pr_n8": pr(M_, "N8_clos_c1"), "pr_k16": pr(M_, "hand_K_h16"), "nt16": pair(M_, "N8_clos_c1", "hand_K_h16", 16),
       "znt16": pz(M_, "N8_clos_c1", "hand_K_h16", 16), "nl16": pair(M_, "N8_local_c1", "hand_K_h8", 16),
       "znl16": pz(M_, "N8_local_c1", "hand_K_h8", 16), "lo": pair(M_, "N0_clos_c1", "hand_K_h0", 2), "c_l": ceil(M_, "L0_clos_c1", 16),
       "c_n": ceil(M_, "N0_clos_c1", 16), "c_n8": ceil(M_, "N8_clos_c1", 16), "c_n8l": ceil(M_, "N8_local_c1", 16), "c_K": ceil(M_, "hand_K_h0", 16),
       "best": ana(M_, "hand_most_closed", "any_width", "h16", "design"), "c_best": ana(M_, "hand_most_closed", "any_width", "h16", "ceiling")},
      {k: 1 for k in ("zl8", "zl16", "zn8", "zn16", "pr_l", "pr_k8", "zlt16", "pr_n8", "pr_k16", "znt16", "znl16")})
claim("M4 (membrane, the other objectives). The linear local law learns block means of the cell material: R2 from the four block means "
      "{zf}, best single design block K {aK} (seed agreement {sd}); its window is flat on phi and L (flat shares {dphi}, {dL}); it is "
      "more closed than block K at h = 4 and 8 ({d4}, {d8}; z {z4}, {z8}) and equal at h = 16 ({d16}, z {z16}). Linear reconstruction "
      "is block K (R2 {aR}, seed agreement {sR}). Nonlinear reconstruction is close to block phi (R2 {aN}) and less closed than block K "
      "({dN4} at h = 4, z {zN4}).",
      {"zf": zfrom(M_, "L0_local_c1", "fields"), "aK": agree(M_, "L0_local_c1", "K_h0"), "sd": seed(M_, "L0_local_c1"),
       "dphi": ext(M_, "windows", "L0_local_c1", "fields", "phi", "dc"), "dL": ext(M_, "windows", "L0_local_c1", "fields", "L", "dc"),
       "d4": pair(M_, "L0_local_c1", "hand_K_h0", 4), "d8": pair(M_, "L0_local_c1", "hand_K_h0", 8), "z4": pz(M_, "L0_local_c1", "hand_K_h0", 4),
       "z8": pz(M_, "L0_local_c1", "hand_K_h0", 8), "d16": pair(M_, "L0_local_c1", "hand_K_h0", 16), "z16": pz(M_, "L0_local_c1", "hand_K_h0", 16),
       "aR": agree(M_, "L0_recon_c1", "K_h0"), "sR": seed(M_, "L0_recon_c1"), "aN": agree(M_, "N0_recon_c1", "phi_h0"),
       "dN4": pair(M_, "N0_recon_c1", "hand_K_h0", 4), "zN4": pz(M_, "N0_recon_c1", "hand_K_h0", 4)},
      {"z4": 1, "z8": 1, "z16": 1, "zN4": 1})
claim("M5 (membrane, seed stability). Closure with a global head is not reproducible as a variable: seed agreement {s_l0} (L0), {s_l8} "
      "(L8), {s_n0} (N0), {s_n8} (N8), against {s_ll} for the linear local law and {s_nl} for the nonlinear one at block only "
      "({s_n8l} and {s_l8l} with the halo). The two seeds reach the same ceilings (differences at h = 16: {d_l0}, {d_l8}, {d_n0}, {d_n8}).",
      {"s_l0": seed(M_, "L0_clos_c1"), "s_l8": seed(M_, "L8_clos_c1"), "s_n0": seed(M_, "N0_clos_c1"), "s_n8": seed(M_, "N8_clos_c1"),
       "s_ll": seed(M_, "L0_local_c1"), "s_nl": seed(M_, "N0_local_c1"), "s_n8l": seed(M_, "N8_local_c1"), "s_l8l": seed(M_, "L8_local_c1"),
       "d_l0": cfg(M_, "L0_clos_c1", "ceiling_G_seed_diff", 4), "d_l8": cfg(M_, "L8_clos_c1", "ceiling_G_seed_diff", 4),
       "d_n0": cfg(M_, "N0_clos_c1", "ceiling_G_seed_diff", 4), "d_n8": cfg(M_, "N8_clos_c1", "ceiling_G_seed_diff", 4)})
claim("M6 (membrane, controls and width). The dense encoder with per-channel whitening collapses onto one mode ({pc1} of the variance) "
      "that is neither slow (autocorrelation over 20 ticks {ac}) nor a function of the box means (R2 {r}); ceiling at h = 16 {cuc}. "
      "With full whitening the dense closure encoder is above block K at h = 16 ({du}, z {zu}) and below the linear local encoder "
      "({dl}, z {zl}). With two numbers per block the nonlinear halo closure reaches {c2} at h = 16, {d2} above the four block field "
      "means (z {z2}).",
      {"pc1": ext(M_, "global", "Uc_clos_c1", "pc1_share"), "ac": ext(M_, "global", "Uc_clos_c1", "g_autocorr", "20"),
       "r": ext(M_, "global", "Uc_clos_c1", "r2_g_from_box", "fields"), "cuc": ceil(M_, "Uc_clos_c1", 16),
       "du": pair(M_, "U_clos_c1", "hand_K_h0", 16), "zu": pz(M_, "U_clos_c1", "hand_K_h0", 16), "dl": pair(M_, "U_clos_c1", "L0_clos_c1", 16),
       "zl": pz(M_, "U_clos_c1", "L0_clos_c1", 16), "c2": ceil(M_, "N8_clos_c2", 16), "d2": pair(M_, "N8_clos_c2", "hand_fields", 16),
       "z2": pz(M_, "N8_clos_c2", "hand_fields", 16)}, {"zu": 1, "zl": 1, "z2": 1})
claim("M7 (membrane, predictable content). Closure with a global head gives up content at h = 1: I_capt {i_l} nats (linear) and {i_n} "
      "(nonlinear) against {i_phi} for block phi and {i_K} for block K; the local law keeps it ({i_ll} linear, {i_nl} nonlinear).",
      {"i_l": cfg(M_, "L0_clos_c1", "I_capt", 0), "i_n": cfg(M_, "N0_clos_c1", "I_capt", 0), "i_phi": hand(M_, "phi_h0", "logdet", "I_capt", 0),
       "i_K": hand(M_, "K_h0", "logdet", "I_capt", 0), "i_ll": cfg(M_, "L0_local_c1", "I_capt", 0), "i_nl": cfg(M_, "N0_local_c1", "I_capt", 0)},
      {k: 0 for k in ("i_l", "i_n", "i_phi", "i_K", "i_ll", "i_nl")})

# ------------------------------------------------------------------ across the three theories
claim("X1 (the map, linear block-only closure with a global head, one number per block). Gliders: block mass (R2 {g_a}, flat window share "
      "{g_dc}, box-mean share {g_bm}, seed agreement {g_s}). Vortex: the block reading of a slow box-scale fuel and label mode (R2 from "
      "block means {v_a}, with the closed-form slow feature {v_sfa}; box-mean share {v_bm}; seed agreement {v_s}; vorticity share "
      "{v_om}). Membrane: a within-block gradient of phi - K + L (flat window share {m_dc}, gradient share {m_dip}; box-mean share "
      "{m_bm}; seed agreement {m_s}). 'Closure finds mass' holds only in the mass-conserving theory.",
      {"g_a": agree(G_, "L0_clos_c1", "mass_h0"), "g_dc": ext(G_, "windows", "L0_clos_c1", "all_fields", "dc"), "g_bm": bms(G_, "L0_clos_c1"),
       "g_s": seed(G_, "L0_clos_c1"), "v_a": zfrom(V_, "L0_clos_c1", "fields"), "v_sfa": agree(V_, "L0_clos_c1", "sfa_c1"),
       "v_bm": bms(V_, "L0_clos_c1"), "v_s": seed(V_, "L0_clos_c1"), "v_om": share(V_, "L0_clos_c1", "om"),
       "m_dc": ext(M_, "windows", "L0_clos_c1", "all_fields", "dc"), "m_dip": ext(M_, "windows", "L0_clos_c1", "all_fields", "dipole"),
       "m_bm": bms(M_, "L0_clos_c1"), "m_s": seed(M_, "L0_clos_c1")}, {"g_bm": 4, "m_bm": 4})
claim("X2 (learned against the most closed hand design of at least the same effective dimension and the same receptive field, "
      "closure ceiling at h = 16). Gliders: {g} (z {zg}; nonlinear halo local law against the 8-px c0 tent) and {g0} (z {zg0}; linear "
      "local law against the closed-form slow feature). Vortex: {v} (z {zv}; nonlinear closure against block vorticity, with a tenth "
      "of its effective dimension), and {v16} (z {zv16}) against the 16-px vorticity tent. Membrane: {m} (z {zm}; nonlinear closure "
      "against the closed-form extended slow feature, the most closed hand design there), {m8} (z {zm8}) with the halo, {ml} (z {zml}) "
      "linear. Round 4's 'nothing learned beats the hand designs' carries over to the vortex world (tent-smoothed vorticity) but not "
      "to the membrane world, where no hand design, closed-form slow features included, is as closed at long horizons.",
      {"g": pair(G_, "N8_local_c1", "hand_c0_h8", 16), "zg": pz(G_, "N8_local_c1", "hand_c0_h8", 16),
       "g0": pair(G_, "L0_local_c1", "hand_sfa_c1", 16), "zg0": pz(G_, "L0_local_c1", "hand_sfa_c1", 16),
       "v": pair(V_, "N0_clos_c1", "hand_om_h0", 16), "zv": pz(V_, "N0_clos_c1", "hand_om_h0", 16),
       "v16": pair(V_, "N0_clos_c1", "hand_om_h16", 16), "zv16": pz(V_, "N0_clos_c1", "hand_om_h16", 16),
       "m": pair(M_, "N0_clos_c1", "hand_sfax_c1", 16), "zm": pz(M_, "N0_clos_c1", "hand_sfax_c1", 16),
       "m8": pair(M_, "N8_clos_c1", "hand_sfax_c1", 16), "zm8": pz(M_, "N8_clos_c1", "hand_sfax_c1", 16),
       "ml": pair(M_, "L0_clos_c1", "hand_sfax_c1", 16), "zml": pz(M_, "L0_clos_c1", "hand_sfax_c1", 16)},
      {k: 1 for k in ("zg", "zg0", "zv", "zv16", "zm", "zm8", "zml")})