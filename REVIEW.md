# Simulated peer review — *Valence without fear* (ARS reviewer, full mode)

Manuscript: "Valence without fear: emotion-resolved forma mentis networks show that STEM
negativity is evaluative, not affectively wired."
Panel: two referees + handling editor. Rubric (weights): Originality 20%, Methodological
Rigor 25%, Evidence Sufficiency 25%, Argument Coherence 15%, Writing Quality 15%.

---

## Reviewer 1 (cognitive network science)

**Summary.** A secondary analysis that reproduces Stella et al. (2019) and extends it by
resolving valence into Plutchik emotions and adding a structural proximity test. The paper's
distinctive move is self-correction: it discards its own underpowered statistic and a
non-robust group difference. I find the core dissociation credible and the honesty unusual
and welcome. Several methodological points need addressing before I would endorse.

**Major.**
1. **Italian VAD coverage.** The independent confirmation of student fear cohesion (r=0.065)
   rests on the valence–arousal quadrant, but the Italian VAD norms cover only ~11% of
   student nodes (506/4,483; 171 fear-like). The assortativity is then computed on a sparse
   labelling. Report how many *edges* have both endpoints covered, and show the result is not
   an artifact of coverage (e.g., restrict all four lexicons to the common covered vocabulary
   and recompare). As it stands the "3 of 4 lexicons agree" claim is uneven across languages.
2. **Proximity null does not preserve degree.** The decay-proximity permutation samples random
   node sets of equal size, but fear nodes may differ systematically in degree from random
   words. Re-run the null with a degree-matched resample (or a configuration model) so the
   "farther than chance" result in experts cannot be a degree confound.
3. **Absence of evidence.** The central claim is a null (STEM not close to fear). Even with the
   injection MDE (~10–30% of degree), this is "we could not detect embedding above a moderate
   threshold," not "there is none." Please reframe with equivalence testing (e.g., TOST against
   the MDE) so the claim matches what the data support.

**Minor.**
- Louvain is stochastic; report modularity, resolution sensitivity, and whether fear modules
  are stable across seeds.
- Multiple comparisons: 8 emotions × 12 concepts × 2 groups. State the correction (or that
  results are reported descriptively) for the concept-level z-scores.
- The emotion-assortativity estimator (symmetrised Pearson on a 0/1 indicator) should be named
  and, ideally, cross-checked against `attribute_assortativity_coefficient`.

**Scores.** Originality 4/5 · Rigor 3/5 · Evidence 3/5 · Coherence 4/5 · Writing 5/5.

---

## Reviewer 2 (educational / math-anxiety)

**Summary.** The dissociation between evaluative negativity and affective wiring is a genuinely
useful conceptual contribution for the math-anxiety literature, which too often equates
"negative associations" with "anxiety." The difficulty-bridge vocabulary is a nice, actionable
observation. My concerns are about scope and interpretation, not analysis.

**Major.**
1. **N = 2 networks.** Every group-level claim rests on one student network and one expert
   network, differing in language *and* population. "Experts distance STEM from fear" is a
   single-network observation. Soften generalisation throughout, and frame as a case study
   that a multi-cohort design should test. The recent larger STEM forma mentis datasets (incl.
   LLM digital twins) would be an obvious replication target — cite as future work.
2. **Construct validity of "fear."** The paper leans on lexicon fear labels but never anchors
   them to a math-anxiety instrument. State explicitly that network "fear" is a lexical
   property of associates, not measured anxiety, and avoid slippage between the two in the
   Discussion (mostly handled, but §4 para 3 drifts).

**Minor.**
- The Italian abstract is strong; ensure the English and Italian abstracts stay aligned after
  any revision.
- Consider a supplementary table of the difficulty-bridge words with frequencies.

**Scores.** Originality 4/5 · Rigor 4/5 · Evidence 3/5 · Coherence 4/5 · Writing 4/5.

---

## Handling editor — decision

**Recommendation: Major Revision** (both referees positive on originality and writing; shared
concerns on evidence strength and generalisation — all addressable without new data collection).

Weighted panel score ≈ **3.6 / 5**. The paper's transparency (reporting a failed positive
control and a non-robust result) is a strength, not a liability, and should be preserved.

**Required for acceptance:**
1. Degree-preserving null for the proximity test (R1-2). *[analysis, ~1 day]*
2. Common-vocabulary re-analysis of the four lexicons to defend the cross-lexicon claim under
   uneven coverage (R1-1). *[analysis]*
3. Equivalence-testing framing of the null (R1-3). *[reframing + small analysis]*
4. Explicit scope limits: N=2, language confound, network-fear ≠ measured anxiety (R2-1, R2-2).
   *[writing]*
5. Louvain stability + multiple-comparison statement (R1 minor). *[analysis + writing]*

**Optional but recommended:** replication target in a larger/multi-cohort STEM dataset (future
work); supplementary bridge-word table.

---

## Author-side triage (which are quick wins)

| # | Comment | Effort | In current data? |
|---|---|---|---|
| R1-2 degree-preserving null | Medium | yes — re-run proximity with configuration-model null |
| R1-1 common-vocabulary lexicon re-test | Medium | yes — intersect coverage, recompute Table 1 |
| R1-3 TOST equivalence framing | Low–Med | yes — bound against MDE |
| R2-1 soften N=2 generalisation | Low | writing only |
| R2-2 fear≠anxiety caveat | Low | writing (tighten §4) |
| R1 minor: Louvain stability, MCC | Low–Med | yes |

None require new data. Items R2-1, R2-2 and the abstract-alignment are pure writing and can be
folded into the humanization pass; R1-1/2/3 and Louvain stability are the substantive revision.
