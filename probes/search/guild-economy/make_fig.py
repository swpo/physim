import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

wd = "/Users/spoho/Documents/prime/test/physim/probes/search/guild-economy"
rho_pts = [1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
fr_pts  = [0.323, 0.408, 0.455, 0.473, 0.493, 0.507, 0.524]
tau_pts = [4050, 3578, 2890, 2217, 2034, 2246, 2036]
tau_seed_lo, tau_seed_hi = 2445, 3139

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(rho_pts, fr_pts, 'o-', color='C0')
ax1.errorbar([2.1], [0.455], yerr=[[0.005],[0.007]], fmt='s', color='C3', capsize=4, label='8-seed spread @rho=2.1')
ax1.set_xlabel('price ratio rho = cW/cR (micro price)')
ax1.set_ylabel('fr* (recycler site share at equilibrium)')
ax1.set_title('G3: demand curve - market equilibrium vs waste price')
ax1.legend(fontsize=8); ax1.grid(alpha=0.3)
ax2.plot(rho_pts, tau_pts, 'o-', color='C1')
ax2.errorbar([2.1], [2890], yerr=[[2890-tau_seed_lo],[tau_seed_hi-2890]], fmt='s', color='C3', capsize=4, label='8-seed spread @rho=2.1')
ax2.set_xlabel('price ratio rho = cW/cR')
ax2.set_ylabel('tau3 (market relaxation time, ticks)')
ax2.set_title('G3: relaxation time vs price (monotone to rho=2.3, then flat)')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(wd + '/strips/GE1_response_curve.png', dpi=120)
print('saved')
