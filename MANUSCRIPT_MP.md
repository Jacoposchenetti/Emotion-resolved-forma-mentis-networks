# When is a concept "near" an emotion? A reproduction and robustness audit of emotional forma mentis networks of STEM perception

Jacopo Schenetti

*Center for Mind/Brain Sciences (CIMeC), University of Trento, Rovereto, Italy.*
Correspondence: jschenetti@gmail.com

*Submitted to Meta-Psychology. Peer review is open; the editorial process and contact are at https://open.lnu.se/index.php/metapsychology. Preprint and all code/data: https://github.com/Jacoposchenetti/Emotion-resolved-forma-mentis-networks*

## Abstract

Forma mentis (free-association) networks are widely used to read how learners feel about
science and mathematics, and a well-known study (Stella, De Nigris, Aloric & Siew, 2019) found
that students frame mathematics far more negatively than experts do. That study, and much of the
cognitive-network programme built around it, encodes affect either as valence or, more recently,
as emotional profiles from a single lexicon. We (i) reproduce the valence-level results of Stella
et al. (2019) from the open data, and (ii) stress-test the natural next step of resolving affect
into discrete emotions and asking whether STEM concepts are structurally *close* to fear. The
reproduction succeeds. The stress-test yields two cautionary, generalisable results. First, a
natural spreading-activation statistic for "is a concept near an emotion?" is **underpowered**:
in a positive control it fails to detect fear-embedding that we inject by hand, so any null it
returns is uninterpretable; a distance-based measure, validated by the same control, is needed.
With that validated measure and a degree-preserving null, STEM concepts are not closer to fear
than chance in either group, and several are significantly farther (equivalence-tested,
FDR-corrected). Second, an apparent students-versus-experts difference in fear cohesion **does
not survive a change of emotion lexicon**: it appears only with the NRC-derived labels and
vanishes under an independent valence–arousal lexicon. We conclude that STEM negativity in these
data is evaluative and lexical rather than a wiring of concepts into an affective fear network,
and, more broadly, that emotion–network claims should be validated with positive controls and
across lexicons before being read as facts about the mind. This is a non-preregistered
reanalysis; a confirmatory reproduction is separated from exploratory analyses throughout.

**Keywords:** reproducibility; robustness; cognitive network science; forma mentis networks;
math anxiety; emotion lexicons

## 1. Introduction

How a subject *feels* to a learner predicts whether they pursue it, and math anxiety is the
sharpest case (Ashcraft, 2002). Cognitive network science reads such attitudes from the structure
of the mental lexicon (Siew, Wulff, Beckage & Kenett, 2019), and behavioural *forma mentis*
networks reconstruct a group's mindset toward cue concepts from continued free associations, with
each word carrying an affective label (Stella et al., 2019). Comparing Italian high-schoolers with
international researchers, Stella et al. (2019) reported above-chance emotional homophily in both
groups and a markedly more negative framing of mathematics among students, whose negative
"emotional auras" around maths, physics and statistics they related to science anxiety. This
programme is active and growing: reviews frame math anxiety as a networked complex system (Stella,
2022), and recent work profiles the emotions of math-anxious associative structures and compares
humans with large language models (Ciringione et al., 2025; Franchino et al., 2026), typically
using the eight Plutchik emotions from the NRC lexicon as implemented in EmoAtlas (Semeraro et
al., 2025; Mohammad & Turney, 2013).

Two questions sit just beyond that literature, and both are really questions about *method*. The
first is whether a group difference in an emotion-network statistic is robust to the analytic
choices that produced it, the concern behind multiverse and many-analyst analyses (Steegen,
Tuerlinckx, Gelman & Vanpaemel, 2016; Silberzahn et al., 2018). Emotion labels, in particular,
come from a chosen lexicon, and a result that appears with one lexicon and not another is a
property of the instrument, not the mind. The second is subtler. Valence, and even a per-emotion
frequency profile, cannot separate two structurally different situations: a concept that is
*evaluated* negatively, and a concept that is *wired into* the network region where an emotion
lives. A word can attract negative associates because the things attached to it are unpleasant,
without sitting anywhere near where fear is organised. Asking "is mathematics close to fear?"
requires a structural test, one whose power, like any test's, we have checked.

We take up both. We first reproduce the valence-level findings of Stella et al. (2019) from the
released data, to establish that we are working with the same object. We then run the natural
emotion-resolved extension as a stress-test: we relabel words with the eight Plutchik emotions,
ask whether fear is cohesive and whether STEM concepts are structurally close to it. The core
methodological content is that we validate the structural test with a positive control and
check every emotion result across four lexicons. The contribution is not a new phenomenon; the
emotion-resolved machinery is established. It is a reproduction plus a robustness audit that
surfaces two cautions of general use, and a correspondingly careful reading of what the data do
and do not show.

## 2. Methods

**Design and transparency.** This is a secondary reanalysis of open data; nothing was
preregistered. Following Meta-Psychology's convention we separate a *confirmatory reproduction*
of Stella et al. (2019) (Section 3.1) from *exploratory analyses* (Sections 3.2–3.6). All data are
public and all code, intermediate labels, and figures are released (see Data and Code
Availability), including a runnable pipeline and a tutorial notebook.

**Data.** The forma mentis networks are the OSF release of Stella et al. (2019) (osf.io/xyfwg,
CC-BY 4.0): undirected free-association edge lists and per-word valence labels (Positive,
Negative, Neutral) for Italian high-school students (4,483 nodes, 10,628 edges) and international
STEM researchers (1,616 nodes, 3,045 edges). External affective norms: Warriner, Kuperman &
Brysbaert (2013) for English; Montefinese, Ambrosini, Fairfield & Mammarella (2014) and Fairfield,
Ambrosini, Mammarella & Montefinese (2017) for Italian valence–arousal.

**Reproduction.** We recomputed link-level valence assortativity (symmetrised Kendall's τ over
edge endpoints), neighbourhood valence clustering (Kendall's τ between a valenced word's valence
and its neighbours' mean valence), each against a degree-preserving double-edge-swap null; the
negative share of *mathematics*'s associates; and the rank correlation of the English labels with
Warriner valence.

**Emotion labelling and lexicons.** Words were labelled with Plutchik's eight emotions via
EmoAtlas (Semeraro et al., 2025), whose labels derive from the NRC lexicon (Mohammad & Turney,
2013). For robustness we relabelled *fear* three further ways: the NRC word list applied directly;
a valence–arousal quadrant (fear-like = below-median valence and above-median arousal) from
Warriner (English) and Fairfield et al. (2017) (Italian), which is independent of NRC; and
DepecheMood++ (Araque, Gatti, Staiano & Guerini, 2022).

**Network measures.** Emotion assortativity is the correlation of a binary emotion indicator
across edge endpoints (Newman, 2003), the discrete-emotion analogue of the affective-dimension
assortativity documented for the mental lexicon (Van Rensbergen, De Deyne & Storms, 2015).
Significance used a label-shuffle null; uncertainty used a nonparametric edge bootstrap (95% CI).
Group inference rests on within-network measures because the two networks are in different
languages. Communities were detected with Louvain (Blondel, Guillaume, Lambiotte & Lefebvre,
2008), checked for stability across 50 seeds.

**Structural proximity and its validation.** To ask whether STEM concepts are close to fear we
first tried spreading activation as personalised PageRank seeded on each concept, scoring the
stationary mass on fear nodes. We subjected this statistic to a **positive control**: injecting
synthetic edges from a concept into the fear set and checking whether the score rises. It does not
(Section 3.3), so we replaced it with a distance-based measure from single-source shortest paths,
a decay-weighted proximity $\text{prox}(c)=\sum_{f\in\text{fear}}\beta^{\,d(c,f)}$ with $\beta=0.5$,
which passes the same control. The permutation null is **degree-stratified** (fear-sized samples
matched to the fear set's degree profile), and we frame the result as an **equivalence test**
against the injection-calibrated minimum detectable effect (Lakens, 2017), correcting the
concept-level tests for multiple comparisons (Benjamini–Hochberg, q = 0.05).

**Software.** Python 3.11 (networkx, scipy, numpy, pandas, EmoAtlas); fixed seeds.

## 3. Results

### 3.1 Confirmatory reproduction of Stella et al. (2019)

Node counts are exact. Researcher link-level valence assortativity is τ = 0.116 against the
reported 0.116, and researcher neighbourhood clustering τ = 0.324 against 0.323; the students'
values, 0.147 and 0.398, fall within about 0.02 of the reported 0.163 and 0.385, a residual
consistent with unspecified tie-handling in the original Kendall computation. Every effect stands
far above its degree-preserving null. *Mathematics* carries 44% negative associates against the
reported ~43%, and the English labels correlate with Warriner valence at τ = 0.294 over 1,177
overlapping words, an overlap all but identical to the paper's 1,173. We are analysing the network
the original study reported.

### 3.2 Exploratory: fear is a cohesive emotion, and it replicates across lexicons

With EmoAtlas, fear assortativity is 0.129 in students and 0.052 in researchers, both above the
label-shuffle null, and Louvain places that cohesion in stable, thematic modules (existential
danger, health and death, mental turmoil in students; disease, terrorism and instability in
experts; modularity 0.52 and 0.58, varying under 0.003 across 50 seeds). Because EmoAtlas inherits
NRC, we checked three further lexicons (Table 1). Within each group the cohesion holds: an
independent valence–arousal quadrant, using human ratings and no NRC information, gives significant
positive fear assortativity in both groups (students 0.065, researchers 0.067), as does the direct
NRC list for researchers (0.048); only DepecheMood, whose fear category is the argmax of a
news-derived mood distribution, returns near zero. Restricting all lexicons to the vocabulary they
jointly cover leaves this intact (independent VAD: students 0.278, researchers 0.099). Fear is a
robustly cohesive emotion in these mindsets.

Table 1. Fear assortativity across four emotion lexicons (95% CI).
  EmoAtlas (NRC-synset)      students +0.129 [0.105, 0.157]   researchers +0.052 [0.007, 0.098]
  NRC word-level (direct)    students   n/a (no Italian NRC)   researchers +0.048 [0.005, 0.098]
  VAD quadrant (independent) students +0.065 [0.040, 0.095]   researchers +0.067 [0.027, 0.104]
  DepecheMood (independent)  students +0.007 [-0.011, 0.028]  researchers +0.002 [-0.032, 0.041]

### 3.3 Exploratory: a spreading-activation test cannot answer the structural question

The obvious way to ask whether STEM concepts sit inside the fear region is spreading activation,
scoring the personalised-PageRank mass a concept places on fear nodes against random label sets.
That statistic fails a basic positive control. Seeding activation directly on fear words returns z
near zero, and injecting as many as thirteen synthetic edges from *mathematics* into the fear
region still does not move it above significance. A test that cannot see embedding we have
manufactured cannot be trusted to report its absence, so we discard it, and with it any "null
result" it would have produced. This is the paper's first general caution: a diffusion statistic
in common use needs a power check before a null over it means anything.

### 3.4 Exploratory: a validated proximity test, with a degree-preserving null

The decay-weighted proximity passes the same injection control: it crosses significance once
roughly 10–30% of a concept's edges are redirected to fear, which fixes a minimum detectable
effect. Against a degree-preserving null (fear-sized samples matched to the fear set's degree
profile, since fear words tend to be high-degree), no STEM concept in either group is closer to
fear than chance. Several are significantly *farther*: science, mathematics and physics in
researchers, and science, statistics, *scuola* and *insegnante* in students, all surviving a
Benjamini–Hochberg correction across the twenty-two concept tests. An equivalence check makes the
null positive rather than merely absent: for the hard-science concepts the bootstrapped 90%
proximity interval sits below the detectable-effect threshold (mathematics [−1.2, +1.1] in
students, [−2.8, −1.1] in researchers). The test has the power to detect a moderate embedding;
none is there.

### 3.5 Exploratory: the dissociation and the vocabulary that carries negativity

*Mathematics* is reliably negative in valence yet not close to fear. Its one-hop Plutchik profile,
if anything, tilts toward the epistemic vocabulary the lexicon codes as trust (*teorema, assioma,
razionale*), and the words that actually link STEM concepts to nearby fear terms are terms of
difficulty and technique: *mathematics* reaches fear through *limite, difficoltà, problema,
disturbo*; *chemistry* through *farmaco, gas, forza*; *physics* through *friction, force,
dynamics*. STEM negativity enters through the language of hardness, not a channel into the emotion
system.

### 3.6 Exploratory: what is not robust, the student–expert fear gap

One emotion result does not survive the lexicon check. With EmoAtlas, fear cohesion looks stronger
in students (0.129) than experts (0.052), a gap with non-overlapping intervals inviting a "students
are more fearful" reading. The independent valence–arousal lexicon dissolves it: there students
and experts are indistinguishable (0.065 versus 0.067), and DepecheMood places both near zero.
The apparent gap is specific to the NRC-derived labelling, most plausibly because EmoAtlas's synset
expansion tags more of the students' school-and-anxiety vocabulary as fear. The robust claim is
that fear is cohesive in both mindsets; that it *distinguishes* them is a labelling artifact.

## 4. Discussion

Resolved by emotion and tested by structure, students' STEM mindset separates into two things
valence had fused. Its negativity is real and reproducible, and it is carried by the language of
difficulty rather than by proximity to where fear is organised. Fear itself is genuinely cohesive
in both mindsets, and that survives independent lexicons; but the core STEM concepts are not
embedded in it, and under a degree-matched null they are held at a distance from it in both groups.
The psychologically loaded reading, that students' science concepts are wired into an anxiety
system, is not what the network shows. Network "fear" here is a lexical property of a concept's
associates, not measured anxiety, and we keep the two apart.

The point of the paper is methodological, and its two cautions generalise beyond this dataset. A
single valence coefficient, and even a single emotion lexicon, can mislead: the student–expert
fear gap looked solid until an independent lexicon removed it, exactly the sensitivity that
multiverse and many-analyst work warns about (Steegen et al., 2016; Silberzahn et al., 2018).
And structural questions need power: a spreading-activation statistic in common use could not
detect an embedding we injected by hand, so the negative it would have returned would have been a
property of the test, not of the mind. A positive control is cheap and decisive, and we recommend
it wherever a null over network diffusion is claimed. Neither caution is a new technique; both are
standard rigour imported into a subfield that does not yet use them.

For math anxiety the reading is deliberately narrow. These are cross-sectional free associations,
not affective measurements, and they license description, not diagnosis. If the negative charge of
STEM reaches learners through difficulty vocabulary rather than direct emotional association, the
difficulty "bridge" words are where a longitudinal or experimental design could test whether
loosening those links changes anything. That is a hypothesis this design raises, not one it
settles.

## 5. Limitations

The design rests on two networks, one per group, differing in language and population, so
group-level claims are case-study strength pending a multi-cohort design; the recent larger STEM
forma mentis datasets, including LLM-based comparisons (Ciringione et al., 2025; Franchino et al.,
2026), are the natural replication target. EmoAtlas inherits the NRC tendency to code epistemic
terms as trust, so the trust tilt around technical concepts is partly a lexicon property; we
report it with that caveat and check fear against three other lexicons. The Italian resources are
thinner than the English ones: the independent valence–arousal lexicon covers only part of the
students' network, and no open Italian NRC word list was available for the within-family check.

## 6. Conclusion

Reproducing an emotional forma mentis result and then stress-testing its natural extension turns
one valence contrast into a sharper, more honest picture. Fear is a robustly cohesive emotion in
STEM mindsets, but the core STEM concepts are not wired into it; their negativity is evaluative and
lexical. Along the way, a common spreading-activation statistic proved underpowered and one
apparent group difference proved to be a single-lexicon artifact. These are two reasons to resolve emotions,
vary the lexicon, and validate the test before reading network structure as psychology.

## Data and Code Availability

Primary data: Stella et al. (2019), OSF osf.io/xyfwg (CC-BY 4.0). Norms: Warriner et al. (2013);
Fairfield et al. (2017); DepecheMood++ (Araque et al., 2022); NRC (Mohammad & Turney, 2013). All
reproduction and extension code, cached emotion labels, figures, a one-command pipeline, and a
tutorial notebook are openly available at
https://github.com/Jacoposchenetti/Emotion-resolved-forma-mentis-networks, with a README and
download script that fetches every third-party dataset from its source.

## Author Contributions (CRediT)

J.S.: Conceptualization, Methodology, Software, Formal analysis, Data curation, Writing – original
draft, Writing – review & editing, Visualization.

## Conflict of Interest and Funding

The author declares no competing interests. No funding was received for this work.

## AI-Usage Disclosure

Data acquisition, analysis code, statistics, figures, and a first manuscript draft were produced
with an AI coding assistant (Claude) under the author's direction. All numbers are reproducible
from the released scripts; the author verified the analyses and is responsible for the content.

## Ethics

Secondary analysis of publicly released, de-identified data; no new human-subjects data were
collected.

## References

Araque, O., Gatti, L., Staiano, J., & Guerini, M. (2022). DepecheMood++: A bilingual emotion lexicon built through simple yet powerful techniques. IEEE Transactions on Affective Computing, 13(1), 496-507. https://doi.org/10.1109/TAFFC.2019.2934444

Ashcraft, M. H. (2002). Math anxiety: Personal, educational, and cognitive consequences. Current Directions in Psychological Science, 11(5), 181-185. https://doi.org/10.1111/1467-8721.00196

Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008

Ciringione, L., Franchino, E., Reigl, S., D'Onofrio, I., Serbati, A., Poquet, O., Gabriel, F., & Stella, M. (2025). Math anxiety and associative knowledge structure are entwined in psychology students but not in large language models like GPT-3.5 and GPT-4o [Preprint]. arXiv:2511.01558. https://arxiv.org/abs/2511.01558

De Deyne, S., Navarro, D. J., Perfors, A., Brysbaert, M., & Storms, G. (2019). The "Small World of Words" English word association norms for over 12,000 cue words. Behavior Research Methods, 51(3), 987-1006. https://doi.org/10.3758/s13428-018-1115-7

Fairfield, B., Ambrosini, E., Mammarella, N., & Montefinese, M. (2017). Affective norms for Italian words in older adults: Age differences in ratings of valence, arousal and dominance. PLOS ONE, 12(1), e0169472. https://doi.org/10.1371/journal.pone.0169472

Franchino, E., Gariboldi, F., Grecucci, A., Lattanzi, G., & Stella, M. (2026). Complex networks map test anxiety and wellbeing levels in students and ChatGPT [Preprint]. arXiv:2602.13302. https://arxiv.org/abs/2602.13302

Lakens, D. (2017). Equivalence tests: A practical primer for t tests, correlations, and meta-analyses. Social Psychological and Personality Science, 8(4), 355-362. https://doi.org/10.1177/1948550617697177

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. Computational Intelligence, 29(3), 436-465. https://doi.org/10.1111/j.1467-8640.2012.00460.x

Montefinese, M., Ambrosini, E., Fairfield, B., & Mammarella, N. (2014). The adaptation of the Affective Norms for English Words (ANEW) for Italian. Behavior Research Methods, 46(3), 887-903. https://doi.org/10.3758/s13428-013-0405-3

Newman, M. E. J. (2003). Mixing patterns in networks. Physical Review E, 67(2), 026126. https://doi.org/10.1103/PhysRevE.67.026126

Plutchik, R. (1980). A general psychoevolutionary theory of emotion. In R. Plutchik & H. Kellerman (Eds.), Emotion: Theory, research, and experience (Vol. 1, pp. 3-33). Academic Press.

Semeraro, A., Vilella, S., Improta, R., De Duro, E. S., Mohammad, S. M., Ruffo, G., & Stella, M. (2025). EmoAtlas: An emotional network analyzer of texts that merges psychological lexicons, artificial intelligence, and network science. Behavior Research Methods, 57, Article 77. https://doi.org/10.3758/s13428-024-02553-7

Siew, C. S. Q., Wulff, D. U., Beckage, N. M., & Kenett, Y. N. (2019). Cognitive network science: A review of research on cognition through the lens of network representations, processes, and dynamics. Complexity, 2019, 2108423. https://doi.org/10.1155/2019/2108423

Silberzahn, R., Uhlmann, E. L., Martin, D. P., Anselmi, P., Aust, F., Awtrey, E., … Nosek, B. A. (2018). Many analysts, one data set: Making transparent how variations in analytic choices affect results. Advances in Methods and Practices in Psychological Science, 1(3), 337-356. https://doi.org/10.1177/2515245917747646

Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing transparency through a multiverse analysis. Perspectives on Psychological Science, 11(5), 702-712. https://doi.org/10.1177/1745691616658637

Stella, M. (2022). Network psychometrics and cognitive network science open new ways for understanding math anxiety as a complex system. Journal of Complex Networks, 10(3), cnac012. https://doi.org/10.1093/comnet/cnac012

Stella, M., De Nigris, S., Aloric, A., & Siew, C. S. Q. (2019). Forma mentis networks quantify crucial differences in STEM perception between students and experts. PLOS ONE, 14(10), e0222870. https://doi.org/10.1371/journal.pone.0222870

Van Rensbergen, B., De Deyne, S., & Storms, G. (2015). Examining assortativity in the mental lexicon: Evidence from word associations. Psychonomic Bulletin & Review, 22(6), 1717-1724. https://doi.org/10.3758/s13423-015-0832-5

Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior Research Methods, 45(4), 1191-1207. https://doi.org/10.3758/s13428-012-0314-x

## Figures

Figure 1. Emotion prevalence across the two networks.
Figure 2. Fear assortativity across four emotion lexicons (bootstrap 95% CI). Within-group cohesion is robust (three of four lexicons, including the independent VAD); the student-expert gap appears only for EmoAtlas.
Figure 3. Injection positive control: the discarded PageRank statistic (flat, no power) versus the validated decay-proximity measure (crosses significance at 10-30% of degree).
Figure 4. Validated proximity of STEM concepts to fear under a degree-preserving null: no concept is closer than chance in either group, and several are significantly farther (FDR-corrected).
