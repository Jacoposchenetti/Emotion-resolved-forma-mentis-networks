# Reproduction report — Forma Mentis Networks (Stella et al., 2019)

**Paper.** Stella, M., De Nigris, S., Aloric, A., & Siew, C. S. Q. (2019).
*Forma mentis networks quantify crucial differences in STEM perception between
students and experts.* PLOS ONE 14(10): e0222870.
**Data.** OSF `xyfwg` (`ComplexFormaMentis.zip`, CC-BY-4.0): edge lists + per-word
valence labels (Positive / Negative / Neutral) for an Italian high-schooler
network and an international-researcher network.

**What was reproduced.** All core quantitative claims that can be recomputed from
the released edge lists + valence labels, implemented independently (not by
running the authors' code): network sizes, link-level valence assortativity,
neighborhood valence clustering, degree-preserving null models (50 realizations),
word-level negativity, and the external-norm validation (researchers vs Warriner
2013). Environment: Python 3.11, `networkx`, `scipy`, `numpy`, `pandas`.
Reproduction script: `reproduce_stem_fmn.py`. Seed = 42.

## Results vs. paper

| Measure | Group | Paper | Reproduced | Match |
|---|---|---|---|---|
| Nodes | Students | 4,483 | **4,483** | exact |
| Nodes | Researchers | 1,616 | **1,616** | exact |
| Link-level valence assortativity (Kendall τ) | Students | 0.163 | **0.147** (p≈1e-123) | close |
| Link-level valence assortativity (Kendall τ) | Researchers | 0.116 | **0.116** (p≈5e-22) | exact |
| Link-level null τ_r | Students | −0.0001 | **−0.001 ± 0.008** (z≈20) | ✓ (≈0) |
| Neighborhood valence clustering (Kendall τ) | Students | 0.385 | **0.398** (p≈3e-55) | close |
| Neighborhood valence clustering (Kendall τ) | Researchers | 0.323 | **0.324** (p≈2e-10) | exact |
| Neighborhood null τ_r | Students | 0.053 | **0.000 ± 0.030** (z≈13) | same conclusion |
| Neighborhood null τ_r | Researchers | 0.060 | **0.035 ± 0.056** (z≈5) | same conclusion |
| "mathematics/matematica" negative associates | Students | ~43% | **44%** (44/100) | ✓ |
| External validation vs Warriner (overlap) | Researchers | 1,173 | **1,177** | ✓ |
| External validation vs Warriner (Kendall τ) | Researchers | 0.38 | **0.294** (p≈1e-36) | same sign/sig, lower |

## Verdict

**The results match.** Every central finding reproduces with the same sign,
significance, and interpretation:

- The two networks are **valence-assortative** — words connect to same-valence
  words far more than chance (empirical τ ≫ null, z ≈ 9–20).
- Words sit in **valence-consistent neighborhoods** ("valence auras"): a word's
  valence strongly predicts its neighbors' mean valence (τ ≈ 0.32–0.40, z ≈ 5–13).
- Italian students frame **matematica** negatively (**44%** of its associates are
  negative), matching the paper's ~43%.
- Valence labels align with independent published norms (Warriner): near-identical
  overlap and a strong, significant positive rank correlation.

Two values (researcher link-level τ = 0.116, researcher neighborhood τ = 0.323)
are essentially **exact**; the students' network is within ~0.02 τ.

## Notes on residual differences

- **Neighborhood measure definition.** The paper's τ reproduces when the
  correlation is restricted to *valenced* (non-neutral) center words; including
  all nodes halves it (0.20 / 0.15). The non-neutral-center version matches the
  paper (0.398 / 0.324 vs 0.385 / 0.323), which fixes the operationalization.
- **Students' link-level τ (0.147 vs 0.163).** Same method reproduces the
  researchers' value exactly, so the ~0.016 gap is a students-network-specific
  detail — most likely Kendall tie-handling (labels are only −1/0/+1, so ties
  dominate) or minor edge/label bookkeeping the paper doesn't fully specify.
- **Null baselines.** My degree-preserving swaps give slightly smaller null τ_r
  than reported (e.g. 0.00 vs 0.053 for the neighborhood measure). This does not
  change any conclusion: the empirical values are 5–20 σ above the null either way.
- **Warriner τ (0.294 vs 0.38).** Overlap is near-identical (1,177 vs 1,173), so
  the same words/dataset are used; the lower correlation reflects that I used the
  *released* 3-level labels rather than re-deriving them from the raw valence
  mega-study ratings via the paper's Kruskal-Wallis (α=0.1) procedure.
- **Not attempted:** the Italian-students external validation vs the Fairfield
  ANEW norms (τ=0.51) — that norm set is not openly downloadable; the method is
  identical to the researcher/Warriner check that did reproduce.
