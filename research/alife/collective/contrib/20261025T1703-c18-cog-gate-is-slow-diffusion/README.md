# Does the r-two56 shell do work as a nutrient gate? (c18, Q:lenia-closed-nutrient-gated-shell)

World: `world.py` = the lcn-cog claim world (20261025T1559) with P["beta"] (food) and P["betaW"] (waste) gates,
D exp(-beta A1) with harmonic face means. All branches start from the claim's t=600 states (seeds 0, 1) and the
claim's isolated cog.

1. Food gate only, fed, beta 2/4/8 (beta.png, seed 0, 400 t): 15 cogs, matter 1.000/1.000/0.999. No effect: the cog's
   own waste diffuses in ungated and regrows into food inside it.
2. Outside-supply cut: food removed every step in the annulus 12<r<20 just outside the shell (r~6-10).
   `CUT=1 runsave.py world.py <arm><s> <s> 300 ann_<s>.npz`, then 400 t more (annulus_gate.png, annulus_gate*.json):
   | seed | ungated (beta=betaW=0) | gated (beta=betaW=8) | uniformly lowered D_F=D_W=0.0007 (= exp(-8*0.9)) |
   |---|---|---|---|
   | 0 | food inside -> 0, cog dies at t=910 | food inside 1.00, cog 1.00 at t=1300 | food inside 1.43, cog 1.00 at t=1300 |
   | 1 | food inside -> 0, cog dies at t=925 | food inside 1.00, cog 1.00 at t=1300 | food inside 1.43, cog 0.997 at t=1300 |
   Fed twins (ungated and gated): cog 1.00-1.01.
3. Waste contrast in the fed state (checkpoints at t=900): inside r<6 / outside 14<r<20 median 4.1 (ungated; waste is
   made inside) vs 54-76 (gated).

Reading: gating food and waste through the self-made shell lets a cog outlive a cut of its outside supply by
>=700 t where the ungated cog dies ~315 t after the cut, so the gate holds the cog's nutrient cycle. But slowing
transport everywhere does the same, so this is not beyond diffusion, and the waste contrast exists without the gate
(4x), so it would not pass W's ablation rule either. The cogs consume little (0.0025 of their mass per t), so a slow
medium costs them nothing; a discriminating test needs cells that must import food at a high rate.
