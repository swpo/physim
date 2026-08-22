# BLOB-LOOP (V2c recirculation) — controller fan-in (child died post-runs; analysis by controller)

## Verdict: single-zone recirculation = CLEAN GEOMETRIC NO-GO (honest negative, certified 2 seeds)
Layout: P12-heritage lane (L=96 torus, y=48 rail, eta-xbox zone x in [8,72],
carrier pair + plug + 1 cargo... actually 2 towable blobs: plug slot + cargo).
Runs: G1_recirc_s1/s2 (T=6000, noise 2e-3).

## What happened (identical both seeds — deterministic physics, 1.5% timing spread)
- Each towable blob got exactly ONE tow phase (slot0: +78px @ t~200-1600;
  slot1: +135px @ t~350-2600), was released past the eta edge (x=72), and PARKED
  at x=80 / x=95 (mod 96) — OUTSIDE the coupling zone.
- The carriers kept lapping (4.5 laps in the record) and passed through/near the
  parked cargo repeatedly with ZERO re-grip and ZERO disturbance (<1px) — the
  machinev3-style flyby immunity, working exactly as designed: no eta, no grip.
- No second cycle occurred in 6000tu and none ever would: released cargo is
  geometrically unreachable by the single zone that released it.

## The law
Re-circulation requires a RETURN LEG: released cargo parks in the eta-null
region and nothing transports it back into the grip zone. Closing the loop needs
one of: (a) a second eta zone + opposite-direction carrier on a return lane,
(b) a b-field slope in the null region sliding parked cargo back to the zone
entry (genesis toolkit), or (c) zone geometry that wraps the release point into
the next entry (release edge = entry edge on the torus — but then release never
happens; the edge cannot be both).
This is the dock-to-dock composition question posed by V2c, answered: docks
compose in SERIES only with an interposed transport primitive.

## Files
results.json (4 rows: smoke, anchor, G1 s1/s2), data/G1_recirc_s{1,2}.npz,
this SUMMARY (controller). Child sessions: 4 lives, each advancing one stage
(read -> smoke+anchor -> design -> runs); cycle analysis completed by controller.
