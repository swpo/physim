# Lens: how science reaches deeper levels from the top, and what limits it

## 1. Key works

**Fluctuations.**
- **Einstein [1]:** a visible particle's mean-square displacement determines Avogadro's number N, through D = RT/(6πηaN).
- **Perrin [2]:** five independent methods gave N between 60 and 68 ×10^22. What settled the reality of molecules was that the methods agreed, not any single value.
- **Kubo [3]:** a system's linear response is fixed by its equilibrium fluctuations. A generalized Nyquist relation ties frequency-dependent friction to coloured noise.
- **Mori [4]:** projecting the dynamics onto chosen variables gives a memory kernel equal to the correlation of the random force. To the observer, an eliminated level shows up as memory plus noise, in a fixed ratio.

**Probes.**
- **Van Hove [5]:** scattering measures the space-time pair correlation function, which becomes long-range near a critical point.
- **Manohar [6]:** a distant observer reads multipole coefficients b_lm ~ c_lm/Λ^l, and finite resolution caps l_max.
  - The short scale can be reached by more precise measurement at long distance, or by cruder measurement at short distance.
  - Coefficients that vanish reveal symmetries.
  - Processes forbidden at low order expose high scales: the proton decay rate goes as M_G^-4.
- **Gordon–Webb–Wolpert [7]:** different shapes can have the same spectrum.

**Amplification.**
- **Wilson [8]:** ions seed drops only above a critical expansion ratio: 1.25 for negative ions, about 1.31 for positive ions. This made single ions visible, and the threshold sorts them by sign.
- **Allahverdyan et al. [9]:** a metastable magnet, tipped by a weak coupling to the measured spin, registers the outcome.

**Dynamics.**
- **Sugihara et al. [10]:** the history of a driven variable carries redundant information about the state of its driver (Takens [11]).
  - Their example: "fish time series can be used to estimate weather, but not conversely."
  - Very strong forcing causes synchrony.
  - Causation is transitive along chains.
- **Liu et al. [12]:** every root strongly connected component of the system's inference graph needs its own sensor.
- **Schreiber [13]:** transfer entropy measures the direction of information flow.

**Irreversibility.**
- **Barato–Seifert [14]:** measuring a current to precision ε costs at least 2k_BT/ε² of dissipation.
- **Martínez et al. [15]:** asymmetry in waiting times gives a lower bound on hidden entropy production, even when no current is visible. The bound is tight only if all nonequilibrium variables are observed.

**Limits.**
- **Gutenkunst et al. [16]:** parameter-sensitivity eigenvalues span more than 10^6. A model whose every parameter was uncertain by more than 50× still predicted well.
- **Machta et al. [17], Transtrum et al. [18]:** argue that this Fisher-information (FIM) hierarchy is why universal and continuum theories exist.
- **Raju et al. [19]:** under coarse-graining, FIM distances along irrelevant directions shrink at rates set by the RG exponents.
- **Gordon et al. [20]:** what the information bottleneck keeps as relevant matches the operators with the lowest scaling dimension.
- **Laughlin–Pines [21]:** "one therefore learns little about the atomic structure of a crystalline solid by measuring its acoustics." The underlying theory is "unknowable until one raises the energy scale sufficiently to escape protection." Yet protected effects (Josephson, quantum Hall) give exact constants.
- **Apgar et al. [22]:** five complementary perturbations identified parameters that no single experiment could.
- **Pavliotis–Stuart and Papavasiliou et al. [23]:** fitting homogenized models to finely sampled data gives wrong parameters, unless the data are subsampled at an interval between the two timescales.

**Leaks.**
- **Touchette [24]:** large-deviation theory refines Gaussian fluctuation theory. My own reading: the tails keep more of the microscopic law than the central limit theorem does.
- **Jarzynski [25]:** free-energy estimates are dominated by rare realizations.
- **del Campo–Zurek [26]:** local symmetry-breaking choices freeze in as defects, with a density set by the quench rate.
- **Har Shemesh et al. [27]:** in Gray–Scott, the Fisher information peaks on the lines where pattern type changes.

## 2. Implications

**Each channel is a design choice.**
- **Fluctuation channel:** needs a finite, stochastic deep level. A deterministic mean-field g closes it.
- **Probes:** need perturbations the agent applies at scales it chooses.
- **Amplification:** needs metastable shallow states the agent can prepare.
- **Irreversibility:** needs a driven deep level.
- **Dynamical channel:** appears automatically whenever upward coupling is deterministic and injective.

**Coupling direction decides what is observable [10,12].**
- **Upward-only coupling:** the deep state can generally be recovered from shallow history when noise is low.
- **Downward-only coupling:** the deep level is invisible.
- **Strong two-way coupling:** synchronizes the levels and merges them.

**Bottleneck.** With coupling only between adjacent levels, everything the agent learns about h_0 has to pass through the trajectory of h_1. Transfer entropy per edge is therefore a hard budget, by the data-processing inequality (MEMORY).

**Define a level by contraction.** A many-to-one, local g plus separated timescales makes the Fisher information about deep parameters decay geometrically with depth [16–19]. A generic RNN block will tend to leak either everything or nothing.

**This fits the lead's framing.** Universal shallow levels expose only a few stiff combinations of deep parameters. Constructive deep levels are blocks with few parameters whose compositions generate everything above them.

## 3. Design principles and quantities

1. **Fisher-information audit.** Use autodiff through the world to get the Fisher information of the observations with respect to each level's parameters θ_i, for each instrument set. The number of eigenvalues above the noise floor is the "reachable depth". Tune basic instruments to reach 1–3 per level.
2. **Information budget.** Track I(h_i; o_{0:T}) with designer-side probes, plus transfer entropy on each edge.
3. **Gated amplifiers.** Add threshold or metastable units to the shallow block. Deep events register only after the agent prepares a unit, and the threshold selects which kind of event registers [8].
4. **Resolution ladders.** Give instruments settings for q, ω, precision and cost, with deep effects suppressed as (scale ratio)^n [6].
5. **Engineered leaks.** Make rare events, critical lines, quench defects and symmetry-forbidden processes the regimes where deep parameters become stiff. Check with the Fisher information that they actually do [27].
6. **Depth score.**
   - Predict the shallow consequences of held-out deep interventions do(θ_i), scored as predictions rather than as parameter values [16].
   - Check consilience: two independent channels must give the same deep constant, as in Perrin's work.
   - Ask for calibrated bounds, for example on hidden dissipation [14,15].

## 4. Pitfalls

- **Takens trap:** with low-noise deterministic coupling, a sequence model can recover the deep state without understanding anything. Add intrinsic deep noise or a many-to-one g.
- **Over-contraction:** held-out tasks may ask for quantities that cannot be identified. Check identifiability first.
- **Synchrony:** strong coupling merges levels.
- **Multiscale fitting bias [23]:** affects the designers' reference predictors as well as the agent.
- **Same spectrum, different structure [7]:** different deep structures can give identical spectra.
- **Weak channels:** some channels give only lower bounds [15], and rare-event channels need exponentially many samples [25].
- **Learned blocks:** blocks trained to reproduce known dynamics (Lenia-like) may lack the structure that makes deep details irrelevant at the top.

## 5. Open questions

- Should information about deep levels decay geometrically per level, or reach the top only through gates?
- Can universality be tested operationally, as the dimension of the set of deep blocks whose shallow statistics are indistinguishable?
- Should instruments be structures the agent builds inside the world, or tools with a cost?
- Are mutual-information estimates in high dimensions reliable enough to score with?
- How do we stop agents from memorizing the signatures of rare regimes?

## Sources (VERIFIED = I read the relevant part, MEMORY = not opened)

[1] A. Einstein (1905) Über die von der molekularkinetischen Theorie der Wärme geforderte Bewegung… Ann. Phys. 17:549. https://doi.org/10.1002/andp.19053220806 MEMORY
[2] J. Perrin (1926) Discontinuous structure of matter, Nobel lecture. https://www.mit.edu/~kardar/research/seminars/motility/PerrinNobelLecture.html VERIFIED
[3] R. Kubo (1966) The fluctuation-dissipation theorem. Rep. Prog. Phys. 29:255. https://doi.org/10.1088/0034-4885/29/1/306 VERIFIED (abstract)
[4] H. Mori (1965) Transport, collective motion, and Brownian motion. Prog. Theor. Phys. 33:423. https://doi.org/10.1143/PTP.33.423 VERIFIED (abstract)
[5] L. Van Hove (1954) Correlations in space and time and Born approximation scattering in systems of interacting particles. Phys. Rev. 95:249. https://doi.org/10.1103/PhysRev.95.249 VERIFIED (abstract, from a search excerpt; the APS page was blocked)
[6] A. V. Manohar (2018) Introduction to effective field theories (Les Houches). https://arxiv.org/abs/1804.05863 VERIFIED (sec. 2, proton decay)
[7] C. Gordon, D. L. Webb, S. Wolpert (1992) One cannot hear the shape of a drum. Bull. AMS 27:134. https://arxiv.org/abs/math/9207215 VERIFIED (abstract)
[8] C. T. R. Wilson (1927) On the cloud method of making visible ions and the tracks of ionizing particles, Nobel lecture. https://www.nobelprize.org/uploads/2018/06/wilson-lecture.pdf VERIFIED
[9] A. E. Allahverdyan, R. Balian, T. M. Nieuwenhuizen (2013) Understanding quantum measurement from the solution of dynamical models. Phys. Rep. 525:1. https://arxiv.org/abs/1107.2138 VERIFIED (abstract)
[10] G. Sugihara, R. May, H. Ye, C. Hsieh, E. Deyle, M. Fogarty, S. Munch (2012) Detecting causality in complex ecosystems. Science 338. https://doi.org/10.1126/science.1227079 VERIFIED (full text)
[11] F. Takens (1981) Detecting strange attractors in turbulence. Lect. Notes Math. 898. https://doi.org/10.1007/BFb0091924 MEMORY
[12] Y.-Y. Liu, J.-J. Slotine, A.-L. Barabási (2013) Observability of complex systems. PNAS 110:2460. https://pmc.ncbi.nlm.nih.gov/articles/PMC3574950 VERIFIED
[13] T. Schreiber (2000) Measuring information transfer. PRL 85:461. https://arxiv.org/abs/nlin/0001042 VERIFIED (abstract)
[14] A. C. Barato, U. Seifert (2015) Thermodynamic uncertainty relation for biomolecular processes. PRL 114:158101. https://arxiv.org/abs/1502.05944 VERIFIED (abstract)
[15] I. A. Martínez, G. Bisker, J. M. Horowitz, J. M. R. Parrondo (2019) Inferring broken detailed balance in the absence of observable currents. Nat. Commun. 10:3542. https://pmc.ncbi.nlm.nih.gov/articles/PMC6684597 VERIFIED
[16] R. N. Gutenkunst, J. J. Waterfall, F. P. Casey, K. S. Brown, C. R. Myers, J. P. Sethna (2007) Universally sloppy parameter sensitivities in systems biology models. PLoS Comput. Biol. 3:e189. https://doi.org/10.1371/journal.pcbi.0030189 VERIFIED
[17] B. B. Machta, R. Chachra, M. K. Transtrum, J. P. Sethna (2013) Parameter space compression underlies emergent theories and predictive models. Science, doi:10.1126/science.1238723. https://arxiv.org/abs/1303.6738 VERIFIED (abstract)
[18] M. K. Transtrum, B. B. Machta, K. S. Brown, B. C. Daniels, C. R. Myers, J. P. Sethna (2015) Sloppiness and emergent theories in physics, biology, and beyond. J. Chem. Phys. 143:010901 (venue MEMORY). https://arxiv.org/abs/1501.07668 VERIFIED (abstract)
[19] A. Raju, B. B. Machta, J. P. Sethna (2018) Information loss under coarse graining: a geometric approach. PRE 98:052112. https://arxiv.org/abs/1710.05787 VERIFIED (abstract)
[20] A. Gordon, A. Banerjee, M. Koch-Janusz, Z. Ringel (2021) Relevance in the renormalization group and in information theory. PRL 126:240601. https://arxiv.org/abs/2012.01447 VERIFIED (abstract)
[21] R. B. Laughlin, D. Pines (2000) The theory of everything. PNAS 97:28. https://pmc.ncbi.nlm.nih.gov/articles/PMC26610/ VERIFIED
[22] J. F. Apgar, D. K. Witmer, F. M. White, B. Tidor (2010) Sloppy models, parameter uncertainty, and the role of experimental design. Mol. BioSyst. 6:1890. https://dspace.mit.edu/handle/1721.1/76208 VERIFIED (abstract)
[23] G. A. Pavliotis, A. M. Stuart (2007) Parameter estimation for multiscale diffusions. J. Stat. Phys. 127. https://arxiv.org/abs/math/0603668; and A. Papavasiliou, G. A. Pavliotis, A. M. Stuart (2009) Maximum likelihood drift estimation for multiscale diffusions. Stoch. Proc. Appl. 119:3173. https://arxiv.org/abs/0806.3248 VERIFIED (both abstracts)
[24] H. Touchette (2009) The large deviation approach to statistical mechanics. Phys. Rep. 478:1. https://arxiv.org/abs/0804.0327 VERIFIED (abstract)
[25] C. Jarzynski (2006) Rare events and the convergence of exponentially averaged work values. PRE 73:046105. https://arxiv.org/abs/cond-mat/0603185 VERIFIED (abstract)
[26] A. del Campo, W. H. Zurek (2014) Universality of phase transition dynamics: topological defects from symmetry breaking. IJMPA 29:1430018. https://arxiv.org/abs/1310.1600 VERIFIED (abstract)
[27] O. Har Shemesh, R. Quax, A. G. Hoekstra, P. M. A. Sloot (2016) Information geometric analysis of phase transitions in complex patterns: the Gray-Scott reaction-diffusion model. J. Stat. Mech. 043301. https://arxiv.org/abs/1512.02077 VERIFIED (abstract)

Downloaded source texts are in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/lit2/deep-access/