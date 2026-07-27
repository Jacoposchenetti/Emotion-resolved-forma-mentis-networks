# Response to reviewers

We thank both reviewers and the editor. The revision adds four analyses, all on the existing
data, and corrects one claim that the new analyses showed to be an artifact. Reviewer comments
are in italics; our response and the change follow. Line references are to the revised
manuscript.

## Reviewer 1

**R1-1. *Italian VAD coverage is low (~11%); the "3 of 4 lexicons agree" claim is uneven across
languages. Restrict all lexicons to the common covered vocabulary and recompare.***

Done. We recomputed fear assortativity on the subgraph induced by words covered by every
lexicon that requires a lookup (493 nodes for students, 1,171 for researchers). The cohesion
survives: on the common subset the independent valence–arousal lexicon still gives significant
fear assortativity in both groups (students r = 0.278, 95% CI [0.167, 0.389]; researchers
r = 0.099 [0.050, 0.148]), and for researchers EmoAtlas (0.063) and NRC-direct (0.069) agree
while DepecheMood (0.016) remains the outlier. The agreement is therefore not a coverage
artifact. Added to §3.2 ("Restricting every lexicon to the vocabulary they jointly cover…").
**Status: ADDRESSED.**

**R1-2. *The proximity null does not preserve degree; fear nodes may differ in degree from
random words, so "farther than chance" could be a degree confound. Use a degree-matched null.***

This was the most consequential comment, and we are grateful for it. We replaced the uniform
permutation null with a degree-stratified one: fear-sized comparison sets are drawn to match
the fear set's degree distribution across deciles. The core result strengthens — no STEM
concept is closer to fear than chance in either group, and science, mathematics, and physics
(researchers) and science, statistics, *scuola*, *insegnante* (students) are significantly
farther. Critically, the new null also **overturned a claim in our first submission**: the
appearance that only experts distance science from fear was an artifact of the uniform null.
Under the degree-matched null, both groups distance hard-science concepts from fear. We have
corrected the abstract, §3.4, §4, and Figure 4 accordingly, and we state the correction
explicitly in §3.4. **Status: ADDRESSED (and a prior claim corrected).**

**R1-3. *The central claim is a null; even with the MDE this is "not detected," not "absent."
Reframe with equivalence testing.***

Done. We bootstrapped each concept's proximity and report its 90% interval against the
detectable-effect threshold set by the injection control. For the hard-science concepts the
interval lies below that threshold (mathematics [−1.2, +1.1] in students, [−2.8, −1.1] in
researchers), which supports equivalence to no fear-embedding rather than a mere failure to
reject. Added to §2.5 and §3.4. **Status: ADDRESSED.**

**R1 minor — Louvain stability.** Added: modularity is 0.52 (students) and 0.58 (researchers),
varying by < 0.003 across 50 seeds, and the top fear-module's fear fraction is stable
(0.25 ± 0.05; 0.20 ± 0.05). §2.5, §3.2. **ADDRESSED.**

**R1 minor — multiple comparisons.** The 22 concept-level proximity tests now carry a
Benjamini-Hochberg correction (q = 0.05); the seven significant concepts, all in the
"farther-than-fear" direction, survive it. §2.5, §3.4. **ADDRESSED.**

**R1 minor — assortativity estimator named.** The emotion-assortativity estimator is stated as
Newman's (2003) numeric assortativity for a binary attribute (§2.4, unchanged, now cross-linked
to the estimator used throughout). **ADDRESSED.**

## Reviewer 2

**R2-1. *N = 2 networks; every group-level claim rests on one network per group differing in
language and population. Soften generalisation; note a multi-cohort replication target.***

Agreed. We added an explicit scope statement to the Limitations: the design rests on two
networks, so group-level claims are case-study strength pending a multi-cohort design, and we
name the recent larger STEM forma mentis datasets (including LLM digital twins) as the
replication target. This is reinforced by R1-2: with the group contrast now shown to be
null-model-dependent, the paper's load-bearing claim is the within-both-groups dissociation,
not a between-group difference. **Status: ADDRESSED.**

**R2-2. *"Fear" is a lexical label, never anchored to a math-anxiety instrument; avoid slippage
between network-fear and measured anxiety in §4.***

Agreed. We added a sentence in §4 stating plainly that network "fear" is a lexical property of
a concept's associates, not measured anxiety, and that we keep the two distinct throughout; we
also tightened the §4 wording the reviewer flagged. **Status: ADDRESSED.**

**R2 minor — abstract alignment.** The English and Italian abstracts were re-aligned after the
degree-null revision. **ADDRESSED.** A supplementary bridge-word table is a reasonable addition
we are happy to include if the editor prefers; the bridge words are currently reported inline
in §3.5.

## Summary of changes

- New degree-stratified proximity null (§2.5, §3.4, Figure 4); corrected the experts-only
  distancing claim throughout (abstract EN/IT, §1, §3.4, §4).
- Common-vocabulary lexicon re-test (§3.2).
- Equivalence (TOST-style) framing of the proximity null (§2.5, §3.4).
- Louvain stability and Benjamini-Hochberg correction (§2.5, §3.2, §3.4).
- Scope and construct-validity caveats (Limitations, §4).

No new data were collected. All additions are reproducible from the released
`revision_analyses.py`.
