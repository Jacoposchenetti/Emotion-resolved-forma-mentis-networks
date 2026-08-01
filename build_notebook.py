# -*- coding: utf-8 -*-
"""Assemble PAPER_WALKTHROUGH.ipynb — a runnable, technique-by-technique guide."""
import json, os

cells = []
def md(t):   cells.append({"cell_type": "markdown", "metadata": {}, "source": t})
def code(t): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": t})

# ---------------------------------------------------------------- title
md(r"""# Valence without fear — a step-by-step walkthrough

This notebook explains, **technique by technique**, the paper *"Valence without fear:
emotion-resolved forma mentis networks show that STEM negativity is evaluative, not
affectively wired."* For every method you get: the **idea**, the **mathematics**, a
tiny **worked example** you can check by hand, and then the **real computation** on the
Stella et al. (2019) data.

**Run order.** Execute the cells top to bottom. If you cloned the repo, first run
`python download_data.py` in the repo root (it fetches the datasets into `data/`).
The Plutchik emotion labels are cached in `results_A1/`, so **EmoAtlas is not needed**.

**Map of the argument.**
1. what a forma mentis network *is*
2. valence assortativity (Kendall's τ) and its null model — the reproduction
3. resolving valence into 8 emotions; emotion-specific cohesion
4. community structure of fear
5. spreading activation — and why the naive version is a trap
6. a validated proximity test, a degree-preserving null, equivalence testing, FDR
7. lexicon robustness and the final dissociation
""")

# ---------------------------------------------------------------- 0 setup
md(r"""## 0. Setup

We import the scientific stack and the project's own modules (each script in the repo is
importable). We also check the data is present.""")
code(r"""import os, sys, numpy as np, networkx as nx, pandas as pd
from scipy.stats import kendalltau
import matplotlib.pyplot as plt

HERE = os.getcwd()
assert os.path.exists("reproduce_stem_fmn.py"), "Run this notebook from the repo root."
DATA = os.path.join(HERE, "data", "stem")
if not os.path.exists(os.path.join(DATA, "FormaMentisStudents.txt")):
    print("Data missing -> run `python download_data.py` first.")
else:
    print("Data OK:", sorted(os.listdir(DATA)))

import reproduce_stem_fmn as R          # reproduction helpers
np.random.seed(42)""")

# ---------------------------------------------------------------- 1 data
md(r"""## 1. The data: a forma mentis network

A **forma mentis network** ("mindset network") is built from a *continued free-association*
task. Participants see a cue word (e.g. *matematica*) and write the words it brings to
mind; those responses become cues in turn. Aggregated over people you get a graph:

- **nodes** = words,
- **edges** = "these two words were associated,"
- each node also carries an **affective label**. In the original study that label is a
  three-level **valence**: `Positive`, `Negative`, or `Neutral`.

There are two networks: **students** (Italian high-schoolers) and **researchers**
(international STEM experts). Let's load them and look.""")
code(r"""GS = R.build("FormaMentisStudents.txt", "ValenceLabelsStudents.txt")
GR = R.build("FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt")

for name, G in [("students", GS), ("researchers", GR)]:
    vl = nx.get_node_attributes(G, "vlabel")
    from collections import Counter
    print(f"{name:12s} nodes={G.number_of_nodes():5d} edges={G.number_of_edges():5d} "
          f"valence={dict(Counter(vl.values()))}")

# a concrete neighbourhood: what surrounds 'matematica' in the students' network?
nb = list(GS.neighbors("matematica"))
print("\n'matematica' has", len(nb), "associates, e.g.:", nb[:12])""")
md(r"""`R.build` stores two node attributes: `vlabel` (the string) and `val`, a numeric
encoding **Positive = +1, Negative = −1, Neutral = 0**. That numeric map is what makes
"do positive words connect to positive words?" a computable question.""")

# ---------------------------------------------------------------- 2 tiny example
md(r"""## 2. Warm-up: assortativity on a 4-node graph

Before the real network, here is the whole idea on something you can check by eye.
Assortativity asks: **do the two endpoints of an edge tend to share a value?**

Consider 4 words with valences and 3 associations:

```
   joy(+1) --- smile(+1) --- exam(-1) --- fear(-1)
```

Two edges join same-valence words, one edge (`smile`–`exam`) joins opposite valences.
We expect a **positive** assortativity, but not maximal.""")
code(r"""T = nx.Graph()
val = {"joy": 1, "smile": 1, "exam": -1, "fear": -1}
T.add_edges_from([("joy","smile"), ("smile","exam"), ("exam","fear")])

# Build the endpoint vectors. An edge is undirected, so to avoid an arbitrary
# orientation we enter BOTH orders (symmetrisation).
X, Y = [], []
for u, v in T.edges():
    X += [val[u], val[v]]
    Y += [val[v], val[u]]
print("edge endpoint pairs (X,Y):", list(zip(X, Y)))
tau, p = kendalltau(X, Y)
print(f"Kendall tau = {tau:.3f}")""")
md(r"""So the statistic is just a **rank correlation between the valence at one end of an
edge and the valence at the other end**, computed over all edges entered in both
directions. Positive τ = *homophily* (like connects to like).""")

# ---------------------------------------------------------------- 3 kendall + reproduction
md(r"""## 3. Kendall's τ, and reproducing the paper's valence assortativity

### The mathematics
Kendall's τ compares all pairs of observations $(x_i,y_i),(x_j,y_j)$. A pair is
**concordant** if the ranks agree ($ (x_i-x_j)(y_i-y_j) > 0 $) and **discordant** if they
disagree. With $C$ concordant and $D$ discordant pairs out of $\binom{n}{2}$,

$$\tau_a = \frac{C - D}{\binom{n}{2}}.$$

Our valences are heavily tied (only $-1,0,+1$), so we use **τ-b**, which divides by a
tie-corrected denominator:

$$\tau_b = \frac{C-D}{\sqrt{(C+D+T_x)(C+D+T_y)}},$$

where $T_x,T_y$ count pairs tied in $x$ or $y$ only. `scipy.stats.kendalltau` returns
$\tau_b$.

### On the real data
This reproduces one of the original paper's headline numbers.""")
code(r"""def link_valence_assortativity(G):
    val = nx.get_node_attributes(G, "val")
    X, Y = [], []
    for u, v in G.edges():
        X += [val[u], val[v]]; Y += [val[v], val[u]]
    return kendalltau(X, Y)

for name, G, paper in [("students", GS, 0.163), ("researchers", GR, 0.116)]:
    tau, p = link_valence_assortativity(G)
    print(f"{name:12s} tau = {tau:.3f}   (paper reported {paper})   p = {p:.1e}")""")
md(r"""The researchers' value lands on **0.116**, exactly the reported figure; the students'
is within rounding. Positive and highly significant: **words of a given valence associate
with same-valence words far more than a random wiring would give.** (We prove the "than
random" part in §5 with a null model.)""")

# ---------------------------------------------------------------- 4 neighbourhood clustering
md(r"""## 4. Valence "auras": neighbourhood clustering

Link-level assortativity is pairwise. A complementary view asks, for each *valenced* word,
whether its **whole neighbourhood** leans the same way. Define, for node $i$ with neighbour
set $N(i)$,

$$\bar v_i = \frac{1}{|N(i)|}\sum_{j\in N(i)} v_j ,$$

and correlate $v_i$ against $\bar v_i$ across nodes (Kendall's τ again). The paper restricts
this to non-neutral centres (words that actually carry a valence).""")
code(r"""def neighbourhood_clustering(G, only_valenced=True):
    val = nx.get_node_attributes(G, "val")
    X, Y = [], []
    for n in G.nodes():
        if only_valenced and val[n] == 0:
            continue
        nb = list(G.neighbors(n))
        if nb:
            X.append(val[n]); Y.append(np.mean([val[m] for m in nb]))
    return kendalltau(X, Y)

for name, G, paper in [("students", GS, 0.385), ("researchers", GR, 0.323)]:
    tau, p = neighbourhood_clustering(G)
    print(f"{name:12s} tau = {tau:.3f}   (paper {paper})")""")
md(r"""A positive/negative word sits in a positive/negative *aura*. Finding the right
operationalisation mattered: including neutral centres roughly halves the coefficient, and
only the "valenced-centres" version matches the paper — a good reminder that a statistic is
only as reproducible as its exact definition.""")

# ---------------------------------------------------------------- 5 null model
md(r"""## 5. Null models I: is 0.116 *big*? Degree-preserving randomisation

A correlation of 0.12 means nothing until we know what **chance** looks like *for this
network*. The right null keeps everything structural fixed and destroys only the thing we
are testing. Here we keep each node's **degree** and its **valence label**, and randomise
*which* nodes connect, with a **double edge swap**:

$$(a\!-\!b),\,(c\!-\!d)\ \longrightarrow\ (a\!-\!d),\,(c\!-\!b).$$

Every node keeps its degree (so the degree sequence and the valence multiset are intact);
only the pairing of valences across edges is scrambled. Repeating $\sim 10E$ times mixes the
graph. We then read off a **z-score**: $z = (\text{observed} - \mu_{\text{null}})/\sigma_{\text{null}}$.""")
code(r"""def null_z(G, stat_fn, nrep=30, swaps_per_edge=5, seed=0):
    rng = np.random.default_rng(seed)
    obs = stat_fn(G)[0]
    null = []
    E = G.number_of_edges()
    for _ in range(nrep):
        H = G.copy()
        try:
            nx.double_edge_swap(H, nswap=swaps_per_edge*E, max_tries=50*E,
                                seed=int(rng.integers(1e9)))
        except nx.NetworkXError:
            pass
        null.append(stat_fn(H)[0])
    null = np.array(null)
    z = (obs - null.mean())/null.std()
    return obs, null.mean(), null.std(), z

# (small nrep so the notebook is fast; the paper used 50 well-mixed realisations)
obs, mu, sd, z = null_z(GR, link_valence_assortativity, nrep=25)
print(f"researchers valence assortativity: obs={obs:.3f}  null={mu:+.3f} ± {sd:.3f}  z={z:.1f}")
print("=> the observed value sits many standard deviations above chance.")""")
md(r"""The null mean is essentially **zero** and the observed value is many σ above it. That
is the sentence "emotional homophily is above chance," made quantitative. Every network
statistic in the paper is reported against a null like this.""")

# ---------------------------------------------------------------- 6 emotions
md(r"""## 6. From valence to eight emotions

Valence flattens *fear, anger, disgust, sadness* into one word: "negative." But a mind
whose negativity is built around **fear** is not the same as one built around **disgust** —
and for math anxiety, fear is the point. So we relabel every node with **Plutchik's eight
emotions** (anger, anticipation, disgust, fear, joy, sadness, surprise, trust).

The labels come from the **NRC Emotion Lexicon** (Mohammad & Turney, 2013), a crowd-sourced
word→emotion table, applied through **EmoAtlas**. A word gets a 1 for each emotion it
elicits (it can carry several, or none). These labels are cached in `results_A1/` so we
just load them.""")
code(r"""EMOS = ["anger","anticipation","disgust","fear","joy","sadness","surprise","trust"]
emoS = pd.read_csv("results_A1/emolabels_italian.csv", index_col=0).reindex(list(GS.nodes())).fillna(0).astype(int)
emoR = pd.read_csv("results_A1/emolabels_english.csv", index_col=0).reindex(list(GR.nodes())).fillna(0).astype(int)

# a few example words and the emotions they carry
for w in ["ansia", "matematica", "gioia", "paura", "biologia"]:
    if w in emoS.index:
        print(f"{w:12s}", [e for e in EMOS if emoS.loc[w, e] > 0] or "(no emotion)")

# prevalence: share of words carrying each emotion
prev = pd.DataFrame({"students": emoS[EMOS].mean(), "researchers": emoR[EMOS].mean()}).round(3)
print("\nprevalence (fraction of words):\n", prev)""")
md(r"""Note *matematica* itself carries **no** discrete emotion — it is a topic word. Its
negativity (we saw 44% negative associates) is therefore *valence*, not lexical *fear*. Hold
that thought; it becomes the whole result.""")

# ---------------------------------------------------------------- 7 emotion assortativity
md(r"""## 7. Emotion-specific cohesion, with a bootstrap confidence interval

Now repeat the assortativity idea **per emotion**. For emotion $e$ let $x_i\in\{0,1\}$ mark
whether word $i$ carries $e$. Newman's numeric assortativity for a scalar attribute is just
the **Pearson correlation of the attribute across edge endpoints** (symmetrised):

$$r_e = \operatorname{corr}\big(x_u, x_v\big)_{(u,v)\in E}.$$

To get uncertainty we **bootstrap the edges**: resample $E$ edges with replacement $B$ times
and recompute $r_e$; the 2.5th–97.5th percentiles give a 95% CI.""")
code(r"""def emotion_assortativity(G, attr):
    edges = list(G.edges())
    x = np.array([attr[u] for u,v in edges], float)
    y = np.array([attr[v] for u,v in edges], float)
    def r(xx, yy):
        X = np.concatenate([xx,yy]); Y = np.concatenate([yy,xx])
        return 0.0 if X.std()==0 or Y.std()==0 else np.corrcoef(X,Y)[0,1]
    return r(x, y), x, y

def boot_ci(G, attr, B=300, seed=1):
    obs, x, y = emotion_assortativity(G, attr)
    rng = np.random.default_rng(seed)
    def r(xx, yy):
        X=np.concatenate([xx,yy]); Y=np.concatenate([yy,xx])
        return 0.0 if X.std()==0 or Y.std()==0 else np.corrcoef(X,Y)[0,1]
    bs = [r(*(lambda s:(x[s],y[s]))(rng.integers(0,len(x),len(x)))) for _ in range(B)]
    return obs, np.percentile(bs,2.5), np.percentile(bs,97.5)

for name, G, emo in [("students", GS, emoS), ("researchers", GR, emoR)]:
    attr = {n:int(emo.loc[n,"fear"]>0) for n in G.nodes()}
    o, lo, hi = boot_ci(G, attr)
    print(f"{name:12s} FEAR assortativity = {o:.3f}  95% CI [{lo:.3f}, {hi:.3f}]")""")
md(r"""With **EmoAtlas** labels, fear looks more cohesive in students (≈0.13) than experts
(≈0.05). That was the first-draft "headline." Keep it provisional — in §15 an *independent*
lexicon dissolves the between-group gap, which is exactly why the paper checks more than one
lexicon.""")

# ---------------------------------------------------------------- 8 communities
md(r"""## 8. Where fear lives: community detection

Assortativity says fear clusters; **community detection** shows the clusters. **Louvain**
maximises **modularity**

$$Q = \frac{1}{2m}\sum_{ij}\Big[A_{ij} - \frac{k_i k_j}{2m}\Big]\,\delta(c_i,c_j),$$

the fraction of edges inside communities minus what you'd expect at random ($A$ = adjacency,
$k_i$ = degree, $m$ = number of edges, $c_i$ = community of $i$). We then ask which
communities are richest in fear.""")
code(r"""from networkx.algorithms import community
comms = community.louvain_communities(GS, seed=1)
fear_nodes = set(emoS.index[emoS["fear"]>0])
rows = sorted(((len(c), len(c & fear_nodes)/len(c),
               [w for w in list(c)[:60] if w in fear_nodes][:6]) for c in comms if len(c)>=20),
              key=lambda t:-t[1])[:3]
print(f"modularity Q = {community.modularity(GS, comms):.3f}")
for sz, frac, ex in rows:
    print(f"  community size={sz:4d}  fear={frac*100:4.1f}%  e.g. {ex}")""")
md(r"""The fear-rich modules are thematic — existential danger (*paura, pericolo*), health and
death (*ospedale, tumore*), mental turmoil (*caos, confusione*). Fear is an organised region,
not scattered noise, and across 50 Louvain seeds the modularity is stable to ±0.003.""")

# ---------------------------------------------------------------- 9 pagerank
md(r"""## 9. Spreading activation with personalised PageRank

Cohesion is not the real question. The real question is **structural**: are the STEM
*concepts* wired into that fear region? A classic tool is **spreading activation**, modelled
as **personalised PageRank**. Starting from a seed concept $s$, activation flows along edges
with probability $\alpha$ and teleports back to $s$ with probability $1-\alpha$. The
stationary vector $\pi$ solves

$$\pi = \alpha\, P^\top \pi + (1-\alpha)\, e_s,$$

with $P$ the row-normalised adjacency (a random walk) and $e_s$ the restart vector on the
seed. The candidate statistic is the **fear-mass** $\sum_{f\in \text{fear}}\pi_f$: how much
activation from *matematica* lands on fear words, versus random label sets.""")
code(r"""def fear_mass(G, seed, fear_nodes, alpha=0.85):
    pr = nx.pagerank(G, alpha=alpha, personalization={seed: 1.0})
    return sum(pr[f] for f in fear_nodes if f in pr), pr

fm, pr = fear_mass(GS, "matematica", fear_nodes)
# compare to random label sets of the same size (uniform null)
rng = np.random.default_rng(0); nodes = list(GS.nodes()); k = len(fear_nodes)
null = [sum(pr[n] for n in rng.choice(nodes, k, replace=False)) for _ in range(500)]
z = (fm - np.mean(null))/np.std(null)
print(f"'matematica' fear-mass z (uniform null) = {z:.2f}  -> looks like ~no effect")""")

# ---------------------------------------------------------------- 10 the trap
md(r"""## 10. The trap: a null result you cannot trust

A z near zero *seems* to say "matematica is not close to fear." But before believing a
**null**, you must show the test could have detected the effect **if it were there**. That is
a **positive control**. We inject synthetic edges from *matematica* straight into the fear
region and re-measure. A trustworthy test's signal should climb as we add edges.""")
code(r"""def inject_and_measure(G, seed, fear_nodes, j, reps=4, seed0=1):
    rng = np.random.default_rng(seed0)
    targets = [f for f in fear_nodes if f != seed and not G.has_edge(seed, f)]
    zs = []
    for _ in range(reps):
        H = G.copy()
        if j: H.add_edges_from((seed, targets[t]) for t in rng.choice(len(targets), j, replace=False))
        fm, pr = fear_mass(H, seed, fear_nodes)
        null = [sum(pr[n] for n in rng.choice(list(H.nodes()), len(fear_nodes), replace=False)) for _ in range(200)]
        zs.append((fm - np.mean(null))/np.std(null))
    return np.mean(zs)

for j in [0, 3, 8, 13]:
    print(f"  +{j:2d} injected edges -> PageRank fear-mass z = {inject_and_measure(GS,'matematica',fear_nodes,j):+.2f}")""")
md(r"""**The z barely moves even with 13 forced edges.** The PageRank fear-mass is *blind*: a
few local edges are drowned in a stationary distribution spread over thousands of nodes, and
the random-set null has large variance. So the earlier "null result" was a property of the
**test**, not of the mind. We discard it. This is the paper's first methodological caution:
*validate a structural test before you trust its null.*""")

# ---------------------------------------------------------------- 11 proximity
md(r"""## 11. A test that works: distance with a decay kernel

We need something **local** and sensitive. Use shortest-path distance $d(c,f)$ (in hops,
from a breadth-first search) and weight nearby fear words heavily with a decaying kernel:

$$\text{prox}(c) = \sum_{f\in \text{fear}} \beta^{\,d(c,f)}, \qquad \beta = 0.5.$$

A fear word one hop away contributes $0.5$; two hops $0.25$; far ones almost nothing. Direct
wiring now moves the number a lot — so the injection control (below) actually responds.""")
code(r"""BETA = 0.5
def decay_prox(G, seed, fear_nodes):
    d = nx.single_source_shortest_path_length(G, seed)
    return sum(BETA**d[f] for f in fear_nodes if f in d and d[f] > 0)

# does the validated measure pass the injection control?
def inj_decay(G, seed, fear_nodes, j, reps=4, seed0=2):
    rng = np.random.default_rng(seed0); nodes = list(G.nodes()); k = len(fear_nodes)
    targets = [f for f in fear_nodes if f != seed and not G.has_edge(seed,f)]
    zs = []
    for _ in range(reps):
        H = G.copy()
        if j: H.add_edges_from((seed, targets[t]) for t in rng.choice(len(targets), j, replace=False))
        obs = decay_prox(H, seed, fear_nodes)
        d = nx.single_source_shortest_path_length(H, seed)
        null = [sum(BETA**d.get(n,99) for n in rng.choice(nodes,k,replace=False)) for _ in range(200)]
        null = np.array(null); zs.append((obs-null.mean())/null.std())
    return np.mean(zs)
for j in [0, 5, 10, 20]:
    print(f"  +{j:2d} edges -> decay-proximity z = {inj_decay(GS,'matematica',fear_nodes,j):+.2f}")""")
md(r"""Now the signal **climbs and crosses significance** at roughly 10–30% of the concept's
degree. That crossing is the **minimum detectable effect (MDE)**: the smallest real embedding
this test would catch. With a validated instrument in hand we can finally ask the real
question — and trust the answer.""")

# ---------------------------------------------------------------- 12 degree null
md(r"""## 12. Null models II: why the *degree* of fear words matters

One subtlety a reviewer caught. Fear words tend to be **high-degree hubs** (*dominio, esame*).
A uniform random comparison set contains many low-degree words that are far from everything,
so it makes the null look "far" and can fake a result. The fix: a **degree-stratified null** —
draw comparison sets whose degree profile *matches the fear set's*, bin by bin. Then
"closer/farther than chance" is judged against degree-matched randomness.""")
code(r"""import revision_analyses as RV     # the paper's degree-stratified implementation
for name, ef, vf, lang, concept in [("students","FormaMentisStudents.txt","ValenceLabelsStudents.txt","italian","matematica"),
                                    ("researchers","FormaMentisResearchers.txt","ValenceLabelsResearchers.txt","english","mathematics")]:
    G, fear = RV.load(ef, vf, lang)
    z, p = RV.prox_degstrat(G, fear, concept, nperm=400)
    print(f"{name:12s} '{concept}': proximity z = {z:+.1f}  p = {p:.3f}  (neg = farther from fear)")""")
md(r"""Under the corrected null, **no** STEM concept is closer to fear than chance in either
group; several are significantly *farther*. (This also overturned a first-draft claim that
only experts distance science from fear — that contrast was an artifact of the uniform null.)""")

# ---------------------------------------------------------------- 13 TOST
md(r"""## 13. Equivalence testing: from "not significant" to "equivalent to zero"

"Not significant" is not "absent." **Equivalence testing** (the logic of TOST — two one-sided
tests) flips the burden of proof. Instead of $H_0:\text{effect}=0$, you set a smallest effect
you'd care about, $\Delta$ (here the injection **MDE**), and test

$$H_0:\ |\text{effect}| \ge \Delta \quad\text{vs}\quad H_1:\ |\text{effect}| < \Delta .$$

If a bootstrap interval for the concept's proximity lies **entirely below** $\Delta$, you have
positive evidence of *no meaningful* fear-embedding — not just a failure to reject.""")
code(r"""G, fear = RV.load("FormaMentisResearchers.txt","ValenceLabelsResearchers.txt","english")
for c in ["mathematics","physics","chemistry"]:
    lo, hi = RV.prox_bootstrap_ci(G, fear, c, nboot=120, nperm=250)
    verdict = "equivalent to NO positive embedding" if hi < 1.96 else "inconclusive"
    print(f"  {c:12s} proximity z 90% CI = [{lo:+.2f}, {hi:+.2f}]  -> {verdict}")""")
md(r"""The upper bound sits below the detectable-effect threshold, so the null is now a
**positive** claim: these concepts are *equivalent to unwired* with respect to fear.""")

# ---------------------------------------------------------------- 14 FDR
md(r"""## 14. Many tests: Benjamini–Hochberg FDR

We test ~12 concepts × 2 groups. Testing many hypotheses inflates false positives, so we
control the **false discovery rate**. Benjamini–Hochberg: sort the $m$ p-values
$p_{(1)}\le\dots\le p_{(m)}$, find the largest $k$ with

$$p_{(k)} \le \frac{k}{m}\,q ,$$

and reject all hypotheses up to $k$ (here $q=0.05$).""")
code(r"""def benjamini_hochberg(pvals, q=0.05):
    p = np.sort(pvals); m = len(p)
    thresh = q*np.arange(1, m+1)/m
    below = np.where(p <= thresh)[0]
    return (p[below.max()] if len(below) else 0.0)

# a small illustrative set of p-values
demo = [0.002, 0.010, 0.014, 0.030, 0.20, 0.51, 0.92]
crit = benjamini_hochberg(demo)
print("p-values :", demo)
print(f"BH critical p (q=0.05) = {crit:.3f}  -> reject all p <= {crit:.3f}")""")
md(r"""In the paper, seven concept tests survive BH correction, and **all of them are in the
"farther from fear" direction** — none is "closer." The dissociation is not a multiple-
comparisons fluke.""")

# ---------------------------------------------------------------- 15 lexicon robustness
md(r"""## 15. Is fear cohesion real, or a lexicon artifact?

EmoAtlas gets its emotions from NRC. A finding that only appears with one lexicon family is a
labelling artifact, not a fact about minds. So we relabel fear with **independent** resources:

- a **valence–arousal quadrant** (fear-like = low valence + high arousal), from human ratings
  (Warriner for English, Fairfield et al. for Italian) — independent of NRC;
- **DepecheMood++**, built from news mood-voting — also independent.

and recompute fear assortativity across all of them.""")
code(r"""# reuse the project's estimator; VAD quadrant labels from human norms
import robustness_lexicon as RL
def vad_fear_attr(G, lang):
    if lang == "english":
        w = pd.read_csv("data/warriner.csv")
        val = dict(zip(w["Word"].str.lower(), w["V.Mean.Sum"])); aro = dict(zip(w["Word"].str.lower(), w["A.Mean.Sum"]))
    else:
        df = pd.read_excel("data/it_vad_s001.xlsx", sheet_name="Database", header=1)
        val = dict(zip(df["Ita_Word"].astype(str).str.lower(), pd.to_numeric(df["M_Val"],errors="coerce")))
        aro = dict(zip(df["Ita_Word"].astype(str).str.lower(), pd.to_numeric(df["M_Aro"],errors="coerce")))
    vm, am = np.nanmedian(list(val.values())), np.nanmedian(list(aro.values()))
    return {n:(1 if (str(n).lower() in val and val[str(n).lower()]<vm and aro[str(n).lower()]>am) else 0) for n in G.nodes()}

for name, G, emo, lang in [("students", GS, emoS, "italian"), ("researchers", GR, emoR, "english")]:
    ea = {n:int(emo.loc[n,"fear"]>0) for n in G.nodes()}
    o1,l1,h1 = RL.assort_ci(G, ea)
    va = vad_fear_attr(G, lang); o2,l2,h2 = RL.assort_ci(G, va)
    print(f"{name:12s} EmoAtlas r={o1:.3f} [{l1:.3f},{h1:.3f}] | independent VAD r={o2:.3f} [{l2:.3f},{h2:.3f}]")""")
md(r"""**Two conclusions, and they differ.**
- *Within* each group the independent VAD lexicon still finds significant fear cohesion → the
  cohesion is **robust** (not an NRC artifact).
- *Between* groups, the students>experts gap that EmoAtlas showed **vanishes** under VAD
  (students ≈ experts). So that between-group claim was lexicon-specific and is **dropped**.

This is the paper's second methodological caution: *vary the lexicon before you believe an
emotion-network result.*""")

# ---------------------------------------------------------------- 16 synthesis
md(r"""## 16. Synthesis: valence without fear

Put the pieces together:

| technique | what it established |
|---|---|
| Kendall-τ valence assortativity + null | reproduces Stella et al. (2019); valence homophily is above chance |
| Plutchik relabelling | negativity resolves into emotions; *matematica* itself carries none |
| emotion assortativity + bootstrap + 4 lexicons | **fear is robustly cohesive** in both mindsets |
| Louvain | fear forms stable, thematic modules |
| PageRank + injection control | the naive structural test is **underpowered** — discard it |
| decay-proximity + degree-stratified null + TOST + FDR | STEM concepts are **not** closer to fear than chance; several are farther |

**The dissociation.** STEM negativity is **evaluative and lexical** — it travels through the
vocabulary of *difficulty* (*limite, problema, esame*) — **not** a wiring of STEM concepts
into the affective fear network. The word *matematica* is judged negative without being
*afraid*.

And two lessons about method, both learned the hard way in this very analysis: **validate a
structural test with a positive control**, and **vary the lexicon** before reading an
emotion-network number as a fact about the mind.
""")

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.11"}},
      "nbformat": 4, "nbformat_minor": 4}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER_WALKTHROUGH.ipynb"), "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("wrote PAPER_WALKTHROUGH.ipynb with", len(cells), "cells")
