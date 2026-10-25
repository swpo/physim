# 1.5x resolution continuation of the lcn-cog claim (c18)

`world.py` = the claim's world plus P["R"] (kernel radius; grid 192*R/10; food and waste diffusivities scaled by
(R/10)^2 so bodies keep their size in units of R) and screening keys (P["mod"], P["N"]) that are off by default.
All runs here use `WORLD_P='{"R":15}'` (288^2, R=15, dt 0.1).

- Pack: `WORLD_P='{"R":15}' python -m labkit.run world.py --out pack_r15 --seeds 0 1 --frames 200 --spf 50 --no-movie`.
  Cogs form from full-domain noise (up to 37 components during the transient). Fewer persist than at R=10: final 3 and 6
  (R=10: 14 and 11); several die one by one by t~700 although food stays plentiful (sheet.png, seed 0, white waste blobs).
- Shell profile (`radial_cog.py`): A1 trough at r=4-5 (R=10: r=3), shell band peak at r=12 (R=10: r=7-8), i.e. 1.5x;
  shell 0.96, trough 0.001, outside (r=25-29) 0.013 / 0.006; per-cell shell/trough >= 7.2 in all 129 / 134 cell-frames.
- Fork, seed 2: `runsave.py` pre to t=600 (4 cogs), `RAD=27 PRE=r15pre OUT=r15cut_ mkcut.py 2`, fed twin and food cut
  (disk r=27) for 300 t; `PFX=r15 cutplot.py localcut_r15.png 2`: the cut cog is below 10% at t=635 and 0 at t=900;
  fed twin 1.00; all other bodies 1.00 / 1.00.

So the shell and the food dependence survive the resolution change; cog persistence does not fully (spontaneous deaths
with food present at R=15), which is a limit on the claim's I at this resolution, not on B or E.
