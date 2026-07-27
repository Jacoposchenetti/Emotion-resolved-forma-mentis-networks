# Valence without fear: emotion-resolved forma mentis networks show that STEM negativity is evaluative, not affectively wired

*Manuscript draft: secondary analysis of open data. Prepared with AI assistance (see disclosure). Every statistic is reproducible from the released code.*

## Abstract

How learners feel about science and mathematics predicts whether they pursue it, and free-association "forma mentis" networks read that feeling from the words people spontaneously produce. Prior work compressed the affect carried by these networks into a single positive/negative/neutral valence label. Valence, however, is a projection: it merges discrete emotions that may be organised very differently, and it cannot tell whether a concept is merely evaluated negatively or is structurally tied to an emotion. We revisit the open student and expert STEM networks of Stella and colleagues, resolve their affect into Plutchik's eight emotions, and add the structural test that valence omits. Three findings survive scrutiny. First, the original valence results reproduce closely. Second, fear is a cohesive, thematically organised emotion in both mindsets, and this cohesion replicates across independent emotion lexicons. Third, and centrally, the core STEM concepts are not wired into that fear structure. A proximity test, which we first show has the power to detect embedding when it exists, finds mathematics, physics, and chemistry no closer to the fear region than chance in either group; under a degree-preserving null several are significantly farther from it. STEM negativity is therefore evaluative and lexical, routed through the vocabulary of difficulty rather than through a connection into the emotional fear network. Two cautionary results frame these conclusions: a widely used spreading-activation statistic proves underpowered for this question, and one apparent group difference, greater fear cohesion in students, turns out to be an artifact of a single lexicon family. We argue that mindset networks should be analysed at the resolution of emotions, across lexicons, and with power-validated structural tests.

**Keywords:** cognitive network science; forma mentis networks; emotion lexicons; math anxiety; spreading activation; reproducibility

## Abstract (Italiano)

Il modo in cui gli studenti vivono la scienza e la matematica ne predice la scelta, e le reti di libere associazioni ("forma mentis") leggono quell'atteggiamento dalle parole prodotte spontaneamente. Il lavoro precedente comprimeva l'affetto in un'unica etichetta di valenza. La valenza però fonde emozioni discrete organizzate in modo diverso e non distingue un concetto valutato negativamente da uno legato a un'emozione. Ripartendo dalle reti aperte di studenti ed esperti STEM di Stella e colleghi, risolviamo l'affetto nelle otto emozioni di Plutchik e aggiungiamo il test strutturale che la valenza omette. Tre risultati reggono: (i) i risultati di valenza originali si riproducono fedelmente; (ii) la paura è un'emozione coesa e tematicamente organizzata in entrambe le menti, e la coesione replica con lessici indipendenti; (iii) i concetti STEM non sono cablati in quella struttura di paura. Un test di prossimità, di cui prima dimostriamo la potenza, trova matematica, fisica e chimica non più vicine alla paura del caso in nessuno dei due gruppi; sotto un null che preserva il grado, diverse sono significativamente più lontane. La negatività STEM è dunque valutativa e lessicale, veicolata dal vocabolario della difficoltà anziché da una connessione al sistema affettivo. Due risultati cautelativi incorniciano le conclusioni: una statistica di spreading activation molto usata è underpowered per questa domanda, e una differenza apparente, la maggiore coesione della paura negli studenti, si rivela un artefatto di un'unica famiglia di lessici.

## 1. Introduction

Attitudes toward science, technology, engineering, and mathematics form early and shape participation. Math anxiety is the sharpest case: it consumes working memory, drives avoidance, and forecloses quantitative careers, with correlations to motivation and confidence as high as .82 in absolute value (Ashcraft, 2002). Measuring how a subject feels to a learner, not only how well they perform, is therefore part of understanding who stays in STEM.

Cognitive network science reads cognition from the topology of the mental lexicon (Siew et al., 2019). Within this programme, forma mentis networks reconstruct a group's mindset toward a set of cue concepts from continued free associations: words are nodes, an association is an edge, and each word can be tagged with an affective label (Stella et al., 2019). Comparing Italian high-schoolers with international researchers, Stella et al. (2019) found above-chance emotional homophily in both networks and a markedly more negative framing of mathematics among students.

That analysis, like most forma mentis work, encoded affect as three-level valence. Valence is a useful summary and a lossy one. It merges fear, anger, disgust, and sadness into a single "negative", although a mindset whose negativity is organised around fear is psychologically distinct from one organised around disgust. That distinction matters precisely for a construct like math anxiety, which is, after all, an anxiety. Valence also cannot separate two structurally different situations: a concept that is evaluated negatively, and a concept that is wired into the network's emotional machinery. A word can attract negative associates because the things attached to it are unpleasant, without sitting anywhere near the region where an emotion actually lives.

We take up both gaps. We resolve affect into Plutchik's (1980) eight emotions using EmoAtlas (Semeraro et al., 2025), whose labels derive from the crowd-sourced NRC lexicon (Mohammad & Turney, 2013), and we add an explicit structural test of whether STEM concepts are close, in the network, to the emotion of fear. The paper makes four contributions. It reproduces the valence-level findings of Stella et al. (2019) as a baseline. It shows that fear is a cohesive emotion in both mindsets and checks that this holds across four emotion lexicons, two of them independent of NRC. It demonstrates that a common spreading-activation statistic is underpowered for the structural question, and replaces it with a proximity test validated by a positive control. And it uses that validated test to establish a dissociation: STEM concepts are negatively evaluated without being affectively wired to fear, and under a degree-preserving null they are, if anything, held at a distance from it in both groups.

## 2. Methods

### 2.1 Data

We used the forma mentis data released by Stella et al. (2019) on the Open Science Framework (osf.io/xyfwg, CC-BY 4.0): undirected free-association edge lists and per-word valence labels (Positive, Negative, Neutral) for Italian high-school students and international STEM researchers. As simple graphs the students' network has 4,483 nodes and 10,628 edges, the researchers' 1,616 nodes and 3,045 edges, matching the reported node counts. External affective norms were Warriner, Kuperman, and Brysbaert (2013) for English and the Italian ANEW adaptation of Montefinese, Ambrosini, Fairfield, and Mammarella (2014); for the arousal-based analyses we drew Italian valence–arousal ratings from the openly released norms of Fairfield, Ambrosini, Mammarella, and Montefinese (2017).

### 2.2 Reproduction

We recomputed the paper's core quantities from the edge lists: link-level valence assortativity (symmetrised Kendall τ over edge endpoints), neighbourhood valence clustering (Kendall τ between a valenced word's valence and its neighbours' mean valence), each against a degree-preserving double-edge-swap null; the negative share of mathematics's associates; and the rank correlation of the English labels with Warriner valence.

### 2.3 Emotion labelling and lexicons

Each node received binary indicators for Plutchik's eight emotions via EmoAtlas, Italian lexicon for students and English for researchers. To test lexicon robustness we relabelled fear three further ways: the NRC word-level lexicon applied directly (English), a valence–arousal quadrant definition (fear-like = below-median valence and above-median arousal, from Warriner for English and the Fairfield et al. (2017) norms for Italian), and DepecheMood++ (Araque et al.), whose fear-like category is AFRAID for English and PREOCCUPATO for Italian. NRC-family and independent (VAD, DepecheMood) lexicons let us separate a genuine signal from a labelling artifact.

### 2.4 Network and structural measures

Emotion prevalence, and emotion assortativity (the correlation of a binary emotion indicator across edge endpoints, i.e. Newman's (2003) numeric assortativity), were computed per network; significance used a label-shuffle null (z) and a nonparametric edge bootstrap (95% CI). Because the networks are in different languages, group inference rests on within-network measures, not raw prevalence. Communities were detected with Louvain (Blondel et al., 2008) and characterised by fear enrichment.

### 2.5 Structural proximity to fear, and its validation

To ask whether STEM concepts are close to fear we first tried spreading activation as personalised PageRank seeded on each concept, summing stationary mass on fear nodes against a fear-label-permutation null. We then subjected this statistic to a positive control, injecting synthetic edges from a concept to fear nodes, and found it could not detect embedding even when we created it (Section 3.3). We therefore replaced it with a distance-based proximity measure from single-source shortest paths: a decay-weighted proximity, the sum of β^d over fear nodes (β = 0.5), tested against the same permutation null. We validated this measure with the same injection control and characterised its minimum detectable effect before interpreting it. The permutation null is degree-stratified: the fear-sized comparison samples are drawn to match the fear set's degree distribution across deciles, so proximity is judged against degree-matched random sets rather than uniform ones. We report the result as an equivalence test, asking whether a concept's bootstrapped proximity stays below the effect the injection control calls detectable, and we correct the concept-level tests for multiple comparisons (Benjamini-Hochberg, q = 0.05). Community partitions were checked for stability across 50 Louvain seeds. We also traced the first intermediate nodes on shortest paths from each concept to nearby fear words to identify the linking vocabulary.

### 2.6 Reproducibility

Analyses used Python 3.11 with networkx, scipy, numpy, pandas, and EmoAtlas; seeds were fixed. All scripts, emotion-label tables, and figures are released.

## 3. Results

### 3.1 The valence-level network reproduces

Node counts are exact. Researcher link-level valence assortativity is τ = 0.116 against the reported 0.116, and researcher neighbourhood clustering τ = 0.324 against 0.323; the students' values, 0.147 and 0.398, fall within about 0.02 of the reported 0.163 and 0.385, a residual consistent with unspecified tie-handling. Every effect stands far above its degree-preserving null. Mathematics carries 44% negative associates against the reported ~43%, and the English labels correlate with Warriner valence at τ = 0.294 over 1,177 overlapping words, an overlap all but identical to the paper's 1,173. The network we analyse is the network the original study reported.

### 3.2 Fear is a cohesive emotion in both mindsets, and it replicates across lexicons

Every emotion clusters above chance in both networks, so emotional homophily is not specific to valence. Fear is prominent: with EmoAtlas its assortativity is 0.129 in students and 0.052 in researchers, both far above the label-shuffle null. Louvain shows where that cohesion lives. In students it sits in dedicated modules organised around existential danger (paura, orrore, pericolo, spavento), health and death (ospedale, tumore, autopsia, catastrofe), and mental turmoil; in experts it gathers around disease, death, pandemics, terrorism, and instability. Fear is a coherent region, not scattered noise.

Because EmoAtlas inherits NRC, we checked fear cohesion against three further lexicons (Table 1). It holds. An independent valence–arousal quadrant definition, which uses human ratings and no NRC information, yields significant positive fear assortativity in both groups (students 0.065, researchers 0.067), as does the directly applied NRC word list for researchers (0.048). Only DepecheMood, whose fear category is the argmax of a news-derived mood distribution and which shows the lowest agreement with every other lexicon, returns near zero. Three of four lexicons, including an independent one in each language, agree: fear is a robustly cohesive organising emotion in STEM mindsets. Restricting every lexicon to the vocabulary they jointly cover leaves this intact. On the common subset the independent valence–arousal lexicon still yields significant fear cohesion in both groups (students 0.278, researchers 0.099), so the agreement is not an artifact of uneven coverage. The fear communities are also stable: modularity is 0.52 in students and 0.58 in researchers, varying by less than 0.003 across 50 Louvain seeds.

Table 1. Fear assortativity across four emotion lexicons (95% CI).
  EmoAtlas (NRC-synset)      students +0.129 [0.105, 0.157]   researchers +0.052 [0.007, 0.098]
  NRC word-level (direct)    students   n/a (no Italian NRC)   researchers +0.048 [0.005, 0.098]
  VAD quadrant (independent) students +0.065 [0.040, 0.095]   researchers +0.067 [0.027, 0.104]
  DepecheMood (independent)  students +0.007 [-0.011, 0.028]  researchers +0.002 [-0.032, 0.041]

### 3.3 A naive spreading-activation test cannot answer the structural question

The next question is whether STEM concepts sit inside that fear structure. The natural tool is spreading activation, and the natural statistic is the personalised-PageRank mass a concept places on fear nodes relative to random label sets. That statistic fails a basic positive control. Seeding activation directly on fear words returns z near zero, and injecting as many as thirteen synthetic edges from mathematics straight into the fear region still does not move the statistic above significance. A test that cannot see embedding we have manufactured cannot be trusted to report its absence. We discard it, and with it any "null result" it would have produced.

### 3.4 A validated proximity test: STEM concepts are not wired to fear

We replaced the statistic with a decay-weighted proximity to the fear set and validated it the same way. Now the injection control works: proximity crosses significance once roughly ten to thirty per cent of a concept's associations are redirected to fear, giving the test a quantified minimum detectable effect. Against a degree-preserving null, one that draws fear-sized samples matched to the fear set's own degree profile, no STEM concept in either group is closer to fear than chance. Several are significantly farther: science, mathematics, and physics in researchers, and science, statistics, scuola, and insegnante in students, all of which survive a Benjamini-Hochberg correction across the twenty-two concept tests. An equivalence check turns the null into a positive claim rather than a mere failure to reject: for the hard-science concepts the bootstrapped 90% interval of proximity sits below the detectable-effect threshold (mathematics [−1.2, +1.1] in students, [−2.8, −1.1] in researchers), so the data support equivalence to no fear-embedding. The test has the power to detect a moderate embedding. None is there. The earlier appearance that only experts hold science away from fear was an artifact of a uniform null; under the degree-matched null both groups do.

### 3.5 The dissociation, and the vocabulary that carries negativity

The reproduction and the structural test point the same way. Mathematics is reliably negative in valence, yet it is not close to fear. Its one-hop Plutchik profile is, if anything, tilted toward the epistemic vocabulary the lexicon codes as trust (teorema, assioma, razionale), and the words that actually link STEM concepts to nearby fear terms are neither affective nor topical but terms of difficulty and technique: mathematics reaches fear through limite, difficoltà, problema, disturbo; chemistry through farmaco, gas, forza; physics through friction, force, dynamics. STEM negativity enters through the language of hardness, not through a channel into the emotion system.

### 3.6 What is not robust: the student–expert fear gap

One result from the emotion-resolved analysis does not survive the lexicon check, and we report it as such. With EmoAtlas, fear cohesion looks stronger in students (0.129) than experts (0.052), a difference with non-overlapping intervals that invites a "students are more fearful" reading. The independent valence–arousal lexicon dissolves it: there students and experts are indistinguishable (0.065 versus 0.067), and DepecheMood places both near zero. The apparent group gap is specific to the NRC-synset labelling, most plausibly because EmoAtlas's synset expansion tags more of the students' school-and-anxiety vocabulary as fear. The robust claim is that fear is cohesive in both mindsets; the claim that it distinguishes them is a labelling artifact.

## 4. Discussion

Resolved by emotion and tested by structure, students' STEM mindset separates into two things valence had fused. Its negativity is real and reproducible, and it is carried by the language of difficulty rather than by proximity to where fear is organised. Fear itself is genuinely cohesive in both mindsets, and that survives independent lexicons. But the core STEM concepts are not embedded in it, and under a degree-matched null they are held at a distance from it in both groups. The psychologically loaded reading, that students' science concepts are wired into an anxiety system, is not what the network shows. One caution belongs here rather than only in the limitations: network "fear" is a lexical property of the words a concept associates with, not measured anxiety, and we keep the two apart throughout.

This dissociation is the paper's substantive claim, and two methodological findings protect it. The first is that a single valence coefficient, and even a single emotion lexicon, can mislead: the student–expert fear gap looked solid until an independent lexicon removed it. Emotion-resolved network results should be reported across lexical resources, not from one. The second is that structural questions need power. A spreading-activation statistic in common use could not detect an embedding we injected by hand; the negative it would have returned would have been a property of the test, not of the mind. A positive control is cheap and it is decisive, and we recommend it wherever a null over network diffusion is claimed.

For math anxiety the reading is deliberately narrow. These are cross-sectional free associations, not affective measurements, and they license description, not diagnosis. What they suggest is a target: if the negative charge of STEM reaches students through difficulty vocabulary rather than through direct emotional association, then the difficulty "bridge" words are where the charge is transmitted and where a longitudinal or experimental design could test whether loosening those links changes anything. That is a hypothesis this design raises, not one it settles.

## 5. Limitations

Four constraints bound the conclusions. EmoAtlas inherits the NRC tendency to code epistemic terms as trust, so the trust tilt around technical concepts is partly a lexicon property; we report it with that caveat and check fear against three other lexicons. The two networks are in different languages, so raw prevalence is confounded and group inference rests on within-network measures. The data are free associations collected cross-sectionally, describing structure rather than process. The design also rests on two networks, one per group: every group-level claim, including the finding that experts distance science from fear, is a case-study observation that a multi-cohort design should test, and the recent larger STEM forma mentis datasets (including LLM digital twins) are an obvious replication target. And the Italian resources are thinner than the English ones: the independent valence–arousal lexicon covers only part of the students' network, and no Italian NRC word list was openly available for the within-family check.

## 6. Conclusion

Fear is a robustly cohesive emotion in STEM mindsets, yet the core STEM concepts are not wired into it. That gap, between a concept that is evaluated negatively and one that is affectively organised, is exactly what a single valence label hides. Recovering it took three things a valence summary skips: discrete emotions, more than one lexicon, and a structural test whose power we had checked. Two of those steps caught our own mistakes before they reached print, which is the stronger argument for taking them.

## Figures

Figure 1. Emotion prevalence across the two networks.
Figure 2. Fear assortativity across four lexicons with bootstrap CIs (Table 1 visualised): cohesion is robust within each group, but the student–expert gap appears only for EmoAtlas.
Figure 3. Injection positive control: the discarded PageRank statistic (flat, no power) versus the validated decay-proximity measure (crosses significance at 10–30% of degree).
Figure 4. Validated proximity of STEM concepts to fear under a degree-preserving null: none is closer than chance in either group, and several concepts are significantly farther (Benjamini-Hochberg corrected).

## Data and code availability

Primary data: Stella et al. (2019), OSF osf.io/xyfwg (CC-BY 4.0). Norms: Warriner et al. (2013); Fairfield et al. (2017); DepecheMood++ (Araque et al., 2022); NRC (Mohammad & Turney, 2013). All reproduction and extension code, emotion-label tables, and figures are released with this manuscript.

## AI-usage disclosure

Data acquisition, analysis code, statistics, figures, and a first manuscript draft were produced with an AI coding assistant under author direction. All numbers are reproducible from the released scripts; the authors verified the analyses and take responsibility for the content.

## Author contributions, competing interests, funding, ethics

CRediT roles to be completed. No competing interests declared. Funding to be completed. Secondary analysis of publicly released, de-identified data; no new human-subjects data were collected.

## References

Ashcraft, M. H. (2002). Math anxiety: Personal, educational, and cognitive consequences. Current Directions in Psychological Science, 11(5), 181-185. https://doi.org/10.1111/1467-8721.00196

Araque, O., Gatti, L., Staiano, J., & Guerini, M. (2022). DepecheMood++: A bilingual emotion lexicon built through simple yet powerful techniques. IEEE Transactions on Affective Computing, 13(1), 496-507. https://doi.org/10.1109/TAFFC.2019.2934444

Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics: Theory and Experiment, 2008(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008

Fairfield, B., Ambrosini, E., Mammarella, N., & Montefinese, M. (2017). Affective norms for Italian words in older adults: Age differences in ratings of valence, arousal and dominance. PLOS ONE, 12(1), e0169472. https://doi.org/10.1371/journal.pone.0169472

Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a word-emotion association lexicon. Computational Intelligence, 29(3), 436-465. https://doi.org/10.1111/j.1467-8640.2012.00460.x

Montefinese, M., Ambrosini, E., Fairfield, B., & Mammarella, N. (2014). The adaptation of the Affective Norms for English Words (ANEW) for Italian. Behavior Research Methods, 46(3), 887-903. https://doi.org/10.3758/s13428-013-0405-3

Newman, M. E. J. (2003). Mixing patterns in networks. Physical Review E, 67(2), 026126. https://doi.org/10.1103/PhysRevE.67.026126

Plutchik, R. (1980). A general psychoevolutionary theory of emotion. In R. Plutchik & H. Kellerman (Eds.), Emotion: Theory, research, and experience (Vol. 1, pp. 3-33). Academic Press.

Semeraro, A., Vilella, S., Improta, R., De Duro, E. S., Mohammad, S. M., Ruffo, G., & Stella, M. (2025). EmoAtlas: An emotional network analyzer of texts that merges psychological lexicons, artificial intelligence, and network science. Behavior Research Methods, 57, Article 77. https://doi.org/10.3758/s13428-024-02553-7

Siew, C. S. Q., Wulff, D. U., Beckage, N. M., & Kenett, Y. N. (2019). Cognitive network science: A review of research on cognition through the lens of network representations, processes, and dynamics. Complexity, 2019, 2108423. https://doi.org/10.1155/2019/2108423

Stella, M., De Nigris, S., Aloric, A., & Siew, C. S. Q. (2019). Forma mentis networks quantify crucial differences in STEM perception between students and experts. PLOS ONE, 14(10), e0222870. https://doi.org/10.1371/journal.pone.0222870

Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior Research Methods, 45(4), 1191-1207. https://doi.org/10.3758/s13428-012-0314-x
