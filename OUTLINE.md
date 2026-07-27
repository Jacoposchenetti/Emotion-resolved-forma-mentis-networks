# Paper Outline + Evidence Map (ARS `outline-only`)

**Working title:** *Emotion-resolved forma mentis networks dissociate valence from
affective structure in STEM perception*

---

## Phase 0 — Paper Configuration Record

| Field | Value |
|---|---|
| Paper type | Empirical research article (IMRaD), secondary analysis of open data |
| Discipline | Cognitive science / cognitive network science / NLP |
| Target venues | *Cognitive Science*; fallback *Scientific Reports* / *PLOS ONE* (open-data fit) |
| Citation style | APA 7.0 |
| Length target | 5,000–7,000 words (main text), ~4 figures, 1–2 tables |
| Data availability | Reuses OSF `xyfwg` (Stella et al., 2019, CC-BY 4.0); Warriner et al. (2013) norms; all reproduction/extension code released |
| Ethics | Secondary analysis of de-identified public data; no new human subjects |
| Contribution class | (i) independent reproduction + (ii) original emotion-resolved extension |

**One-sentence thesis.** Re-analysing the Stella et al. (2019) STEM free-association
networks with Plutchik's eight emotions (via EmoAtlas) shows that the students-vs-experts
difference is carried specifically by a **more cohesive fear structure** in students,
yet the core STEM concepts are **not** wired into that fear system — STEM negativity is
lexical/valence-level (difficulty vocabulary), not affective-structural.

---

## Phase 2 — Structure (IMRaD) + word budget

### 1. Introduction (~900 w)
- 1.1 Attitudes/anxiety shape STEM engagement; mental representations matter (math-anxiety lit).
- 1.2 Cognitive network science + forma mentis networks as a way to read mindsets from free associations (Stella et al. 2019; cognitive-network reviews).
- 1.3 Gap: prior forma mentis STEM work reduced affect to **3-level valence**; valence conflates distinct discrete emotions and cannot separate "negatively evaluated" from "affectively fearful."
- 1.4 This study: (a) reproduce the 2019 valence findings; (b) re-resolve affect into 8 Plutchik emotions; (c) test whether STEM concepts are structurally embedded in the affective (fear) subnetwork via spreading activation.
- 1.5 Contributions bullet list + roadmap.

### 2. Methods (~1,300 w)
- 2.1 **Data**: OSF `xyfwg` — students (Italian high-schoolers) and researchers (intl. experts) free-association networks; N nodes, edge lists; released valence labels. External norms: Warriner et al. (2013).
- 2.2 **Reproduction procedures**: link-level valence assortativity (symmetrised Kendall τ over edges); neighbourhood valence clustering (valenced center words, Kendall τ node-valence vs mean-neighbour-valence); degree-preserving null (double-edge-swap, 50×); word-level negativity share.
- 2.3 **Emotion labelling**: EmoAtlas Plutchik lexicon (IT for students / EN for researchers), 8 binary emotion attributes per node.
- 2.4 **Emotion-resolved measures**: per-emotion prevalence; per-emotion assortativity (numeric endpoint-indicator correlation) with 500-shuffle null (z) and 500× bootstrap 95% CI.
- 2.5 **Mesoscale**: Louvain community detection; per-community fear enrichment.
- 2.6 **Spreading activation**: personalised PageRank (α=0.85) seeded on each STEM concept; fear-mass = stationary mass on fear nodes; **fear-label-permutation null (1,000×)** holding the seed fixed → z, p. Rationale: controls for hub centrality.
- 2.7 **Bridge extraction**: first intermediate nodes on shortest paths from STEM concepts to fear words ≤2 hops.
- 2.8 Reproducibility: Python/networkx/scipy/EmoAtlas versions, seeds, released scripts.

### 3. Results (~1,700 w)
- 3.1 **Reproduction holds** (Table 1): node counts exact; researcher valence assortativity and neighbourhood clustering ≈ exact; students within ~0.02 τ; matematica ~44% negative ≈ paper's 43%.
- 3.2 **Emotion prevalence** (Fig 1): trust dominates both; students carry more negative-emotion words (descriptive; language-confounded).
- 3.3 **Emotion-specific assortativity** (Fig 2): all emotions cluster > null; **fear uniquely separates the groups** — students 0.129 [0.105,0.157] vs experts 0.052 [0.007,0.098], non-overlapping CIs.
- 3.4 **Fear modules** (Table 2): Louvain isolates thematic fear communities (existential-danger, health/death, mental-chaos in students; risk, disease/death in experts).
- 3.5 **Null result — STEM concepts not affect-wired** (Fig 3): spreading-activation fear-mass from matematica/fisica/chimica is n.s. vs label-permutation null (z≈0). Concept-level Plutchik auras also mostly n.s.
- 3.6 **Bridges are difficulty/technical terms** (descriptive): matematica→discussione/limite/disturbo; chimica→farmaco/gas/forza; physics→friction/force/dynamics.

### 4. Discussion (~1,400 w)
- 4.1 **Valence ≠ affective structure.** Core theoretical claim: STEM negativity in these data is an evaluative/valence property mediated by difficulty vocabulary, not embedding into the fear subnetwork.
- 4.2 Fear cohesion as a candidate signature of the anxious mindset; students' fear is more organised than experts'.
- 4.3 Implications for interpretation of prior valence-only forma mentis results (a single assortativity number hides emotion-specific structure).
- 4.4 Educational reading (cautious): difficulty "bridge" words as levers; but no causal claim.
- 4.5 Methodological contribution: emotion-resolved forma mentis + spreading-activation test as a reusable protocol.

### 5. Limitations (~500 w)
- EmoAtlas lexicalises epistemic terms as *trust* (WordNet) → concept-level trust auras partly lexicon artefact.
- Cross-language prevalence comparison confounded (IT vs EN lexicon density) — hence reliance on within-network assortativity for group inference.
- Free-association data are cross-sectional, descriptive; no causal/psychological inference.
- Single external validation (Warriner, researchers only); Italian norm validation (Fairfield) not openly available.
- Binary emotion labels ignore intensity; alternative lexicons (NRC/FEEL-IT) untested.

### 6. Conclusion (~250 w)
Restate dissociation; fear-cohesion result; call for emotion-resolved (not valence-only) mindset analyses.

### Back matter
Data & code availability; AI-usage disclosure; author contributions (CRediT); COI; funding; ethics.

---

## Evidence Map (claim → evidence → artifact)

| # | Claim in paper | Statistic / value | Source artifact |
|---|---|---|---|
| E1 | Reproduction: network sizes exact | Students 4,483; Researchers 1,616 nodes | `reproduce_stem_fmn.py`; `REPORT.md` |
| E2 | Reproduction: valence assortativity | Researchers τ=0.116 (≈paper); Students τ=0.147 (paper 0.163) | `reproduce_stem_fmn.py` (B) |
| E3 | Reproduction: neighbourhood clustering | Researchers τ=0.324 (paper 0.323); Students τ=0.398 (0.385) | `reproduce_stem_fmn.py` (C) |
| E4 | Reproduction: null ≈ 0, effect ≫ null | z ≈ 9–20 | `reproduce_stem_fmn.py` (D) |
| E5 | matematica negativity | 44% negative associates (paper ~43%) | `reproduce_stem_fmn.py` (E) |
| E6 | External validation | Warriner overlap 1,177 (paper 1,173), τ=0.294 | Warriner check |
| E7 | Emotion prevalence | trust ~9% both; students higher on fear/anger/sadness/disgust | `emotion_resolved_fmn.py`; `prevalence_compare.png` |
| E8 | Emotion-specific assortativity + null | all >null; fear students z=13.7 vs experts z=3.0 | `emotion_resolved_fmn.py` [2] |
| E9 | Fear cohesion group difference (headline) | fear 0.129 [0.105,0.157] vs 0.052 [0.007,0.098], CIs disjoint | `fear_module_analysis.py` [3b]; `assortativity_CI.png` |
| E10 | Fear modules (Louvain) | comm. with 20–23% fear; thematic labels | `fear_module_analysis.py` [1a] |
| E11 | Null result: STEM not affect-wired | spreading-activation fear-mass z≈0, n.s. | `fear_module_analysis.py` [1b]; (Fig 3 to render) |
| E12 | Concept auras mostly n.s.; math trust+ (lexicon caveat) | z-heatmap | `aura_heatmap_italian.png` |
| E13 | Bridges are difficulty/technical terms | ranked gateway lists | `fear_module_analysis.py` [2] |
| E14 | Prevalence group diff weak + confounded | only anger p=0.013; language caveat | `fear_module_analysis.py` [3a] |

**Figures to finalise:** Fig 1 prevalence (done), Fig 2 assortativity CI (done), Fig 3 spreading-activation null (to render: fear-mass z per concept vs null band), Fig 4 fear-module network snapshot (optional, EmoAtlas draw). Table 1 reproduction; Table 2 fear modules.

---

## References (IRON RULE: no fabricated citations)

**Confirmed (used/verified this project):**
- Stella, M., De Nigris, S., Aloric, A., & Siew, C. S. Q. (2019). Forma mentis networks quantify crucial differences in STEM perception between students and experts. *PLOS ONE, 14*(10), e0222870.
- Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. *Behavior Research Methods, 45*, 1191–1207.

**High-confidence, VERIFY exact metadata before submission (do not cite until checked):**
- Plutchik, R. (1980). *Emotion: A psychoevolutionary synthesis.*
- Blondel, V. D., et al. (2008). Fast unfolding of communities in large networks (Louvain). *J. Stat. Mech.*
- Newman, M. E. J. (2003). Mixing patterns / assortativity in networks. *Phys. Rev. E.*
- Siew, C. S. Q., Wulff, D. U., Beckage, N. M., & Kenett, Y. N. (2019). Cognitive network science: a review. *Complexity.*
- De Deyne, S., et al. (2019). The Small World of Words English word-association norms. *Behavior Research Methods.*
- EmoAtlas methodological paper (Stella and colleagues) — **verify exact author list, title, venue, year.**
- A math-anxiety anchor (e.g., Ashcraft, 2002, *Current Directions in Psychological Science*) — verify.
- Fairfield et al. Italian affective norms (for future IT external validation) — verify.

> Action item before drafting: run `/ars-citation-check` to resolve DOIs and confirm the "verify" block; drop any that cannot be confirmed.

---

## Reviewer-anticipation notes (from Phase-3 argument stress test)
- *"Is the null result just low power?"* → report bridge counts + that hubs DO reach fear (mass is high) but not more than label-permuted null; power addressed by 1,000 permutations and consistent direction.
- *"Trust auras are lexicon artefacts."* → pre-empt in Limitations; report result with explicit WordNet caveat; robustness check with an alternative lexicon (NRC) recommended.
- *"Cross-language comparison invalid."* → we do NOT infer from prevalence; group inference rests on within-network assortativity CIs.
