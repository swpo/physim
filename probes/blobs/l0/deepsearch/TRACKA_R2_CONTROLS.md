INTERFACE REVISION R2 (user, 2026-09-01): the control surface leaks geometry.
probe_move(a1,a2) + probe_dilate(gain) DISCLOSE that the pose space factorizes
into 2 translation channels + 1 scale channel => the 2D-ness and the existence
of a zoom are given away in the API shape.
REPLACE with ONE opaque actuator:
  probe_adjust(device, u1, u2, u3, steps=1, read=True)
  - u in [-1,1]^3; effect = secret per-WORLD fixed linear map M (invertible,
    random rotation+scale mix over (dx, dy, dlog_spacing)); the CHANNELS MIX
    translation and dilation so even the motion/zoom split must be discovered
    by experiment (the lattice structure of the device makes this learnable:
    dilation changes inter-slot correlation scale, translation shifts phase).
  - cost: sum|u_i| per step from a SINGLE 'adjust' budget (no cost-structure
    leak between translation and dilation).
  - status: report n_actuator_channels=3 (count only), drop 'motion'/'dilate'
    budget names, drop the basis-disclosure note ('meaning undisclosed' stays).
Injection stays as-is (emitter disclosure retained round-1: flagged for a
future round decision). probe_status text audit: remove any wording implying
translation/scaling/spacing semantics.