# Embodied agent and apparatus for PhySim: literature review (4 Nov 2026)

Five surveys, an adversarial critique and a citation check. Corrections from the check are listed at the end; where a survey and the check disagree, the check wins.

---

## Survey: alife-embodied

**Lens: embodied agents and sensorimotor agency in CA and continuous ALife worlds**

## 1. Key works and what they show

**Beer, R.D. (2004). "Autopoiesis and Cognition in the Game of Life." *Artificial Life* 10(3):309–326.** https://cepa.info/fulltexts/1143.pdf. VERIFIED (pp. 309–318).
- Beer defines the glider as 5 ON cells plus their OFF boundary layer. All glider–environment interaction passes through that boundary.
- About 24 cells border the glider, so there are 2^24 possible perturbations. In "informal explorations" most of them destroy it, so its cognitive domain is "extremely limited." Beer blames its small size: there is little structural degeneracy, so there is little room for nondestructive change.
- The same perturbation phase-shifts or destroys the glider depending on its current state, so response depends on history.
- Whether a glider survived or was destroyed and rebuilt depends on how the observer defines its organization.

**Beer (2014). "The Cognitive Domain of a Glider in the Game of Life." *Artificial Life* 20(2):183–206.** https://direct.mit.edu/artl/article/20/2/183/2768. MEMORY (publisher page returned 403; I saw only abstract text through search). The nondestructive perturbations reportedly fall into six classes that make up the glider's Umwelt. A companion paper, Beer "Characterizing autopoiesis in the game of life," *Artificial Life* 21(1):1–19, is real (it appears in Biehl and Virgo's reference list), but I did not open it.

**Biehl & Virgo (~2023). "The game of life in a glider's frame of reference." ALIFE workshop abstract.** https://www.nichele.eu/ALIFE-DistributedGhost/7-Biehl.pdf. VERIFIED.
- Even reading out a moving body's state needs a frame transformation that re-centres the world on the body.
- Defining the glider's inputs and outputs is left as future work.

**Hamon, Etcheverry, Chan, Moulin-Frier, Oudeyer (2025). "Discovering sensorimotor agency in cellular automata using diversity search." *Science Advances* 11(44):eadp0834.** https://pmc.ncbi.nlm.nih.gov/articles/PMC12577699/. VERIFIED.
- **Setup:** multichannel Lenia on a 256² grid. Obstacles sit in a hand-engineered fixed channel with a rule that blocks matter from entering.
- **Sensing:** the body has no sensors. It "senses" only through deformation of its own structure, which the authors compare to touch.
- **Search results:** IMGEP plus curriculum plus gradient descent gave 486 moving patterns out of 1,600, with 261 above 0.95 obstacle robustness. Random search gave 30 moving and 20 robust out of 117,000 trials. Hand-found Lenia gliders often died on the obstacles.
- **Robustness:** near-perfect survival with up to 48 obstacles. Failures came from fast obstacles, noise above a threshold, small or symmetric initial disks, and down-scaling.
- **Collisions:** some produced a third entity.
- **"External control":** an attractive element whose rule was found by random search plus human assessment. It sometimes killed, exploded or replicated the agent.

**Plantec et al. (2023). "Flow-Lenia: towards open-ended evolution in cellular automata through mass conservation and parameter localization." ALIFE 2023 (best paper per Google Research listing); arXiv 2212.07906.** https://arxiv.org/abs/2212.07906. VERIFIED.
- Mass conservation makes most random parameter sets produce localized patterns.
- Optimizing ordinary Lenia for directed motion found only exploding patterns.
- Walls are a separate channel with a strong outward flow. Chemotaxis and food each need added channels.
- With parameters embedded in the matter (1024² grid, 144 creatures, 200k steps), species "take over" by contaminating each other.

**Mordvintsev, Niklasson, Randazzo (2022). "Particle Lenia." Google Research blog.** https://google-research.github.io/self-organising-systems/particle-lenia/. VERIFIED. The rotor is "quite sensitive to small perturbations." Multi-creature runs were left as future work.

**Randazzo & Mordvintsev (2023). "Biomaker CA." arXiv 2307.09320.** https://arxiv.org/abs/2307.09320. VERIFIED.
- Physics is kept separate from agent logic. Agent outputs pass through interfaces that are sanitized into valid operations, because "we cannot trust our agent logics to not exploit everything they can for survival." Energy cannot be created.
- Perception is the 3×3 neighbourhood. Movement is discouraged for connected organisms.
- Random initializations "will undoubtedly fail," so the authors hand-wrote starting parameters.
- **Extinction:** 43.75–68.75% in the "pestilence" configuration at 1,000 steps. "Sideways" was 0% at 1,000 steps but 18.75–81.25% at 10,000 steps, which the authors call "deceitful evaluations."

**Mordvintsev, Randazzo, Niklasson, Levin (2020). "Growing Neural Cellular Automata." *Distill*.** https://distill.pub/2020/growing-ca/. VERIFIED. Models trained only to grow die out or grow without limit. Persistence needed sample-pool training, and regeneration needed damage during training.

**Sudhakaran, Najarro, Risi (2022). "Goal-Guided Neural Cellular Automata." ICLR 2022 workshop "From Cells to Societies."** https://arxiv.org/abs/2205.06806. VERIFIED.
- A goal vector is added only to the hidden states of the body's living cells. This is internal-only control.
- Because the CA rule was co-trained with the goal encoder, a human could steer a salamander for thousands of steps on a 192² grid after training on 64².
- If 75% of cells receive the goal it still works. At 25–50% the shape is lost.

**Cvjetko, Hamon, Moulin-Frier, Oudeyer (2025). "Discovering and Controlling Diverse Self-Organised Patterns in Cellular Automata Using Autotelic RL." Short paper, venue not stated on the PDF.** https://developmentalsystems.org/rl-for-ca/lba.pdf. VERIFIED. States that "all automated discovery methods applied to CAs so far have been open-loop." The RL agent learns to steer an Orbium.

**Cvjetko, Hartl, Levin, Moulin-Frier, Oudeyer (2026). "The Artificial Experimentalist." arXiv 2608.26116 (accepted ALIFE 2026 per arXiv comments).** https://arxiv.org/abs/2608.26116. VERIFIED.
- **Action:** add or remove 0.3 mass within radius 5 anywhere on the grid, with an action cost.
- **Observation:** the last 4 full 64² grids.
- **Steering (cosine similarity):** 0.91 on training conditions, 0.81 for unseen directions, 0.76 for unseen solitons and directions together.
- **Cost:** about 10^6 transitions. The maze demo is qualitative only.
- **Failures:** solitons hitting walls "disintegrate or explode," and the agent "generally cannot recover a disrupted pattern."

**Cool, Hartl, Levin, Petti (2026). "Agnosiophobia in a virtual agent." arXiv 2605.30708 (under review, ALIFE 2026).** https://arxiv.org/abs/2605.30708. VERIFIED.
- "Sensing" is defined as the kernel-convolution input. Blind regions are masked out of the convolution.
- Three of four catalogued creatures turn away from blind regions. S1s dies on contact with them.
- Mapping 3×3 occlusions over the body shows that heading changes come from the body maintaining its own shape.

**Froese, Virgo, Ikegami (2014). "Motility at the origin of life." *Artificial Life* 20(1):55–76; arXiv 1311.2531.** https://arxiv.org/abs/1311.2531. VERIFIED (pp. 8–19).
- In Gray-Scott, a "virtual pipette" can steer spots: feeding attracts them, overfeeding splits them, and withdrawing material repels them. A pipette moved too fast or too close kills the spot.
- Adding a waste product gives self-propulsion. One spot trapped itself in its own waste and died.

**Sims, K. (1994). "Evolving Virtual Creatures." SIGGRAPH '94, pp. 15–22.** https://www.karlsims.com/papers/siggraph94.pdf. VERIFIED.
- Sensors are hand-designed: joint angle, contact and photosensors.
- "Any bugs that allow energy leaks from non-conservation, or even round-off errors, will inevitably be discovered and exploited."
- Light-following creatures "can be led around in arbitrary paths by movement of the light sources."
- The companion paper, Sims (1994) "Evolving 3D Morphology and Behavior by Competition," *Artificial Life IV*, is MEMORY.

**Bhatia et al. (2021). "Evolution Gym." NeurIPS 34.** https://arxiv.org/abs/2201.09863. VERIFIED (abstract only). "All tested algorithms fail to find robots that succeed in our hardest environments."

**Further sources (lighter):**
- **Agmon, Gates, Churavy, Beer (2016).** "Exploring the space of viable configurations in a model of metabolism–boundary co-construction," *Artificial Life* 22(2):153–171. MEMORY; abstract snippet only. Proposes viability as average expected survival time under ongoing perturbation.
- **Michel et al. (2025).** "Exploring Flow-Lenia Universes with a Curiosity-driven AI Scientist," arXiv 2505.15998. VERIFIED. An open-loop parameter search that observes only global statistics.
- **Kumar et al. (2024).** ASAL, arXiv 2412.17799. VERIFIED (abstract). Foundation models used as judges of ALife simulations.

## 2. Feasibility

**Viable bodies exist, but they are rare, must be searched for, and survive only a narrow range of interactions.**
- Hamon needed an elaborate search to find them. Biomaker needed hand-written parameters. Growing NCA needed pool and damage training.
- Robustness breaks under fast impacts, noise above a threshold, scale changes, wall contact (CARL), and small perturbations (Particle Lenia rotor).
- Beer's explanation applies here: robustness needs structural degeneracy. The body has to be large compared with the size of the perturbations and actions it meets.
- Biomaker shows that surviving 1,000 steps does not predict surviving 10,000.

**Sensing is never canonical; someone always designs it.**
- In the verified work it is either implicit or hand-designed. Implicit forms are body deformation (Hamon), the convolution input (Agnosiophobia) and the boundary interface (Beer). Hand-designed forms are Sims's sensors, Biomaker's 3×3 view and NCA Sobel filters.
- For an external AI "inside" a blob, someone must still define which cells count as the body and what reading it gets. Beer, Froese and Biehl all show that body boundaries and identity depend on the observer.
- **Embodiment moves the non-canonical choices into the world's rules rather than removing them.** Walls are a special channel with a special rule in both Hamon and Flow-Lenia, the attractive element was picked by humans, and food is an added channel.

**Did an external controller drive an embodied body?** Yes, but always with a god's-eye view.
- CARL edits mass anywhere on the grid and sees the full grid.
- Froese's pipette, Sims's moving light and Hamon's attractive element all act on the environment around the body.
- GoalNCA is the only case of internal-only actuation, and it worked because the body's rule was trained together with the controller.

I found no work in which an AI agent's observations were limited to what its own body senses, and none in which a CA or continuum body built a tool or instrument. That is an absence of evidence after about 15 searches, not proof none exists.

**Controllers will exploit any leak.** Sims says so directly, and Biomaker sanitizes every action for the same reason.

## 3. Usefulness for evaluating scientific method

- **Closed loop does not need embodiment.** The strongest support for the lead's motivation is the claim that all CA discovery so far was open-loop, together with CARL's success at closed-loop steering. But CARL got closed loop from an external, full-view apparatus. Three possible gains should be tested separately: closed-loop feedback, local or partial observation, and building instruments. Only the third strictly needs a body, and it has no precedent in this literature.
- **A body is a biased instrument.** Its response depends on its state and history (Beer), and its behaviour follows its own self-maintenance (Agnosiophobia). Measurements made through it mix world properties with body dynamics. That is realistic, because calibrating instruments is part of science, but it makes held-out scoring harder.
- **The eval could turn into a control or RL task.** CARL needed about 10^6 transitions to steer one soliton. An LLM agent on a limited budget may spend most of it keeping its body alive. Score survival separately so it cannot pass for scientific skill.

## 4. Design lessons

1. **Build the agent body as engineered apparatus, not a native creature.** Give it a protected identity: a tagged channel or a sanitized-action interface as in Biomaker. Pre-qualify it with a perturbation battery like Hamon's 9 families × 5 strengths, measure survival time as Agmon proposes, and test over at least 10× the episode length.
2. **Enforce conservation in actuation.** The body should move or exchange existing material and never create it (Biomaker, Flow-Lenia). Otherwise expect exploits.
3. **"Changing internal balances" needs spatially resolved degrees of freedom to steer.** Uniform internal controls only change size or mass. Hamon's small or symmetric disks died. GoalNCA's directional control was learned.
4. **Define sensing as what crosses the boundary**, for example fluxes through the body boundary plus changes in internal content (Beer's interface). Publish it as a fixed operator and check it is informative with per-location occlusion maps, as in Agnosiophobia.
5. **Use a separate, stable phase as building material.** Walls were a separate channel with simple rules in Hamon and Flow-Lenia. My inference: in our worlds this could be a deposited Cahn-Hilliard domain. Otherwise anything built dissolves.
6. **Climb in steps and measure the gain at each one:**
   - add closed loop and local observation to the current probes (CARL-style);
   - add a tethered body with internal-only control (GoalNCA-style);
   - only then a free body that can construct.
7. **Keep a referee instrument fixed for scoring.** Score held-out predictions in terms of world properties, not the agent's own home-made instruments.

## 5. Open questions

- Can any continuum or CA body move or deposit material to build a lasting structure without destroying itself? I found no example.
- Can an LLM, rather than RL with about 10^6 samples, learn to steer a fragile body within an eval's budget?
- How can co-evolving instruments be scored when an energy score needs a fixed apparatus?
- Does embodiment measure anything that closed loop plus partial observation does not?
- **Cross-world reuse:** Flow-Lenia's parameter embedding hints that one "agent species" could be dropped into many worlds, but only within the Lenia family. Is there a world-agnostic body?
- **Not opened:** I did not read Beer (2014) beyond its abstract, or Agmon et al. (2016) at all. Their numbers should be checked before anyone relies on them.
---

## Survey: ai-discovery-envs

**Lens: AI scientific-discovery environments and benchmarks, and how they define the agent's interface to the world**

All sources below were found and opened with the built-in WebSearch/WebFetch. No firecrawl tools were used.

## 1. Key works and what they actually show

**A. Text or symbolic labs with instruments supplied**

- **ScienceWorld** (Wang, Jansen, Côté, Ammanabrolu 2022, EMNLP; arxiv.org/abs/2203.07540) [VERIFIED]
  - Interface: 25 templated text actions (about 200k combinations), plus a "valid-action" aid that all but two agents needed at test time.
  - Simulation: engines for thermodynamics, circuits, chemistry, genetics and inclined planes; 30 tasks; scored by subgoals (0–1).
  - Results: DRRN (1.5M params) 0.17; behaviour cloning and decision transformer on T5-11B 0.08; random 0.03.
  - Failures: plausible but invalid actions; agents do not use knowledge they already have (they rerun a conductivity experiment rather than recall that a fork conducts).
- **DiscoveryWorld** (Jansen, Côté, Khot, Bransom, Dalvi Mishra, Majumder, Tafjord, Clark 2024, NeurIPS D&B; arxiv.org/abs/2406.06769) [VERIFIED]
  - Interface: 14 discrete actions. Instruments are given ready-made (spectrometer, densitometer, etc.). There is no action to build or modify an instrument.
  - Three scores: binary task completion; a procedural scorecard of relevant actions; explanatory knowledge, checked as binary questions by a GPT-4o judge.
  - Results: Hypothesizer, ReAct and Plan+Execute reach about 18–23% completion on Normal tasks and 1–10% knowledge on Challenge tasks. Human MSc/PhD scientists: 66% completion, 55% knowledge.
  - Ten "unit-test" tasks (navigation, pick-and-place, using an instrument) separate interaction skill from discovery: agents score 44–64% there but fail at discovery.
  - Failures: distractors, context truncation, and completing tasks without the correct explanation.

**B. Experiments as calls to an oracle (no body)**

- **BoxingGym** (Gandhi, Li, Goodyear, Bhatia, Li, Bhaskar, Zaman, Goodman 2025, arXiv; arxiv.org/abs/2501.01540) [VERIFIED]
  - 10 probabilistic-model environments; at most 10 natural-language designs per run.
  - Metrics: EIG regret; prediction error standardized against the prior; "communication", where a novice predicts from the scientist's explanation.
  - Failures: GPT-4o keeps strong wrong assumptions (e.g. symmetric decay); error sometimes rises with more data; priors often hurt; good prediction does not imply good design; Box's Apprentice falls back to linear fits.
- **NewtonBench** (Zheng, Tam, Nguyen et al. 2025, arXiv, listed as ICLR 2026; arxiv.org/abs/2510.07172) [VERIFIED; venue from listing]
  - 324 tasks built from counterfactually shifted laws; up to 10 rounds of 20 queries each.
  - GPT-5 symbolic accuracy falls from 87.5% (bare equation) to 40.3% (complex system).
  - Even 1e-4 observation noise costs 12–16 points.
  - A code interpreter slightly hurts strong models, which settle early on curve fits.
- **PhysGym** (Chen, Piękos, Ostaszewski, Laakom, Schmidhuber 2025, NeurIPS D&B; arxiv.org/abs/2507.15550) [VERIFIED]
  - 97 problems, 100-experiment budget.
  - Removing context and variable names roughly halves success (Gemini-2.5-pro 74% to 32%).
  - Models anchor on recalled physics and choose "realistic" inputs that carry little information.

**C. Embodied worlds with hidden structure (RL agents)**

- **Alchemy** (Wang, King, Porcel, Kurth-Nelson, … Botvinick 2021, NeurIPS D&B; arxiv.org/abs/2102.02926) [VERIFIED]
  - Episode scores: VMPO 156, IMPALA 140, random heuristic 146, Bayes ideal observer 284.
  - The symbolic version (no navigation) also gives VMPO 155. Removing the motor problem did not help: the bottleneck was structure inference, not control.
  - VMPO's actions did reduce posterior entropy, but it did not use what it learned.
  - Feeding in the ideal observer's belief state, or adding auxiliary prediction tasks, closed most of the gap.
- **Denil et al.** (Denil, Agrawal, Kulkarni, Erez, Battaglia, de Freitas 2016/17, arXiv; ICLR 2017 [MEMORY]; arxiv.org/abs/1611.01843) [VERIFIED]
  - Agents poke blocks to infer hidden mass or count rigid bodies.
  - Reward comes only from a "label" action, and the discount sets the cost of information.
  - Agents learn adaptive experiment lengths. The authors explicitly say they did not address theory-building.
- **XLand** (Open Ended Learning Team 2021, arXiv; arxiv.org/abs/2107.12808) [VERIFIED]
  - Participation 95%; 10th-percentile normalized score 82%.
  - "Experimentation" and ramp-making appear only as qualitative probe episodes.
  - Fails zero-shot on gaps and on building several ramps.
  - Normalizers come from co-players, so scores are not fixed.
- **AdA** (Adaptive Agent Team 2023, arXiv; arxiv.org/abs/2301.07608) [VERIFIED abstract only]: claims hypothesis-driven exploration at human timescales.
- **Hide-and-seek** (Baker, Kanitscheider, Markov, Wu, Powell, McGrew, Mordatch 2019, arXiv; ICLR 2020 [MEMORY]; arxiv.org/abs/1909.07528) [VERIFIED]
  - Shelter-building and ramp use emerge; ramp defense arrives after 132M episodes, box surfing after about 380M.
  - Transfer gains over intrinsic-motivation baselines are "not drastic".
  - Agents exploited physics-engine inaccuracies.
  - The authors say judging progress by qualitative observation "will become intractable".

**D. Explore without reward, then a separate test**

- **WorldTest/AutumnBench** (Warrier, Nguyen, … Tenenbaum, Ellis, Tavares 2025, arXiv; arxiv.org/abs/2510.19788) [VERIFIED]
  - A reward-free interaction phase, then scoring in a *derived* environment: masked-frame prediction, change detection, planning.
  - Humans (517) beat every model in every environment.
  - Models spend under 7% of actions on resets or no-ops; humans use each about 12.5% of the time. Models also fail to revise rules after seeing contradicting evidence.
- **ARC-AGI-3** (ARC Prize Foundation, 22 Apr 2026, technical report; arcprize.org/media/ARC_AGI_3_Technical_Report.pdf) [VERIFIED]
  - No instructions or goals; 64×64 grid observation; small action set "so the complexity … lies in the logic … not the difficulty of the controls".
  - Score is squared action efficiency relative to the upper-median human, capped at 1.15.
  - Humans solve 100% of environments; frontier AI scores under 1%.

**E. Embodied lab with physical apparatus**

- **EmbodiedLab** (Gao, Zheng et al., 26 Oct 2026, arXiv; arxiv.org/abs/2610.35385) [VERIFIED]
  - 30 experiments on 14 physical apparatus platforms; the agent works a robot arm through cameras.
  - Three tiers: T0 (raw joint control), T1 (adds segmentation and motion planning), T2 (adds a skill library).
  - Each failure is attributed to its first decisive error. Acting, observing and restoring the bench cause 75–100% of failures; "knowing" causes at most 25%.
  - Best agent at T0: 43.3%. Perception and planning help by at most 10 points; distilled skills add 10–27 points.
  - Gates require that cited readings came from instruments used in the episode. Apparatus is given, never built.

**F. Open-ended tool and crafting worlds**

- **Voyager** (Wang, Xie, Jiang, Mandlekar, Xiao, Zhu, Fan, Anandkumar 2023, arXiv; arxiv.org/abs/2305.16291) [VERIFIED]
  - Code is the action space (Mineflayer primitives); text-only state; a self-growing skill library.
  - Results: 3.3× more items; tech-tree milestones up to 15.3× faster.
  - Removing self-verification cuts items by 73%. It hallucinates items and API calls.
- **MineDojo** (Fan et al. 2022, NeurIPS 2022 D&B Outstanding Paper; arxiv.org/abs/2206.08853) [VERIFIED]
  - 1,581 programmatic and 1,560 creative tasks; creative tasks are judged by a learned MineCLIP classifier.
- **Crafter** (Hafner 2021, ICLR 2022; arxiv.org/abs/2109.06780) [VERIFIED]: score is a geometric mean over 22 achievements; human experts 50.5%, DreamerV2 10.0%.
- **Craftax** (Matthews, Beukman, Ellis, Samvelyan, Jackson, Coward, Foerster 2024, arXiv; ICML 2024 [MEMORY]; arxiv.org/abs/2402.16801) [VERIFIED]: runs up to 250× faster than Crafter; exploration and environment-design methods make no material progress on the full benchmark.
- **Kinetix** (Matthews, Beukman, Lu, Foerster 2024, ICLR 2025; arxiv.org/abs/2410.23208) [VERIFIED]
  - Fixed reward (green touches blue); entity-set observations; 74 handmade held-out levels.
  - Car-Ramp is solved zero-shot about 5% of the time; needs billions of steps.

**G. Inventing apparatus and measurement procedures**

- **Melnikov, Poulsen Nautrup, Krenn, Dunjko, Tiersch, Zeilinger, Briegel 2018**, PNAS 115:1221 (arxiv.org/abs/1706.00868) [VERIFIED abstract]: an RL agent assembles optical setups and rediscovers standard techniques.
- **Krenn, Drori, Adhikari 2025**, PRX 15:021012 (arxiv.org/abs/2312.04258) [VERIFIED abstract]: more than 50 AI-found gravitational-wave detector designs that beat next-generation designs.
- **EvalResearchBench** (Zhang, Xu, Zhao, Zhao, Wu, Wang, Oct 2026, arXiv; arxiv.org/abs/2610.04184) [VERIFIED]
  - The agent builds a measurement instrument (an evaluator), scored against 14 sealed targets by Lin concordance and pairwise agreement.
  - Best evaluator: about 75% pairwise agreement against a 91% ceiling. Only 4 of 8 beat a random human-designed sample on agreement.
  - Fitting the visible targets did not transfer to the sealed ones.

**H. Passive law discovery and bodies in cellular automata**

- **AI Physicist** (Wu & Tegmark 2019, PRE 100:033311; arxiv.org/abs/1810.10525) [VERIFIED]: learns from passive trajectories only; prediction error about 1e9 times lower than a neural-net baseline.
- Related passive work [MEMORY]: AI Feynman (Udrescu & Tegmark 2020, Sci. Adv.) and Schmidt & Lipson 2009 (Science).
- **Hamon, Etcheverry, Chan, Moulin-Frier, Oudeyer 2025**, Sci. Adv. 11:eadp0834 (arxiv.org/abs/2402.10236) [VERIFIED abstract]: diversity search *finds* rules under which moving, self-maintaining "agents" navigate obstacles. Nothing is built or steered.
- **Deep Adaptive Design** (Foster, Ivanova, Malik, Rainforth 2021, ICML; arxiv.org/abs/2103.02438) [VERIFIED abstract]: closed-loop experiment design in milliseconds per step.

## Answers to the lens questions

- **Does any benchmark score method or instrument invention?** I found none that scores building physical instruments inside a world. Instruments are supplied (DiscoveryWorld, EmbodiedLab), or tool-building is only observed (hide-and-seek, XLand).
  - Closest templates: EvalResearchBench (the instrument is judged by how well it agrees with a sealed reference) and Krenn/Melnikov (designs judged by a physical figure of merit, as an optimization problem, not as an agent benchmark).
- **How embodied benchmarks separate control from understanding:**
  - Control-only unit tests (DiscoveryWorld).
  - A symbolic interface versus 3D (Alchemy).
  - Interface tiers plus first-error attribution (EmbodiedLab).
  - A minimal action set (ARC-AGI-3).
  - Reward only for the answer action (Denil).
  - A reward-free exploration phase followed by a separate test (WorldTest).
- **Evaluation targets:**
  - Prediction (BoxingGym, WorldTest, AI Physicist).
  - Symbolic equivalence to the true law (NewtonBench, PhysGym).
  - Explanations (DiscoveryWorld's judge; BoxingGym's novice).
  - Goals or achievements (ScienceWorld, Crafter, XLand, Kinetix).
  - Action efficiency (ARC-AGI-3).
  - Design information (EIG regret).

## 2. Feasibility

- **LLM agents fail mostly at the body, not the physics.** EmbodiedLab shows this even with a rigid arm and real apparatus. A soft blob that the agent controls only through internal field balance is a harder control problem, and I found no evidence that LLM agents can steer one.
- **RL agents get construction only at huge cost.** Hide-and-seek needed 100M+ episodes, and its world had objects with designed affordances (boxes, ramps, locks). Continuum worlds have no persistent rigid parts.
- **Bodies in a CA are possible, but they are found, not built.** Hamon et al. show self-maintaining moving bodies exist under search, but they are not built to order and not steered by a planner.
- **The practical route for LLM agents is a code layer over the body.** Voyager's code-as-action and EmbodiedLab's skill libraries make embodiment workable. But that primitive layer is a designer-chosen apparatus again: embodiment moves the arbitrary choice from the probes into the body physics and the primitives. It does not remove it.
- **Sensing through one's own body is low-bandwidth.** With full-grid views, LLM agents already explore poorly (WorldTest, ARC-AGI-3). Narrower sensing will make this worse.

## 3. Usefulness as an evaluation of scientific method

- **Expect the score to measure the body.** By EmbodiedLab's evidence, a naive embodied PhySim would mostly measure motor competence.
- **Removing the body is not sufficient either.** Alchemy shows that removing the control problem leaves structure inference as the bottleneck.
- **The benefits are real but obtainable more cheaply.** Closed-loop design (DAD, Denil, WorldTest resets) and targeting moving objects could be added to the external apparatus as adaptive programs.
- **Method invention is a real gap in the literature.** Nobody scores it, so a benchmark that measured the gain from agent-built instruments would be new.
- **Specific risks:**
  - Exploiting the simulator, as in hide-and-seek. On grids this means agents building "instruments" that read off discretization artifacts.
  - Credit assignment: did the instrument or the inference produce the result?

## 4. Design lessons

1. **Ablate the interface by tier.** Run each world as external apparatus, embodied with primitives, and embodied raw (as in EmbodiedLab or Alchemy). Report the difference as the cost of embodiment.
2. **Test the body without hidden physics.** Use control-only unit tests in a null world (as in DiscoveryWorld) and report discovery conditional on passing them.
3. **Keep the final score independent of the agent's own instrument.** Let the agent explore embodied, then score held-out predictions of canonical interventions through a frozen reference apparatus (a WorldTest-style derived test).
4. **Score built instruments by validity, not by appearance.** Measure how well an instrument's readings agree with the hidden true field quantity (Lin concordance, as in EvalResearchBench). Add gates: cited readings must come from that instrument (EmbodiedLab), and the agent must restore or clean up the setup it built.
5. **Price actions and make resets and waiting explicit.** Use squared action efficiency against a reference (ARC-AGI-3), and include explicit reset and no-op actions (WorldTest).
6. **Compute ideal-observer references** for small subtasks (Alchemy), and set the cost of information explicitly (Denil).
7. **Block recall of textbook physics.** Use counterfactual law shifts (NewtonBench) and remove names and context (PhysGym).
8. **Allow self-written tools.** Let the agent write and modify its own primitives and analysis code (Voyager, EmbodiedLab T2). For LLM agents, this software layer is the realistic channel for methods and instruments to co-evolve.
9. **Check constructions for numerical artifacts.** Re-run built setups at a finer resolution; anything that disappears is an exploit.
10. **Add a novice-transfer check on explanations** (BoxingGym) as a secondary score.

## 5. Open questions

- No study holds a discovery task fixed and compares embodied against disembodied interfaces for LLM agents, except EmbodiedLab's tiers and Alchemy's 3D-versus-symbolic comparison (where both ran near random).
- Can structures in continuum worlds persist without the agent present? Without that, construction is ill-posed.
- How can instrument invention be credited without rewarding exploits, and without the designer choosing a "canonical" instrument after the fact?
- Does a shared body layer across worlds destroy the independence between worlds, or can the body be a passive tracer that is calibrated in each world?
- How many bits per step can the agent sense through its own field content, compared with what the hidden laws need?
---

## Survey: philosophy-instruments

**Lens report: philosophy, history and sociology of experiment and instruments, plus the thermodynamics of embedded observers**

All sources were found with the built-in WebSearch and WebFetch tools only; no firecrawl tools were used. Each source is tagged in the list at the end. VERIFIED means I opened it and read the relevant part. VERIFIED-secondary means I read a reliable summary but not the primary text. MEMORY means I did not open it.

### 1. Key works and what they actually show

- **Hacking (1983) [R1].** He argues that experiment "has a life independent of theory." Chapter 13 adds that scientists often "create the phenomena which then become the centrepieces of theory." On microscopes, belief comes from two things: the image stays the same across instruments built on different physics, and intervening (for example staining the sample) gives the predicted change [R2]. His realism criterion, "if you can spray them, then they are real" (p. 24), rests on using an entity as a tool [R3].
- **Hacking (1992) [R4] and Pickering (1995) [R5].** Laboratory science becomes stable when ideas, apparatus and readings are adjusted until they support each other. Hacking calls the result "mutually self-vindicating." Pickering treats the apparatus, the model of the instrument and the model of the phenomenon as all open to change, and calls mutual support "the defining characteristic of the successful experiment." Hacking himself warns that this stability does not prove the science is true [R2].
- **Chang (2004) [R6–R8].** Temperature faced the "problem of nomic measurement": the laws needed to justify a thermometer could only be tested with a thermometer you already trusted. It was solved by "epistemic iteration," a coherentist process of "enrichment and self-correction of the initially affirmed system." Fixed points had to be manufactured, not found. Chang repeated the historical experiments: vessel material shifts the boiling temperature by more than 3°C, and de-gassed water reaches 108–109°C. Thermometers calibrated on the assumption that water boils at 100°C were used to show that it often does not. Regnault picked the air thermometer because instruments of the same type agreed with each other ("comparability") [MEMORY]. Bridgman's operationalism: "If we have more than one set of operations, we have more than one concept" [R8]. Kuhn argued the opposite direction, theory first and measurement after [R7].
- **Rheinberger (1994, 1997) [R9–R11].** Experimental systems are "the smallest integral working units of research." They are designed to give answers to questions the experimenters cannot yet clearly ask, and research "begins with the choice of a system rather than with the choice of a theoretical framework." Once stabilized, an object of inquiry (an "epistemic thing") becomes part of the toolkit (a "technical object"). Zamecnik's cell-free protein synthesis system was built to study cancer. It was later repurposed: Nirenberg added poly-U and cracked the UUU codon.
- **Baird (1998, 2004) [R12, R13].** Instruments are a form of knowledge in their own right. The direct-reading spectrometer took over "the skills and knowledge previously required of human operators." Building an instrument needs "dependable regularities in material behavior," and "creating a phenomenon requires the same kind of adaptive Popperian error elimination as creating a theory."
- **Galison (1987, 1997) [R2, R14].** An experiment ends when the result "will stand up in court," and theory decides what counts as signal and what counts as background. In the neutral-current case, Monte Carlo background estimates were decisive (from a Franklin review snippet; MEMORY). *Image and Logic* adds two detector traditions (picture-based "golden events" versus statistics over many counts) and "trading zones" where instrument makers, theorists and experimentalists exchange knowledge.
- **Collins (1975, 1985) [R15–R17].** The experimenter's regress: "a good experimental apparatus is simply one that gives correct results," so replication alone cannot settle a dispute. TEA laser: everyone who tried to build one from published articles failed; only people who had spent time in a lab with a working laser succeeded. Franklin's reply [R2]: calibrate with surrogate signals that are established independently. Weber's detector could not detect injected pulses of known energy; the rival detectors could.
- **Steinle (1997) [R18].** Exploratory experimentation is the normal mode when "no conceptual framework is readily available."
- **Szilard (1929) [R19].** He defines measurement as coupling a pointer variable y to a fluctuating variable x, then uncoupling them so that y keeps a memory of x. He replaces the "intelligent being" with a simple non-living device inside the system, and finds an entropy cost of k log 2 per measurement, just enough to protect the Second Law.
- **Landauer (1961) [R20].** Logically irreversible operations need dissipation of about kT each. That dissipation "serves the purpose of standardizing signals and making them independent of their exact logical history."
- **Bennett (2003) [R21].** Measurement and copying can in principle cost nothing; the cost sits in overwriting or erasing records. He separates "externally clocked" machines, where an outside agency drives a control parameter, from fully Brownian machines, where the agency has "let go of the handle." He also concedes Earman and Norton's point: if the demon obeys the Second Law, no extra principle is needed.
- **Bérut et al. (2012) [R22] and Toyabe et al. (2010) [R23].** Bérut measured erasure heat for a colloidal one-bit memory: it "saturates at the Landauer bound in the limit of long erasure cycles." Toyabe used position measurement plus feedback to make a particle gain more free energy than the work done on it.

### 2. Feasibility

- **Instruments are historically built from the world's own stable regularities.** Thermal expansion became the thermometer; a cell extract became the protein-synthesis assay; manipulated electrons became tools. So feasibility in PhySim depends on whether each world has what Baird requires: local structures that can be built reliably, last long enough, can be reused and respond in a known way.
  - Candidates: membranes as barriers or moats, condensate droplets as fuel sensors (through their growth rate), vortices as stirrers, a droplet's relaxed radius as a ruler or clock.
  - If built structures merge, coarsen or diffuse away faster than an experiment runs, construction fails. This is an empirical property of each world and should be measured before committing.
- **Sensing is coupling, so back-action comes with it.** On Szilard's definition, the body's internal fields act as the pointer, and in a dissipative PDE diffusion erases that record within a finite time. A body in a Cahn-Hilliard or reaction-diffusion field also changes the local chemistry it is sensing. Every reading disturbs the world. That is acceptable, since Hacking says phenomena are created anyway, but the disturbance has to be modelled rather than ignored.
- **The current apparatus is Bennett's externally clocked machine.** An embodied body moves toward letting go of the handle. The LLM's memory and reasoning stay outside the simulation, though, so this is a teleoperated rover, not an embedded observer.

### 3. Usefulness as an evaluation of scientific method

- **The core claim has strong support.** Hacking 1992, Pickering, Chang and Rheinberger all treat co-adjustment of apparatus and theory as what makes discovery possible. A fixed apparatus fixes the operational concepts the agent can form (Bridgman). It also rules out three standard moves: checking robustness across physically different instruments (Hacking), building a scale from comparability (Chang), and calibrating against independent surrogate signals (Franklin). It cannot run the starve-one-cell experiment either.
- **That is also where the risk lies.** An agent that builds its own instruments can build ones that confirm its own theory; this is the regress and Hacking's self-vindication worry.
- **A simulation is the one setting where the regress can be broken by design,** because the evaluator has ground truth. That advantage only holds if the score is independent of the agent's own apparatus. Today's held-out programs run "through the same apparatus," which measures predictions only within that apparatus's operational concept.

### 4. Design lessons

1. **Inventory technical objects per world first.** List the structures that can be built, and measure how reproducibly they form (spread across repeated builds), how long they last relative to an experiment, and how predictable their response is. These are Chang's "manufactured fixed points." Do not embody a world that fails this test.
2. **Add an anti-demon rule.** Internal actuation must obey the world's conservation laws and fuel budgets. A body that rebalances its fields for free is a Maxwell's demon: it changes the physics it is supposed to be studying.
3. **Use no privileged readouts.** The only sensors are the body's own field content. Measure the disturbance the agent causes as a separate quantity, and state whether claims are about the world without the agent or the world with it.
4. **Score against ground truth that does not depend on the agent.** Use predictions of field dynamics, or responses measured by a held-out standard instrument the agent never had. Also have the agent state what each of its instruments measures, and check that statement against truth.
5. **Plant artifacts.** Include effects caused by the body itself that only a cross-instrument check or a calibration can expose. This tests Galison's effect-versus-artifact judgement and Franklin's calibration strategies directly.
6. **Build a ladder of apparatus tiers and test it.** Tier 0: today's apparatus. Tier 1: closed-loop programs, reusable instruments that keep state, and the ability to calibrate probes against standards the agent builds. Tier 2: full embodiment. Check whether tier 2 reaches hidden mechanisms that tier 1 cannot. Much of Rheinberger's turning of objects into tools may be possible at tier 1 for a fraction of the cost.
7. **Episodes must be long enough to allow failed builds.** Collins's tacit-knowledge result means construction know-how is learned by doing, not from a written manual. Chang's iteration needs at least two or three refine-and-recalibrate cycles.

### 5. Where the analogy breaks, and open questions

- **The LLM's memory and records are outside the world.** The thermodynamic costs of Szilard, Landauer and Bennett apply only to the body. Our PDEs are also deterministic and have no kT, so the bounds do not carry over literally. The closest analogues are conservation laws, finite resolution and memory limited by diffusion.
- **The social side is missing.** Collins and Galison describe closure as a community process (replication, trading zones, standing up in court). A single agent scored against ground truth tests individual method only, unless the setup becomes multi-agent.
- **Timescales differ by orders of magnitude.** Temperature took about 150 years; an episode takes hours.
- **One part of the analogy gets stronger.** Inside the simulation, instruments and objects are literally made of the same fields, which fits Hacking's "use the entity as a tool" better than real laboratories do.
- **Open questions:**
  - Do any of our four worlds pass the technical-object inventory?
  - How do we score instrument building without process scores that agents can game?
  - Can one body interface (a body as a set of conserved internal species behind a permeable boundary) work across different PDE families, and so reduce the loss of independence between worlds?
  - Does tier 2 beat tier 1 on discovery, or only on cost?

### Sources

- R1. Hacking, I. 1983. *Representing and Intervening*. Cambridge UP. https://www.cambridge.org/core/books/representing-and-intervening/F6506B708BB5A8B6A5D884BDCF28E7B7 — VERIFIED (contents and summaries of chapters 9 and 13).
- R2. Franklin, A. & Perovic, S. "Experiment in Physics." SEP, revised 2023. https://plato.stanford.edu/entries/physics-experiment/ — VERIFIED.
- R3. Wikipedia, "Entity realism" (for the p. 24 quote). https://en.wikipedia.org/wiki/Entity_realism — VERIFIED-secondary.
- R4. Hacking, I. 1992. "The self-vindication of the laboratory sciences." In A. Pickering (ed.), *Science as Practice and Culture*, U Chicago Press, pp. 29–64 — VERIFIED-secondary via R2.
- R5. Pickering, A. 1995. *The Mangle of Practice*. U Chicago Press — VERIFIED-secondary via R2.
- R6. Chang, H. 2004. *Inventing Temperature*. Oxford UP. https://academic.oup.com/book/5530 — VERIFIED (chapter 5 abstract); Regnault detail is MEMORY.
- R7. Tal, E. "Measurement in Science." SEP, revised 2020. https://plato.stanford.edu/entries/measurement-science/ — VERIFIED; this also covers Kuhn 1961 (*Isis*) and van Fraassen 2008 secondarily. The author's name is from memory.
- R8. Chang, H. "Operationalism." SEP, revised 2019. https://plato.stanford.edu/entries/operationalism/ — VERIFIED. Also Chang, H. 2007, "The Myth of the Boiling Point" (web essay), https://www.sites.hps.cam.ac.uk/boiling/index.htm — VERIFIED.
- R9. Rheinberger, H.-J. 1994. "Experimental systems: historiality, narration, and deconstruction." *Science in Context* 7(1): 65–81. https://www.cambridge.org/core/journals/science-in-context/article/experimental-systems-historiality-narration-and-deconstruction/DE1F6600AE026B50F6AD5BB62E3A97B6 — VERIFIED (abstract).
- R10. Rheinberger, H.-J. 1997. *Toward a History of Epistemic Things*. Stanford UP (publisher from MEMORY; sources conflicted). Content VERIFIED-secondary via Weber, M., "Experiment in Biology," SEP, revised 2018, https://plato.stanford.edu/entries/biology-experiment/ (author name from memory).
- R11. Morange, M. 2022. *Berichte zur Wissenschaftsgeschichte* 45(3): 301–305. https://pmc.ncbi.nlm.nih.gov/articles/PMC9541519 — VERIFIED.
- R12. Baird, D. 1998. "Encapsulating Knowledge: The Direct Reading Spectrometer." *Techné/SPT* 3(3). https://scholar.lib.vt.edu/ejournals/SPT/v3n3/BAIRD.html — VERIFIED.
- R13. Baird, D. 2004. *Thing Knowledge*. U California Press. https://books.google.com/books?id=8eIbaERH26QC — VERIFIED (description and contents only).
- R14. Galison, P. 1997. *Image and Logic*. U Chicago Press. https://press.uchicago.edu/ucp/books/book/chicago/I/bo3710110.html — VERIFIED (description and contents). Galison, P. 1987, *How Experiments End*, U Chicago Press — VERIFIED-secondary via R2.
- R15. Collins, H. 1975. "The seven sexes…" *Sociology* 9: 205–224 — MEMORY.
- R16. Collins, H. 1985. *Changing Order*. Sage — MEMORY.
- R17. Feder, T. 2021. "Q&A: Harry Collins…" *Physics Today*. https://physicstoday.aip.org/news/q-a-harry-collins-on-acquiring-and-using-scientific-knowledge — VERIFIED.
- R18. Steinle, F. 1997. *Philosophy of Science* 64(S4): S65–S74. https://cambridge.org/core/journals/philosophy-of-science/article/entering-new-fields-exploratory-uses-of-experimentation/A1BF59B7198F4C380D3B5F1FAEFF9241 — VERIFIED (abstract).
- R19. Szilard, L. 1929. *Zeitschrift für Physik* 53: 840–856; English translation in *Behavioral Science* 9 (1964): 301–310. https://informationphilosopher.com/solutions/scientists/szilard/Szilard_Entropy_1964.pdf — VERIFIED.
- R20. Landauer, R. 1961. *IBM Journal of Research and Development* 5(3): 183–191. http://worrydream.com/refs/Landauer%20-%20Irreversibility%20and%20Heat%20Generation%20in%20the%20Computing%20Process.pdf — VERIFIED.
- R21. Bennett, C. H. 2003. *Studies in History and Philosophy of Modern Physics* 34: 501–510. https://arxiv.org/abs/physics/0210005 — VERIFIED. Earman & Norton 1998/99, "Exorcist XIV" — MEMORY.
- R22. Bérut, A. et al. 2012. *Nature* 483: 187–189. https://doi.org/10.1038/nature10872 — VERIFIED (via a mirror of the article).
- R23. Toyabe, S. et al. 2010. *Nature Physics* 6: 988–992. https://arxiv.org/abs/1009.5287 — VERIFIED (abstract).
- Also: Gelfert, A. 2011, "simulationist's regress," in Humphreys & Imbert (eds.), *Models, Simulations, and Representations*, Routledge — MEMORY (cited on Wikipedia).
---

## Survey: construction-continua

**Lens report: agents that manipulate and build inside continuous media and physics sandboxes**

Tags: VERIFIED means I opened the source and read the relevant part. PARTIAL means I saw only the abstract or a search excerpt. MEMORY means I did not open it.

**(1) Key works and what they actually show**

*Differentiable manipulation benchmarks*
- **Huang, Hu, Du, Zhou, Su, Tenenbaum, Gan (2021). "PlasticineLab." ICLR 2021. https://arxiv.org/abs/2104.03311. VERIFIED (full text).**
  - Setup: 10 tasks with 50 configurations, simulated with MLS-MPM in DiffTaichi. The agent is a set of rigid primitives the designers supplied (spheres, a rolling pin, chopsticks).
  - Results: Adam on soft-contact gradients, with 200 episodes, beat RL with 10⁴ episodes. Adam scored Move 0.90, RollingPin 0.93, Chopsticks 0.88 and Assembly 0.90.
  - Failures: it failed Pinch (0.08) and Table (0.01), which are multi-stage tasks. On TripleMove (0.35) it got stuck in local minima. With hard-contact gradients it collapsed (Move 0.05).
  - Authors' stated limit: gradients vanish whenever the tool detaches and reattaches.
  - Cost: about 14 ms forward and 36 ms forward plus backward per step (19 MPM substeps) on a GTX 1080 Ti.
- **Xian, Zhu, Xu, Tung, Torralba, Fragkiadaki, Gan (2023). "FluidLab." ICLR 2023. https://arxiv.org/abs/2303.02346. VERIFIED.**
  - Setup: 10 tasks on a 64³ MPM grid with about 100k particles, plus a 128³ gas grid. Runs in real time (60 FPS) on an RTX 3090. The agent is a 6-DoF rigid end-effector.
  - Results: plain differentiable physics without their tricks fails on fluid-solid coupling and fine control (Pouring 88 vs 603). The tricks are a soft contact model, a temporally expanding optimisation window and gradient sharing between particles.
  - RL (SAC, PPO) fails on Latte Art, Mixing and Ice Cream. On Transporting, though, PODS and SAC beat differentiable physics (2120 and 2051 vs 1471).
  - The authors call all tasks short-horizon with a single action mode; pour-then-stir is left to future work.
  - The walls in the multi-room air task are fixed by the designers. The agent never builds anything.
- **Lin, Wang, Olkin, Held (2020). "SoftGym." CoRL 2020. https://arxiv.org/abs/2011.07215. VERIFIED.**
  - Built on FleX position-based dynamics. 10⁶ steps take 6 hours of wall-clock time.
  - CEM with an oracle model solves most tasks. Image-based RL (CURL, DrQ, PlaNet) falls far short.
  - A policy given the full particle state does poorly on every task.
  - PlaNet cannot predict spilled water. A reduced state works only when it contains the task variables, including hidden ones such as the amount of water.
- **Hu, Anderson, Li, Sun, Carr, Ragan-Kelley, Durand (2020). "DiffTaichi." ICLR 2020. https://arxiv.org/abs/1910.00935. VERIFIED.**
  - 10 simulators. A 2-D MPM with 6.4k particles runs forward plus backward in 0.26 ms.
  - Differentiating collisions naively gives the wrong sign of gradient (+1 instead of −1). This needed a continuous time-of-impact fix.
  - Other gradient traps: flat objectives (billiards), "robot fell over" states with zero gradient, and 1/r singularities.
  - The authors' conclusion: differentiating a simulator "does not always yield useful gradients".
- **Bhatia, Jackson, Tian, Xu, Matusik (2021). "Evolution Gym." NeurIPS 2021. https://arxiv.org/abs/2201.09863. VERIFIED.**
  - 2-D mass-spring voxels, under 100 per robot. Robot and terrain are made of the same material.
  - More than 30 tasks. A genetic algorithm plus PPO did best overall. Each algorithm takes several to 20 hours per task on 80 CPUs.
  - Every algorithm fails the hardest tasks (Beam Slider, for example). Robots co-design their own bodies but never change the terrain.
- **Antonova, Yang, Jatavallabhula, Bohg (2022). arXiv 2207.00167. https://arxiv.org/abs/2207.00167. VERIFIED (abstract).** Loss landscapes for deformables and fluids are rugged, so they propose global search with Bayesian optimisation.

*An embodied agent inside a CA world (adjacent to this lens)*
- **Hamon, Etcheverry, Chan, Moulin-Frier, Oudeyer (2024; Science Advances 2025). "Discovering sensorimotor agency in cellular automata." https://arxiv.org/abs/2402.10236. VERIFIED (HTML).**
  - Obstacles live in a separate fixed channel, hand-engineered, with a large negative growth term.
  - The agents sense obstacles only through disturbances to their own structure; the authors call this "haptic".
  - Search found 261 robust agents out of 1600 parameter sets (16%). Random search found 20 out of 117k.
  - Stated limits: no energy or mass conservation; fast obstacles kill the agents.

*Sandboxes where people build*
- **Minecraft Wiki, "Redstone circuits." https://minecraft.wiki/w/Redstone_circuits. VERIFIED.** The components behave as logic parts: a torch is a NOT gate, a repeater is a diode and booster, pistons can act as memory. The wiki separates signal-processing circuits from mechanisms that act on the world, and documents calculators and basic computers.
- **Zhou, Tang, Zhang, …, Terzopoulos, Gao (2026). "Can Current Agents Close the Discovery-to-Application Gap? A Case Study in Minecraft" (SciCrafter). https://arxiv.org/abs/2604.24697. VERIFIED (abstract).**
  - Tasks: parameterised redstone lamp patterns, so solutions cannot be memorised.
  - GPT-5.2, Gemini-3-Pro and Claude-Opus-4.5 all plateau at about 26% success.
  - The authors split the loop into identifying knowledge gaps, experimental discovery, consolidation and application. Application is the largest gap.
  - This is the closest existing evaluation of "discover, then build".
- **The Powder Toy.**
  - Sources: Wikipedia, https://en.wikipedia.org/wiki/The_Powder_Toy (VERIFIED); Braun (2021), https://www.bryanbraun.com/2021/01/18/the-powder-toy/ (VERIFIED). The official wiki was blocked by bot protection, so its content is search excerpts only (PARTIAL).
  - Content: electronics work by drawing SPRK onto conductors. PSCN→NSCN conducts one way only, so it acts as a diode. Players build logic gates and a calculator. Player-built computers are reported via a Rock, Paper, Shotgun article that I did not open (MEMORY).
- **Noita.**
  - Sources: Purho, GDC 2019, "Exploring the Tech and Design of Noita", https://gdcvault.com/play/1025695 (session page VERIFIED, video not watched); 80.lv interview, 2019, https://80.lv/articles/noita-a-game-based-on-falling-sand-simulation/ (VERIFIED).
  - Content: a per-pixel CA split into 64×64 chunks with dirty rectangles and 4-pass checkerboard threading. Rigid bodies are made of pixels and are recomputed when destroyed. This is evidence about simulation technique (static matter costs almost nothing), not about players building apparatus.
- **Allen, Smith, Tenenbaum (2020). "Virtual Tools." PNAS 117:29302. https://arxiv.org/abs/1907.09620. VERIFIED.** "Tool use" here means placing one of three objects. Humans solve 81% of levels in about 4.5 attempts. A sample-simulate-update model matches humans; DQN is barely above chance.

*Real chemistry run inside built geometry*
- **Steinbock, Kettunen, Showalter (1996). "Chemical wave logic gates." J. Phys. Chem. 100:18970. https://www.chem.fsu.edu/~steinbck/papers/jpc96a.pdf. VERIFIED.**
  - BZ catalyst is ink-jet printed onto a membrane, and the printed geometry sets the logic.
  - Whether a gate works depends on channel width relative to the medium's critical nucleation size.
  - An electrode "door" (about 5 V) switches XNOR to OR, but needs about 2 minutes to recover.
  - Crucially, the catalyst-free regions are not no-flux. The model needed an extra decay term there; without it, bromous acid "accumulated to high concentrations".
- **Steinbock, Tóth, Showalter (1995). Science 267:868, maze solving. PARTIAL (abstract).**
- **Tóth & Showalter (1995). J. Chem. Phys. 103:2058, logic gates. MEMORY (bibliographic record only).**
- **Egbert, Gagnon, Perez-Mercader (2019). J. R. Soc. Interface 16:20190190. https://arxiv.org/abs/1908.11510. VERIFIED (abstract).** A uniform reaction-diffusion medium becomes a full adder purely by switching local external conditions in space and time, with no walls.
- **Microfluidics, all PARTIAL (abstracts via search):**
  - Whitesides (2006), Nature 442:368: channels tens of µm wide.
  - Thorsen, Maerkl, Quake (2002), Science 298:580: thousands of valves, a multiplexor, a 256-comparator chip, and a 1000-chamber memory with 3574 valves.
  - Fidalgo & Maerkl (2011), Lab Chip 11:1612: a valve array with 15 off-chip controls runs many functions with no hardware changes.
  - Beebe et al. (2000), Nature 404:588: hydrogel valves photopatterned in place that sense and actuate, with responses under 10 s.

*Numerical methods for adding walls to PDE worlds*
- **Kadoch, Kolomenskiy, Angot, Schneider (2012). J. Comput. Phys. 231:4365. VERIFIED.**
  - No-flux walls for scalars on a periodic Fourier pseudo-spectral grid: diffusivity becomes κ(1−χ)+ηχ, and obstacles may move.
  - Penalisation error is O(√η), with no time-step penalty.
  - The cost: convergence drops to O(N^-1/2) in 1-D and O(N^-3/4) in 2-D, and the scalar does not converge inside the solid.
  - For flow, they cite a velocity convergence of O(η^1/4) from Angot, Bruneau, Fabrie (1999), Numer. Math. 81:497 (PARTIAL).
- **Yu, Chen, Thornton (2012). Smoothed boundary method. MSMSE 20:075008. https://arxiv.org/abs/1107.5341. VERIFIED.**
  - Covers Neumann and Dirichlet conditions and a Cahn-Hilliard contact-angle condition.
  - Needs about 3 grid points across the wall interface, and the ψ→0 regularisation can make it unstable.
- **Diffuse-domain method.** Li, Lowengrub, Rätz, Voigt (2009), CMS 7:81 (PARTIAL). Lervåg & Lowengrub (2015), CMS 13:1473 (VERIFIED abstract): some boundary-condition approximations are only first-order accurate.
- **Jones et al. (1991). "Surface-directed spinodal decomposition." PRL 66:1326. PARTIAL.** Near a surface that one phase prefers, composition waves orient along the surface normal.

**(2) Feasibility**
- **Compute is not the blocker.** 3-D MPM with 100k particles runs in real time, and 2-D MPM takes under 1 ms per step. Our 2-D grids are cheaper still.
- **Control is the blocker.** Every benchmark success depended on three things:
  - full state plus a differentiable model, used for open-loop plans;
  - rigid tools supplied by the designers;
  - short tasks with one action mode.
- **Multi-stage tasks fail consistently.** Examples: PlasticineLab's Pinch and Table, FluidLab's pour-then-stir, Evolution Gym's hardest tasks. "Build an instrument, then experiment with it" is exactly that kind of task.
- **No continuum benchmark I found has an agent build its own tools.** Building happens only in designed voxel or block worlds (Minecraft, Powder Toy), mostly by humans. I found no example of a body living in the fields that constructs persistent structure in a continuum PDE world.
- **Required material properties:**
  - Persistence: a diffusing field cannot hold a wall. Construction needs an immobile or bistable substrate, like printed catalyst, polymerised hydrogel, a Minecraft block or Lenia's fixed channel.
  - Inertness: redstone and Powder Toy signals ride on inert solids.
  - Local, bounded manipulability.
  - Threshold elements: diodes, repeaters, critical nucleation size.
  - A few documented rules.
- **Can a generic wall material be added without changing the science? Not literally.**
  - In reaction-diffusion, a wall must gate reaction as well as flux, or species accumulate (Steinbock 1996).
  - In Cahn-Hilliard, walls impose wetting and surface-directed composition waves. Even a 90° contact angle is a choice.
  - In flow, no-slip walls create vorticity (MEMORY: standard fluid dynamics).
  - In active nematics, walls impose anchoring (MEMORY).
  - Penalisation lowers accuracy near walls and does not conserve the field content a wall displaces.
- **Sensing through one's own body works but is low-bandwidth.** The Lenia agents needed heavy search, and only 16% of candidates were robust.

**(3) Usefulness as an evaluation of scientific method**
- **For:**
  - SciCrafter shows that "discover, then build" in a designed material is discriminating (a 26% plateau for frontier models) and can be broken into separate capacities.
  - A built device can certify understanding. A BZ gate works only if the builder respects the medium's critical size.
  - Building also opens up the defining experiments the current apparatus cannot do: moats, local law changes, closed-loop tracking of moving targets.
- **Against:**
  - In PlasticineLab and FluidLab, scores were driven by optimiser engineering (soft contact, expanding horizons) more than by understanding. Embodiment risks measuring motor control.
  - The energy score needs a canonical apparatus. If agents build their own instruments, held-out tests still need a frozen referee.
  - Wall physics is specific to each world, so worlds stop being independent. This was already flagged as a cost.

**(4) Design lessons for reaction-diffusion and Cahn-Hilliard worlds**
1. **Make construction a separate, immobile mask channel χ.** Precedents: Lenia's fixed channel and Steinbock's printed catalyst. Give each field one fixed, documented wall rule:
   - Reaction-diffusion: diffusivity D(1−χ)+ηχ and reaction f(u)(1−χ), with an optional decay term inside the wall.
   - Cahn-Hilliard: mobility M(1−χ), and a declared neutral contact angle via the smoothed boundary method.
   - Vorticity: a Brinkman term χu/η.
2. **Offer two building primitives:** geometry (walls and moats) and local law change (excitability or catalyst patches, as in Egbert 2019). The second is how real reaction-diffusion chemists build instruments.
3. **Make χ persistent, local and metered.** Deposit it only at the body's location, rate-limit it, budget it, and make erasure cost something. Consider drawing wall material from a conserved field so construction has a cost.
4. **Validate per world:**
   - with χ=0 the world must be bit-identical to today's;
   - bulk-science checks must pass away from walls;
   - measure wall artefacts (wetting layer depth, vorticity generated at walls);
   - resolve at least 3 cells across each wall;
   - declare the artefacts as physics the agent may need to discover.
5. **Keep a frozen external referee apparatus for scoring.** Let self-built instruments serve the investigation only. Add construction challenges with SciCrafter-style parameterised targets, for example "build a gate or filter with property X".
6. **Stage it.** First let the agent place χ through an API while still disembodied, then add the body, so the value embodiment adds can be measured.
7. **Give closed-loop macro-actions.** The evidence says open-loop plans and long horizons fail.

**(5) Open questions**
- Can a blob that controls only its own internal balances move enough material to build anything? This has not been demonstrated anywhere I could find.
- How should instrument quality be scored separately from what the agent predicts?
- In 2-D grids of our size, do wall artefacts swamp the bulk science?
- How should field content that a new wall displaces be handled while keeping conservation?
- Will LLM agents actually iterate their methods? SciCrafter suggests that identifying knowledge gaps is the emerging bottleneck, and embodiment may make that worse.
- Thorsen 2002, Fidalgo and Maerkl 2011 and Steinbock 1995 need full-text checks; fetches were rate-limited or blocked.

Downloaded paper text for re-checking is in /tmp/claude-0/-home-user/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/pdfs/
---

## Survey: embedded-agency-theory

**Lens report: embedded agents, boundaries, and sensing through action (PhySim embodiment)**

Tag key: VERIFIED means I opened the source and read the relevant part. ABSTRACT means I saw only the abstract or a search listing. MEMORY means I did not open it.

**(1) Key works and what they actually show**

- **Demski & Garrabrant 2019, "Embedded Agency", arXiv:1902.09469.** https://arxiv.org/abs/1902.09469. VERIFIED (introduction).
  - Gives four complications for an agent inside its world: no well-defined I/O channels; smaller than the environment; can reason about and modify itself; made of the same parts as the environment.
  - From these it derives four subproblems: decision theory, embedded world-models, robust delegation, subsystem alignment.
  - It is a conceptual problem statement with no constructive results.
  - What matters for PhySim: our LLM's computation stays outside the world. An embodied PhySim agent is a dualistic agent driving an embedded avatar. Self-reference and naturalized induction mostly do not arise. What does arise is that the I/O channels are made of world stuff, so they depend on the world and can be destroyed.

- **Kenton, Kumar, Farquhar, Richens, MacDermott, Everitt, "Discovering Agents", arXiv 2022; Artificial Intelligence 322:103963 (2023).** https://arxiv.org/abs/2208.08345. VERIFIED (sections 1, 3 and 5; venue from DBLP).
  - Defines an agent as a system that "would adapt their policy if their actions influenced the world in a different way".
  - The discovery algorithm needs interventional data, including interventions on mechanisms, over a set of variables that is given in advance.
  - Section 5.1 says decision and utility labels are "frame-dependent" on the chosen variables. Section 5.2 admits the method does not say how to choose variables, and that coarse-graining "may have an impact on whether agents are discovered".
  - Under this definition a frozen policy is not an agent; the training process is.

- **Garrabrant, Herrmann, Lopez-Wild 2021, "Cartesian Frames", arXiv:2109.10996.** https://arxiv.org/abs/2109.10996. VERIFIED.
  - Formalizes the agent/environment split as a "frame" placed over a set of possible worlds. The same worlds admit many frames, so the boundary is a modelling choice.

- **Friston 2013, "Life as we know it", J R Soc Interface 10:20130475.** https://pmc.ncbi.nlm.nih.gov/articles/PMC3730701. VERIFIED.
  - Simulates a "primordial soup" of 128 subsystems.
  - The blanket was not found from the dynamics alone. It came from the coupling adjacency matrix over the last 256 s, using a spectral heuristic, with k=8 internal states chosen by the modeller.
  - Results:
    - internal states predicted some external motion (5 subsystems above a time-reversed null);
    - lesioning blanket subsystems destroyed the structure.

- **Kirchhoff, Parr, Palacios, Friston, Kiverstein 2018, "The Markov blankets of life", J R Soc Interface 15:20170792.** https://pmc.ncbi.nlm.nih.gov/articles/PMC5805980. VERIFIED.
  - Proposes nested "blankets of blankets", and says blankets need not coincide with the physical body.
  - Concedes that blankets also fit coupled pendulums, and adds "adaptive" active inference to rescue the idea of autonomy.
  - States outright that it has not shown nested blankets self-organize; it defers to simulations under review elsewhere.

- **Critiques of the blanket view:**
  - **Bruineberg, Dołęga, Dewhurst, Baltieri, "The Emperor's New Markov Blankets", BBS 45:e183 (2022).** https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/emperors-new-markov-blankets/715C589A73DDF861DCF8997271DE0B8C. ABSTRACT only; the body text was paywalled or blocked. "Pearl blankets" (an epistemic tool) are distinct from "Friston blankets" (a physical boundary). Moving from inference *with* a model to inference *within* one needs extra philosophical premises.
  - **Aguilera, Millidge, Tschantz, Buckley, Physics of Life Reviews 40:24–50 (2022).** https://arxiv.org/abs/2105.11203. ABSTRACT. Even in weakly coupled linear stochastic systems, the blanket condition holds only in a "very narrow range of parameters". Systems that satisfy it lack the perception–action asymmetry real organisms have.
  - **Biehl, Pollock, Kanai, Entropy 2021.** https://arxiv.org/abs/2001.06408. ABSTRACT. The various definitions of Markov blanket are not equivalent, and the original free energy lemma is false as stated (shown by counterexample).

- **O'Regan & Noë 2001, "A sensorimotor account of vision and visual consciousness", BBS 24:939–1031.** https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0140525X0149011X/resource/name/S0140525X01000115a.pdf. VERIFIED (abstract, sections 2 and 5.14).
  - Separates contingencies due to the apparatus (the sensor's own behaviour) from contingencies due to objects.
  - Tactile visual substitution evidence: blind users could not identify objects with a fixed camera. Identification only became possible when they moved the camera themselves.

- **Philipona, O'Regan, Nadal 2003, Neural Computation 15:2029–2049.** ABSTRACT, from a search listing. A simulated organism with arbitrary wiring can infer the dimension of physical space from sensorimotor dependencies alone.

- **Laflaquière, O'Regan, Argentieri, Gas, Terekhov 2015, Robotics and Autonomous Systems 71:49–59.** https://arxiv.org/abs/1810.01872. VERIFIED.
  - Shows that from sensorimotor invariants alone a simulated agent recovers the manifold of its own sensor's pose (position and orientation).
  - This needs a static environment, no noise, a known Jacobian (how motor commands move the sensor) for sampling, and exhaustive exploration.
  - The authors name these limits themselves.

- **Klyubin, Polani, Nehaniv 2005, "Empowerment: a universal agent-centric measure of control", IEEE CEC 2005.** https://uhra.herts.ac.uk/id/eprint/282. VERIFIED.
  - Defines empowerment as the channel capacity from action sequences to later sensor states.
  - Sensor layouts evolved for maximum 4-step empowerment are niche-specific: near a signal source they capture displacement, far away they capture bearing.

- **Salge, Glackin, Polani 2014, "Empowerment – an introduction", in Guided Self-Organization: Inception (Springer).** https://arxiv.org/abs/1310.1863. VERIFIED (sections 4.5 and 4.6).
  - Empowerment "depends on what the agent's sensors and actions are".
  - Cost grows exponentially with the horizon.
  - In deterministic floating-point simulations it is unbounded or "meaningless" unless a noise level is imposed.
  - Under a power constraint P, the empowerment landscape can invert as P changes.

- **Krakauer, Bertschinger, Olbrich, Flack, Ay 2020, "The information theory of individuality", Theory in Biosciences 139:209–223.** https://pmc.ncbi.nlm.nih.gov/articles/PMC7244620. VERIFIED.
  - Defines three quantities over a system/environment split:
    - organismal individuality A* = I(S'; S), how much the system's next state depends on its current state;
    - colonial individuality A = I(S'; S | E), the same after conditioning on the environment;
    - environmental determination nC = I(S'; E | S).
  - Gives no algorithm for finding the split. A and A* only grow with system size, so finding a boundary needs a size regularizer.
  - The only computed example is a toy with two binary units.

- **Kolchinsky & Wolpert 2018, "Semantic information, autonomous agency and non-equilibrium statistical physics", Interface Focus (venue from MEMORY).** https://arxiv.org/abs/1806.08053. VERIFIED.
  - The system/environment split and the viability function are "subjective choices of the scientist".
  - Choosing them automatically by maximizing semantic information is proposed but left for future work.

- **Biehl, Ikegami, Polani 2016, ALIFE 2016.** https://arxiv.org/abs/1605.05676. VERIFIED.
  - Defines integrated spatiotemporal patterns, so that agent membership can vary from one trajectory to another.
  - Tested only on a 4x4 Game of Life grid. Results were "inconclusive", and cost explodes as 2^(a²) for an a-by-a grid.

- **Hamon, Etcheverry, Chan, Moulin-Frier, Oudeyer, Science Advances 2025, "Discovering sensorimotor agency in cellular automata using diversity search" (arXiv:2402.10236).** https://pmc.ncbi.nlm.nih.gov/articles/PMC12577699/. VERIFIED.
  - Method: goal-exploration search plus gradient descent through 50 steps of multichannel Lenia, a continuous cellular automaton.
  - Found 486 stable moving solitons, against 30 for random search. 9 of 10 seeds produced sensorimotor agents.
  - Near-perfect survival with up to 48 obstacles, under asynchronous updates, and across many scales.
  - No central controller: obstacles are sensed only through body deformation, which the authors compare to haptic perception.
  - Caveats:
    - the obstacles were a hand-engineered channel;
    - no energy or mass conservation;
    - the agents cannot be steered, because behaviour is fixed by the rule.

- **Autopoiesis line:**
  - **Varela, Maturana, Uribe 1974, BioSystems 5:187–196.** MEMORY; bibliography confirmed by search.
  - **McMullin, SFI working paper 97-01-001, "Computational autopoiesis: the original algorithm".** ABSTRACT, search snippet only. Reports that a "crucial" interaction was missing from every published description of the 1974 model.
  - **Beer 2014, "The cognitive domain of a glider in the Game of Life", Artificial Life 20:183–206.** ABSTRACT. Splits perturbations into destructive and nondestructive ones, and maps the glider's response to each nondestructive one.
  - **McShaffrey, Agmon, Beer 2025, "Matters of Life and Death in Computational Cell Biology", arXiv:2511.07847.** https://arxiv.org/abs/2511.07847. VERIFIED.
    - The intrinsic viability limits of a Game of Life glider can be derived exactly, with a ring of off-cells acting as its membrane.
    - Extending this to reaction-diffusion protocells is open: "defining the continuous generalization processes" is the central challenge.
  - **Agmon, Gates, Churavy, Beer 2016, Artificial Life 22:153–171.** ABSTRACT. Maps networks of viable configurations under perturbation in a spatial concentration model.
  - **Barandiaran, Di Paolo, Rohde 2009, Adaptive Behavior 17:367–386.** ABSTRACT. Three conditions for agency: individuality, interactional asymmetry, normativity.

**(2) Feasibility**

- **A designer-free body or interface does not exist in this literature.** Every operational criterion takes as input some choice: a variable set (Kenton), a frame (Garrabrant), a partition plus viability function (Kolchinsky), a candidate split plus size regularizer (Krakauer), or a modeller-chosen adjacency window and k (Friston 2013).
- **Blankets are a poor fit for our worlds.** In diffusive PDE worlds all cells are coupled, which is exactly the regime where Aguilera finds blanket conditions fail.
- **Beer's intrinsic-boundary analysis is the strongest constructive approach, but it is discrete only.** Its authors say the continuum version is unsolved.
- **Embodied bodies that sense by deformation are feasible.** Hamon et al. show this in continuous cellular automata much like our worlds. But nobody has shown an emergent body that can be steered through an internal control, or one that builds tools.
- **Learning through self-perturbation has been shown only under narrow conditions.** Philipona and Laflaquière work in static, noise-free settings with exhaustive exploration. Our worlds are non-stationary and full of moving targets, which is the untested regime.
- **An embodied agent faces a new confound.** It must separate its body's own dynamics (apparatus contingencies) from world laws (object contingencies) before any science starts.

**(3) Usefulness as an evaluation of scientific method**

Gains:
- Kenton's criterion, adapting the policy when mechanisms change, is a clean test of agency that open-loop programs cannot pass by construction.
- The substitution evidence suggests closed-loop control is necessary for some kinds of perceptual learning, which supports the idea that embodiment tests something real.

Costs:
- **Interface strength varies by world.** Empowerment depends on sensors, actuators, horizon, noise and power, so the agent's control bandwidth will differ uncontrollably across worlds. Difficulty is not comparable between worlds.
- **Self-built instruments break frozen held-out scoring.** If the agent builds its own apparatus, there is no fixed "same apparatus" to score through.
- **Scores can get confounded.** If scores include predictions about the agent's own body, they will reward learning the body rather than the world.

**(4) Design lessons**

1. **Declare the cut; do not claim it is canonical.** Make the body a self-maintaining structure native to the world, such as a membrane protocell, and make the interface a narrow, declared set of internal mechanism parameters. This matches Kenton's mechanism nodes.
2. **Calibrate rather than canonicalize.** For each world, compute and report n-step empowerment of the interface, with the noise floor, horizon and power stated. Also report the body's A*, A and nC to certify it is an individual rather than driven by its environment. Do not use these as definitions.
3. **Use an embodied experimenter with a disembodied examiner.** Score predictions of world laws through a fixed external reference probe on frozen held-out cases. Never score through instruments the agent built.
4. **Add mechanism-change trials.** Change a law mid-episode and score whether the agent's experiments adapt appropriately.
5. **Handle the body as its own problem.** Either provide a body-calibration phase or report body learning separately. Otherwise the eval measures how well the agent learns its own sensor geometry.
6. **Make body death an explicit outcome with a stated cost.** The continuum version of intrinsic viability is open, so the death condition will have to be imposed.
7. **Document every hidden interaction rule.** McMullin's finding is that even the canonical autopoiesis model hid a crucial one.

**(5) Open questions**

- Can an agent steer an emergent body through internal balances without destroying it?
- Does any continuum world support construction of tools by bodies? Nothing in this lens shows it.
- How much of the world's law can be identified from body-local interventions? Only what lies downstream of the actuators and is visible to the body's sensors.
- Can empowerment be computed tractably for high-dimensional fields, for example with Salge's quasi-linear Gaussian approximation?
- Can embodied worlds that differ in interface strength still be compared on one scale?
---

## Adversarial critique

**Adversarial critique: should PhySim embody the agent and its apparatus?**

I spot-checked four sources with the built-in WebFetch only and no firecrawl:
- Hamon et al. 2025, *Sci. Adv.*, https://pmc.ncbi.nlm.nih.gov/articles/PMC12577699/ (VERIFIED)
- Cvjetko et al. 2026, CARL, https://arxiv.org/html/2608.26116v2 (VERIFIED)
- Gao et al. 2026, EmbodiedLab, https://arxiv.org/abs/2610.35385 (VERIFIED, abstract only)
- Alchemy, https://arxiv.org/abs/2102.02926 (abstract only; the PDF was too large to fetch)

All other evidence below is as the surveys report it.

## The case AGAINST

**(a) Embodiment moves the arbitrary choices; it does not remove them.** All five surveys reach this independently. An embodied PhySim needs at least these designer choices, each as arbitrary as the probe lattice:
- **Body identity.** Either a tagged channel (Biomaker; Hamon's obstacle channel) or a threshold on the fields. A threshold depends on the observer (Beer 2004; Biehl & Virgo), and so do the variable set (Kenton §5.2) and the frame (Garrabrant).
- **Actuators.** Which internal balances the agent controls, and at what spatial resolution. Goal-guided NCA fails when only 25–50% of cells get the goal, and Hamon's small, symmetric disks die.
- **Sensing operator.** Boundary flux, internal content, or the convolution input as in Agnosiophobia.
- **Fuel budget and death rule.** The fuel budget must be imposed so the body cannot act as a free Maxwell's demon. A death criterion must also be imposed, because continuum viability is unsolved (McShaffrey et al. 2025).
- **Wall rules for each field.** Contact angle, no-slip, anchoring and reaction gating. Steinbock 1996 shows that catalyst-free regions are not no-flux.

This is worse than today. Probe choices sit outside the dynamics; body choices are built into the PDE. The current complaint that "ablations change the whole world" becomes permanent: the world is never observed without the agent's body in it.

**(b) The score would mostly measure motor control.**
- EmbodiedLab: "most failures arise in interacting with the apparatus," and the best agent under native control succeeds less than half the time. That is with a rigid arm.
- CARL needed 10^6 transitions to steer solitons. It saw the full grid, added or removed 0.3 mass anywhere, and "generally cannot recover a disrupted pattern."
- In PlasticineLab and FluidLab, scores tracked optimiser tricks such as soft contact models.
- Construction in hide-and-seek needed more than 10^8 episodes.
- DiscoveryWorld agents score 44–64% on interaction unit tests and still fail discovery. Embodiment therefore adds a second bottleneck in series with inference. The control term would dominate differences between models, and it is skill specific to one world (how to steer a Marangoni rod), not general method.

**(c) Bodies in our worlds are dissipative structures, which works against them.** They exist only while fuel flows through them.
- Beer's degeneracy argument says a robust body must be large compared with the perturbations it meets. A large body is a coarse sensor and a large intervention: it eats fuel and alters local chemistry, which is Szilard's back-action. No source resolves this conflict between robustness and resolution.
- Native materials do not stay put. Cahn-Hilliard domains coarsen, vortices merge, and defects annihilate (standard physics, MEMORY). Building therefore needs an added, immobile wall channel χ, which is physics the world does not have natively.
- Three surveys independently found no example of a body building a lasting structure in any CA or continuum world.
- Internal-only steering worked only when the rule was trained together with the controller (goal-guided NCA). That is impossible here, because the world's rule is the hidden thing being studied.
- Surviving 1,000 steps does not predict surviving 10,000 (Biomaker).

**(d) An LLM agent is too slow to drive a body step by step.** An LLM turn takes seconds; a simulation step takes milliseconds or less. Steering at CARL's scale cannot happen one turn at a time. The only workable route is for the agent to write controller code that runs at simulation speed (Voyager; EmbodiedLab's skill tier). But then the "embodied agent" is a program that reads a local sensor API and writes an actuator API. That is a closed-loop program on a constrained probe, plus a fragile body. Code-level access also widens the room for exploits (Sims: leaks "will inevitably be discovered and exploited"; Biomaker sanitizes every action).

**(e) The score survives embodiment only by not being embodied.** All five surveys arrive at the same canonical score: predictions of world quantities under frozen held-out interventions, checked through a fixed referee instrument that is not embodied. Once scoring is separated from the investigation interface, any interface can be compared on it. It is the separation that is needed, not the body. Two problems remain:
- How strong the interface is will vary between worlds without control, because empowerment depends on sensors, horizon, noise and power (Salge et al.). Difficulty across worlds becomes even less comparable.
- Built instruments can be given a secondary score by how well their readings agree with the true field (Lin concordance, as in EvalResearchBench). Process scores can be gamed.

## The case FOR

- **Instruments co-evolve with theory.** Lab science stabilizes by adjusting apparatus and theory together (Hacking 1992; Pickering; Chang's epistemic iteration; Rheinberger's objects of study becoming tools). A fixed apparatus fixes which operational concepts the agent can form (Bridgman). It also rules out checking a result across physically different instruments, building a scale from instrument-to-instrument agreement, and calibrating against independent surrogate signals (Franklin).
- **The gap is real and new.** No benchmark scores the invention of instruments or method.
- **Simulation is where the experimenter's regress can be broken,** because ground truth exists.
- **Sensing through a body creates realistic confounds.** It brings back-action and forces the agent to separate the sensor's own behaviour from the object's (O'Regan & Noë). Planted artifacts could then test the judgement between real effect and artifact (Galison).
- **Built devices certify understanding.** A BZ logic gate works only if channel width respects the medium's critical nucleation size (Steinbock 1996). SciCrafter's "discover, then build" tasks separate frontier models, which plateau at about 26%.

The catch is that almost every one of these benefits comes from closed loop, construction primitives and referee scoring. Only "the instrument is made of world stuff and disturbs the world" strictly needs a body, and that is the part with no feasibility precedent.

## (f) Intermediate designs, ranked by benefit/cost

0. **Prerequisite: score separately from the investigation interface.** A referee checks frozen held-out interventions at points it chooses, or on full fields. Low cost, and it makes every later comparison possible.
1. **Closed-loop controller programs.** The agent submits code that maps readings to actions each step, with a fixed per-step compute budget and sanitized input/output. Cost is low: a sandbox. It tracks moving targets and allows adaptive designs (Denil; Deep Adaptive Design; CARL). Highest ratio.
2. **Local, conservation-respecting actions on the existing probes.** Actions are written in flux form: they move existing material or draw from an accounted reservoir, within a radius of the device, under a budget. Nearly free for each world. It removes the most unphysical intrusions, such as Gaussian injections into a conserved order parameter, if declared fields include one, or CARL-style creation of mass. Modest benefit at almost no cost.
3. **Placeable materials, set through the API by the disembodied agent.** Three kinds: a no-flux wall χ; an absorbing sink, because the lead's starvation moat needs absorption, not reflection; and local law-change patches (Egbert 2019). This has the largest absolute benefit. It unlocks moats, wells, channels and compartments, and it turns mechanism ablation into a local operation. Cost is medium to high:
   - a wall rule for each field;
   - artifacts such as wetting layers, vorticity made at walls, and anchoring;
   - penalisation error of O(√η) and slower convergence (Kadoch 2012);
   - at least 3 grid cells across each wall;
   - a check that χ=0 gives bit-identical runs.

   Good value for reaction-diffusion and Cahn-Hilliard worlds. Worse for flow and active-nematic worlds, where walls generate vorticity or impose anchoring.
4. **Instruments the agent defines in software.** Examples: flux through a declared contour, a frame that moves with a tracked object, calibration against standards the agent built. Low cost, but much of this can already be computed from dense readings.
5. **A mobile probe with motion limits.** Speed limits, continuous paths, local-only sensing. It adds partial observation but mostly adds a motor-control burden.
6. **A tethered, engineered body with internal-only control.** High cost. It would need a perturbation battery to pre-qualify the body, and the gain is unclear.
7. **A free native body that builds.** No precedent anywhere.

## Survey claims that look wrong or unsupported

- **Hamon can be steered.** embedded-agency says the agents "cannot be steered," and ai-discovery-envs says "nothing is built or steered" (it read only the abstract). Both are wrong. I verified that Hamon added attractive elements so a user could guide an agent, sometimes causing "death or explosion" or reproduction. alife-embodied reports this correctly.
- **Hamon's scale robustness is overstated.** embedded-agency says the agents survive "across many scales." I verified that "a scaling of 0.15 already leads to some death"; only up-scaling is fine.
- **Hamon's mass conservation is misdescribed.** construction-continua and embedded-agency call "no energy or mass conservation" a stated limit. The paper actually proposes mass conservation as a future constraint. The substance is right; the wording overstates it.
- **Alchemy is over-read.** ai-discovery-envs says "removing the motor problem did not help." Scores were VMPO 156 against a random heuristic at 146 and an ideal observer at 284, so both versions sit at the floor. A floor effect cannot show what control costs.
- **EmbodiedLab's attribution is biased.** Blaming each failure on its first decisive error favours early failures (acting and observing) and hides later knowledge failures. I verified only the abstract, not the 75–100% figure.
- **The Kenton claim is wrong.** embedded-agency says open-loop programs "cannot pass by construction." The LLM revises its programs between rounds, and by Kenton's own point that the training process is the agent, the iterating agent passes.
- **"Compute is not the blocker" is incomplete.** construction-continua counts simulation cost only. It ignores agent-side cost: 10^6 transitions for CARL and seconds per LLM decision.
- **CARL is not evidence for embodiment.** alife-embodied rightly calls its view god's-eye, but CARL is still cited as support for the lead's motivation. It acts anywhere and creates mass, so it is evidence for closed loop only.
- **The Flow-Lenia claim is setup-specific.** "Optimising ordinary Lenia for directed motion found only exploding patterns" conflicts with Hamon's 486 moving patterns in ordinary Lenia.
- **Two claims are inference, not evidence.** embedded-agency applies Aguilera's blanket result to diffusive PDE worlds without it being shown there. philosophy-instruments sets "no privileged readouts" as a requirement, but learning from one's own body has been shown only in static, noise-free settings with exhaustive exploration (Laflaquière; Philipona).

**Verdict:** Build tiers 0 to 3. Treat full embodiment as a research question, gated on two things: a per-world inventory of buildable, lasting structures, and a measured gain on the referee score from tier 3 over tier 1.
---

## Citation check

## Citation check: five literature surveys (built-in WebSearch and WebFetch only; no firecrawl)

**Method:** WebFetch could not read some PDFs. I saved those and extracted the text locally with `pdftotext`. I downloaded one PDF (hide-and-seek, which was too large for WebFetch) with curl. "Desc." in the table means whether the survey describes the source's result accurately.

| Source | Exists | Year / venue | Desc. | URL |
|---|---|---|---|---|
| Beer 2004, *Artif. Life* 10:309–326 | yes | yes | yes (2^24 perturbations, "informal explorations", "extremely limited", degeneracy) | cepa.info/fulltexts/1143.pdf |
| Beer 2014, *Artif. Life* 20(2):183–206 | yes | yes | unclear: the "six classes" claim was not checked (paywalled) | direct.mit.edu/artl/article/20/2/183/2768 |
| Beer, "Characterizing autopoiesis", *Artif. Life* 21(1):1–19 | yes | 2015 (Biehl and Virgo list it as 2014a) | n/a | — |
| Biehl & Virgo, glider frame of reference | yes | workshop abstract, after 2023 | yes | nichele.eu/ALIFE-DistributedGhost/7-Biehl.pdf |
| Hamon et al., *Sci. Adv.* 11(44):eadp0834 (2025) | yes | yes | yes in alife-embodied (all numbers match). **Wrong** in ai-discovery-envs and embedded-agency: see correction 1. "Across many scales" is overstated. | pmc.ncbi.nlm.nih.gov/articles/PMC12577699 ; arxiv.org/abs/2402.10236 |
| Plantec et al., Flow-Lenia | yes | ALIFE 2023 Best Paper confirmed (alife.org) | yes (exploding Lenia, walls with outward flow, 1024², 144 creatures, 200k steps, "take over") | arxiv.org/abs/2212.07906 |
| Mordvintsev et al., Particle Lenia (2022) | yes | yes | yes | google-research.github.io/self-organising-systems/particle-lenia |
| Randazzo & Mordvintsev, Biomaker CA | yes | arXiv 2023 | yes; exact quote is "most trivial models or initialization will undoubtedly fail" | arxiv.org/abs/2307.09320 |
| Sudhakaran et al., GoalNCA | yes | ICLR 2022 page exists; workshop not confirmed | yes (64² training, 192² test, 75% vs 25–50%) | arxiv.org/abs/2205.06806 |
| Cvjetko et al., autotelic RL short paper | yes | no venue on PDF | the claim is hedged in the source: "To the best of our knowledge…" | developmentalsystems.org/rl-for-ca/lba.pdf |
| Cvjetko et al., Artificial Experimentalist | yes | arXiv, June 2026; accepted ALIFE 2026 | yes. 10⁶ transitions is the steering agent only; the soliton-creation agent used 2×10⁶. | arxiv.org/abs/2608.26116 |
| Cool et al., Agnosiophobia | yes | under review, ALIFE 2026 | yes (3 of 4 creatures avoid blind regions; S1s dies; 3×3 occlusions). Reorientation passes through distorted states. | arxiv.org/abs/2605.30708 |
| Froese, Virgo, Ikegami, *Artif. Life* 20(1):55–76 | yes | yes (DOI 10.1162/ARTL_a_00096) | not checked in detail | arxiv.org/abs/1311.2531 |
| Sims 1994, SIGGRAPH | yes | yes | yes (both quotes, three sensor types) | karlsims.com/papers/siggraph94.pdf |
| Evolution Gym | yes | NeurIPS 2021 | yes (quote exact) | arxiv.org/abs/2201.09863 |
| Agmon, Gates, Churavy, Beer, *Artif. Life* 22(2):153–171 | yes | yes | yes (viability as average expected survival time) | doi 10.1162/artl_a_00196 |
| ScienceWorld | yes | EMNLP 2022 | the 1.5M vs 11B comparison is right; exact scores not checked | arxiv.org/abs/2203.07540 |
| DiscoveryWorld | yes | NeurIPS 2024 D&B | 14 actions, humans 66%/55%, unit tests 44–64% and GPT-4o judge are right. "18–23% Normal completion" is unclear; per-task range is 0–60%. | arxiv.org/abs/2406.06769 |
| BoxingGym | yes | arXiv | yes | arxiv.org/abs/2501.01540 |
| NewtonBench | yes | ICLR 2026 | 324 tasks and 87.5%→40.3% are right. **Noise result overstated:** see correction 5. | arxiv.org/abs/2510.07172 |
| PhysGym | yes | NeurIPS 2025 D&B confirmed | 97 problems and 100-experiment budget are right; see correction 7 | arxiv.org/abs/2507.15550 |
| Alchemy | yes | NeurIPS 2021 D&B | yes (156.2 / 140.2 / 145.7 / 284.4; symbolic 155.4) | arxiv.org/abs/2102.02926 |
| Denil et al. | yes | arXiv; ICLR 2017 is from memory | "theory-building not addressed" is not verified | arxiv.org/abs/1611.01843 |
| XLand; AdA | yes | arXiv | XLand percentages not verified | arxiv.org/abs/2107.12808 |
| Hide-and-seek | yes | arXiv; ICLR 2020 is from memory | yes (132.3M, 380M, "not drastic", "intractable", physics exploits) | arxiv.org/abs/1909.07528 |
| WorldTest / AutumnBench | yes | **ICML 2026**, not just arXiv | yes (517 humans; humans better in every environment; 12.5% vs under 7%) | arxiv.org/abs/2510.19788 |
| ARC-AGI-3 report | yes | 22 Apr 2026 | yes (64×64, upper-median human, squared score, 1.15 cap, 100% vs under 1%) | arcprize.org/media/ARC_AGI_3_Technical_Report.pdf |
| EmbodiedLab | yes | arXiv, 26 Oct 2026 | mostly yes; see correction 4 | arxiv.org/abs/2610.35385 |
| Voyager; MineDojo; Craftax; Kinetix | yes | Voyager arXiv; MineDojo NeurIPS 2022 Outstanding Paper; Craftax arXiv; Kinetix ICLR 2025 | yes (3.3×, 15.3×; 250×; 74 levels, Car-Ramp about 5%) | 2305.16291 ; 2206.08853 ; 2402.16801 ; 2410.23208 |
| Crafter | yes | ICLR 2022 | 50.5% and 10.0% not checked | arxiv.org/abs/2109.06780 |
| Melnikov 2018, *PNAS* 115(6):1221; Krenn 2025, *PRX* 15:021012; Wu & Tegmark, *PRE* 100:033311 | yes | yes | yes | 1706.00868 ; 2312.04258 ; 1810.10525 |
| EvalResearchBench | yes | arXiv | **"14 sealed" is wrong:** see correction 3 | arxiv.org/abs/2610.04184 |
| SciCrafter | yes | arXiv preprint | yes (about 26% plateau; application is the largest gap) | arxiv.org/abs/2604.24697 |
| PlasticineLab | yes | ICLR 2021 | yes (every score, 14.26/35.62 ms, 19 substeps) | arxiv.org/abs/2104.03311 |
| FluidLab | yes | ICLR 2023 not shown on arXiv | yes, except the gas grid is **128×9×128**, not 128³ | arxiv.org/abs/2303.02346 |
| DiffTaichi; SoftGym | yes | ICLR 2020; CoRL 2020 | DiffTaichi yes (6.4k particles, 0.26 ms, +1/−1 sign); SoftGym summary only | 1910.00935 ; 2011.07215 |
| Allen, Smith, Tenenbaum, Virtual Tools | yes | *PNAS* 2020 | 81% and 4.5 attempts not verified | arxiv.org/abs/1907.09620 |
| Steinbock, Kettunen, Showalter 1996, *JPC* 100:18970 | yes | yes | mostly yes; door direction wrong (see correction 9) | chem.fsu.edu/~steinbck/papers/jpc96a.pdf |
| Egbert et al. 2019; Kadoch et al. 2012, *JCP* 231:4365–4383 | yes | yes | yes (full adder; N^-3/4 in 2D; errors inside the solid) | 1908.11510 ; doi 10.1016/j.jcp.2012.01.036 |
| SEP "Experiment in Physics" (Franklin & Perovic, rev. 2023) | yes | yes | yes (microscopes, self-vindication, Pickering, "court", regress, Weber calibration) | plato.stanford.edu/entries/physics-experiment |
| Hacking 1983 | yes | yes | "spray" quote p. 24 is right. "Life independent of theory" is a paraphrase: his words are "Experimentation has a life of its own". | — |
| Chang, boiling-point essay | yes | yes | yes (over 3°C; 108–109°C) | sites.hps.cam.ac.uk/boiling |
| Rheinberger 1994, *Sci. Context* 7(1):65–81; Morange 2022, *Ber. Wiss.* 45(3):301–305 | yes | yes | Morange does **not** support the cancer or Nirenberg/poly-U claims; SEP biology-experiment does | — |
| Baird 1998, *Techné* 3(3) | yes | yes | yes (all three quotes exact) | scholar.lib.vt.edu/ejournals/SPT/v3n3/BAIRD.html |
| Bennett 2003, *SHPMP* 34:501–510; Toyabe 2010, *Nat. Phys.* 6:988 | yes | yes | yes ("let go of the handle"; concession to Earman and Norton) | physics/0210005 ; 1009.5287 |
| Demski & Garrabrant; Cartesian Frames | yes | arXiv | yes | 1902.09469 ; 2109.10996 |
| Kenton et al. | yes | *AIJ* 322:103963 (2023) confirmed | yes | arxiv.org/abs/2208.08345 |
| Friston 2013; Krakauer 2020, *Theory Biosci.* 139(2):209–223 | yes | yes | yes (128 subsystems, last 256 s, k=8, 5 of 82; two binary units, no boundary algorithm) | PMC3730701 ; PMC7244620 |
| Aguilera 2022; Biehl, Pollock, Kanai; Kolchinsky & Wolpert, *Interface Focus* 2018 | yes | yes | yes | 2105.11203 ; 2001.06408 ; 1806.08053 |
| Laflaquière 2015, *RAS* 71:49–59; Biehl, Ikegami, Polani, ALIFE 2016; Salge 2014; Klyubin 2005, CEC pp. 128–135 | yes | yes | summaries only: the 4×4 grid, "inconclusive" result and Klyubin's sensor details were not checked | 1810.01872 ; 1605.05676 ; 1310.1863 |
| McShaffrey, Agmon, Beer 2025 | yes | arXiv | the continuum-challenge quote is right; see correction 6 | arxiv.org/abs/2511.07847 |
| McMullin, SFI 97-01-001 | yes | yes | yes (a "crucial" interaction was missing) | santafe.edu working paper |

**Not opened:** O'Regan & Noë, Philipona, Bruineberg, Kirchhoff, Collins, Szilard, Landauer, Bérut, Yu/Chen/Thornton, Thorsen, Fidalgo, Beebe, Growing NCA and DAD. All are plausible from memory but unverified.

## The 10 most important corrections

1. **Hamon et al. agents *can* be steered.** ai-discovery-envs says "Nothing is built or steered" and embedded-agency says the agents "cannot be steered." Both are wrong. The paper shows a user steering agents by moving an added attractive element, a cyan disk found by random search plus human assessment. Any feasibility claim that no emergent body has ever been steered needs to say "by an internal control, or by a planner."
2. **Hamon robustness across scales is overstated** (embedded-agency). Down-scaling to 0.15 already causes some deaths.
3. **EvalResearchBench has 14 targets, of which only 8 are sealed.** The other 6 are visible during development. Its "4 of 8 beat the random sample on pairwise agreement" contradicts the paper's own Table 2, which shows 3 (Fable 5.1 scores 67.80, below 68.29). 7 of 8 beat the random sample on Score.
4. **EmbodiedLab's 10–27 point skill gains were measured only on three weaker agents** (DeepSeek, Kimi, GLM). T2 is a diagnostic tier, not part of the released protocol. Do not generalise "skills add 10–27 points" to strong agents.
5. **NewtonBench's noise result is smaller than stated.** It is a 12–16% *relative* drop, not 12–16 points, and it was measured on GPT-5-mini, not GPT-5.
6. **McShaffrey, Agmon, Beer 2025 does not derive glider viability limits itself.** It credits earlier Beer work, and its glider figure is a schematic. Cite Beer for the exact derivation.
7. **PhysGym: removing context alone costs about 13 points** (74.2% to 60.8%). The drop to about 32% comes from also stripping variable meaning and names (Level 4). So the recall-blocking lesson rests on variable names more than on context.
8. **Artificial Experimentalist: about 10⁶ transitions covers the steering agent only.** The soliton-creation agent needed 2×10⁶. The 64² grid is stated for training, not for the steering task.
9. **Steinbock 1996: the ~5 V electrode *closes* the door,** reducing local excitability and giving the XNOR gate. Opening the door gives OR[y, XNOR]. The survey reverses or blurs this direction.
10. **Smaller fixes for venues, quotes and attribution:**
    - WorldTest is ICML 2026, not just arXiv.
    - FluidLab's gas grid is 128×9×128, not 128³.
    - Hacking's wording is "Experimentation has a life of its own"; "has a life independent of theory" is a paraphrase.
    - The Zamecnik/cancer and Nirenberg/poly-U claims are supported by SEP "Experiment in Biology," not by Morange (R11).
    - "Characterizing autopoiesis" is dated 2015, not 2014.