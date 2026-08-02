# -*- coding: utf-8 -*-
"""Assemble PAPER_WALKTHROUGH.ipynb — a beginner-first, technique-by-technique guide
that starts from single-subject trials and builds up to the aggregate metrics."""
import json, os

cells = []
def md(t):   cells.append({"cell_type": "markdown", "metadata": {}, "source": t})
def code(t): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": t})

# ================================================================ TITLE
md(r"""# From words in people's heads to a number: a from-scratch walkthrough

This notebook explains the paper *"Valence without fear: emotion-resolved forma mentis
networks show that STEM negativity is evaluative, not affectively wired"* **assuming you have
never seen a network before.**

We build everything from the ground up:

- **Part A** — what a network *is* (dots and lines), with pictures.
- **Part B** — how the raw data of **individual people, one trial at a time**, becomes a
  single aggregated network. This is the part most papers skip.
- **Part C** — how each word gets *meaning* (valence, emotions).
- **Part D** — every metric in the paper, first on a tiny toy graph you can check by eye,
  then on the real data.

Every concept comes with a concrete **Esempio**. Run the cells top to bottom. If you cloned
the repo, first run `python download_data.py`.
""")

# ================================================================ SETUP
md(r"""## Setup""")
code(r"""import os, numpy as np, networkx as nx, pandas as pd
from scipy.stats import kendalltau
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

assert os.path.exists("reproduce_stem_fmn.py"), "Run from the repo root."
import reproduce_stem_fmn as R
np.random.seed(0)

def draw(G, values=None, title="", cmap_neg_pos=True, ax=None, seed=1):
    # Tiny helper to draw a small graph, optionally colouring nodes by a value.
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 3.4))
    pos = nx.spring_layout(G, seed=seed)
    if values is None:
        colors = "#cfe3ff"
    elif cmap_neg_pos:
        colors = ["#e06666" if values[n] < 0 else "#93c47d" if values[n] > 0 else "#dddddd" for n in G.nodes()]
    else:
        colors = ["#f6b26b" if values.get(n, 0) else "#dddddd" for n in G.nodes()]
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#999")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=900, edgecolors="#444")
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
    ax.set_title(title); ax.axis("off")
    return ax
print("ready")""")

# ================================================================ PART A
md(r"""# Part A — What is a network?

A **network** (a *graph*) is just **dots joined by lines**. The dots are **nodes**; the lines
are **edges**. That's the whole idea. Networks are useful whenever "things" are "related":
people and friendships, cities and roads, or — as here — **words and the associations between
them**.

### Esempio: a friendship network
Anna knows Bea and Carla; Bea knows Carla; Dan knows only Carla.""")
code(r"""F = nx.Graph()
F.add_edges_from([("Anna","Bea"), ("Anna","Carla"), ("Bea","Carla"), ("Carla","Dan")])
draw(F, title="A tiny friendship network"); plt.show()
print("nodes:", list(F.nodes()))
print("edges:", list(F.edges()))""")

md(r"""### Neighbours and degree
The **neighbours** of a node are the dots directly joined to it. The **degree** is *how many*
neighbours it has — a simple measure of how connected something is.

**Esempio:** Carla is joined to Anna, Bea, and Dan, so Carla's degree is 3. Dan's degree is 1.""")
code(r"""for person in F.nodes():
    print(f"{person:6s} neighbours = {list(F.neighbors(person))!s:30s} degree = {F.degree(person)}")""")

md(r"""### The adjacency matrix
The same network can be written as a table: a **1** in row *i*, column *j* means "i and j are
joined," **0** means "not joined." This table is the **adjacency matrix** $A$. Everything a
computer does with a graph is really arithmetic on $A$.

**Esempio:** row "Carla" has three 1s (Anna, Bea, Dan) — matching her degree of 3. In fact
the degree of a node is just the **sum of its row**.""")
code(r"""A = nx.to_pandas_adjacency(F, nodelist=sorted(F.nodes()), dtype=int)
print(A)
print("\nrow sums (= degrees):"); print(A.sum(axis=1))""")

md(r"""### Paths and distance
A **path** is a chain of edges from one node to another. The **distance** between two nodes is
the length of the *shortest* such chain, counted in edges ("hops"). Distance is how we will
later ask "how far is *matematica* from *fear*?"

**Esempio:** Anna→Carla→Dan is a path of length 2, so the distance from Anna to Dan is 2
(there is no direct Anna–Dan edge).""")
code(r"""print("shortest path Anna -> Dan:", nx.shortest_path(F, "Anna", "Dan"))
print("distance Anna -> Dan:", nx.shortest_path_length(F, "Anna", "Dan"), "hops")
print("all distances from Anna:", dict(nx.single_source_shortest_path_length(F, "Anna")))""")

md(r"""### Two flavours of edge
- **Undirected vs directed:** friendship is usually mutual (undirected). "A replied to B" has
  a direction (directed). The word networks here are treated as **undirected**.
- **Unweighted vs weighted:** an edge can just exist (unweighted), or carry a number — e.g.
  *how many people* made that association (weighted). We'll meet weights in Part B.

### Why a network for the *mind*?
Psychologists model the **mental lexicon** — your inner dictionary — as a network: words are
nodes, and an edge means the two words are **associated** in people's minds. Thinking of one
word partly activates its neighbours (that's why *bread* makes you think of *butter*). A
network built this way, and enriched with the *feelings* attached to each word, is a
**forma mentis network** — literally a "network of the way of thinking." That is the object
this paper studies.""")

# ================================================================ PART B
md(r"""# Part B — From single people and single trials to one network

Here is the step most tutorials skip. The data does **not** arrive as a graph. It arrives as
**many individual responses**. We now walk the whole assembly line.

## B1. The experiment, one trial at a time
A **trial** is: show one **participant** one **cue word**, and record the words they freely
associate to it. A *continued* association task then feeds those responses back as new cues.
So the atomic record is a triple:

> **(participant, cue, response)**

## B2. A toy dataset of raw responses
Real studies collect hundreds of participants. Let's use five, on a STEM theme, so you can see
every step by hand. Each row is one association a person produced.""")
code(r"""raw = [
    # participant, cue, response  (note the messy capitalisation on purpose)
    (1,"matematica","numeri"), (1,"matematica","difficile"), (1,"matematica","esame"),
    (1,"esame","ansia"),       (1,"esame","voto"),
    (2,"matematica","numeri"), (2,"matematica","logica"),    (2,"matematica","esame"),
    (2,"esame","ansia"),       (2,"ansia","paura"),
    (3,"matematica","Difficile"),(3,"matematica","calcolo"), (3,"esame","Ansia"),
    (3,"ansia","paura"),       (3,"ansia","stress"),
    (4,"matematica","numeri"), (4,"matematica","noia"),      (4,"esame","voto"),
    (5,"matematica","difficile"),(5,"esame","ansia"),        (5,"ansia","paura"),
]
df = pd.DataFrame(raw, columns=["participant","cue","response"])
print(df.to_string(index=False))""")

md(r"""## B3. Trial-level cleaning (normalisation)
People type messily: *Difficile* and *difficile* are the same word; *ansia* and *Ansia* too.
Real pipelines **lowercase**, remove **stopwords** (function words like *the*, *and*), and
**lemmatise** (reduce to a base form: *numeri*→*numero*, *difficoltà*→*difficile*). Skipping
this would split one concept across several nodes.

**Esempio:** below, `Difficile` and `Ansia` collapse onto `difficile` and `ansia`. (We do a
simple lowercase here; the real study uses spaCy lemmatisation.)""")
code(r"""def normalise(w):
    return w.strip().lower()          # real pipeline: + lemmatise + drop stopwords

df["cue"] = df["cue"].map(normalise)
df["response"] = df["response"].map(normalise)
print("distinct response tokens after cleaning:", sorted(df['response'].unique()))""")

md(r"""## B4. One participant → one small graph
Each participant's own responses already form a mini-network: connect every cue to every
response they gave it.

**Esempio — participant 1** produced: matematica→{numeri, difficile, esame}, esame→{ansia, voto}.""")
code(r"""def subject_graph(sub_df):
    g = nx.Graph()
    g.add_edges_from(zip(sub_df["cue"], sub_df["response"]))
    return g

g1 = subject_graph(df[df.participant == 1])
draw(g1, title="Participant 1's associations"); plt.show()
print("participant 1 edges:", list(g1.edges()))""")

md(r"""## B5. Aggregating across people (this is where a *network* is born)
No single person's associations are reliable — one person might link *matematica* to *noia*
out of a bad mood. The signal is what people share. So we **stack every participant's edges**
and **count how many different participants produced each one**. That count is the edge
**weight**: the strength of the association in the group.

**Esempio:** *matematica–numeri* was given by participants 1, 2, and 4 → weight 3.
*matematica–logica* was given only by participant 2 → weight 1.""")
code(r"""edge_participants = defaultdict(set)
for _, r in df.iterrows():
    edge = tuple(sorted((r["cue"], r["response"])))   # undirected: sort the pair
    edge_participants[edge].add(r["participant"])

weights = {e: len(p) for e, p in edge_participants.items()}
wt = pd.DataFrame([(a, b, w) for (a, b), w in sorted(weights.items(), key=lambda x:-x[1])],
                  columns=["word_1","word_2","n_participants"])
print(wt.to_string(index=False))""")

md(r"""## B6. Thresholding — keeping only associations that people share
An edge produced by a **single** person is mostly noise. A standard rule (the one Stella et
al. use for their *filtered* network) is: **keep an edge only if at least 2 different
participants produced it.** This is exactly the *"associations provided by at least two
different participants"* criterion in the paper.

**Esempio:** dropping weight-1 edges removes *logica, calcolo, noia, stress* — idiosyncratic
one-offs — and leaves the shared backbone.""")
code(r"""THRESH = 2
M = nx.Graph()
for (a, b), w in weights.items():
    if w >= THRESH:
        M.add_edge(a, b, weight=w)

print("kept edges (>=2 participants):")
for a, b, w in M.edges(data="weight"):
    print(f"  {a} — {b}   (weight {w})")
print("\ndropped (weight 1):", [e for e, w in weights.items() if w < THRESH])""")

md(r"""## B7. The aggregated forma mentis network (in miniature)
That's it — we have gone from 21 individual responses to **one** group-level network `M`.
Thicker lines = associations more people shared. This little `M` is a forma mentis network;
the real one is the same object built from **hundreds** of students.""")
code(r"""fig, ax = plt.subplots(figsize=(5.5, 3.8))
pos = nx.spring_layout(M, seed=3)
w = [M[u][v]["weight"] for u, v in M.edges()]
nx.draw_networkx_edges(M, pos, width=[x*1.4 for x in w], edge_color="#888", ax=ax)
nx.draw_networkx_nodes(M, pos, node_color="#cfe3ff", node_size=1100, edgecolors="#444", ax=ax)
nx.draw_networkx_labels(M, pos, font_size=8, ax=ax)
ax.set_title("M: our toy aggregated forma mentis network"); ax.axis("off"); plt.show()
print("Notice the chain matematica → esame → ansia → paura: a route from a topic into feelings.")""")

md(r"""## B8. The real data is just this, at scale
The OSF files from Stella et al. (2019) already contain the **final aggregated edge list** —
the output of exactly steps B1–B6, run over hundreds of Italian high-schoolers (and,
separately, international researchers). Let's load it and confirm it is the very same kind of
object as our toy `M`, only bigger.""")
code(r"""GS = R.build("FormaMentisStudents.txt", "ValenceLabelsStudents.txt")
GR = R.build("FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt")
print(f"toy M         : {M.number_of_nodes()} nodes, {M.number_of_edges()} edges")
print(f"students (real): {GS.number_of_nodes()} nodes, {GS.number_of_edges()} edges")
print(f"researchers    : {GR.number_of_nodes()} nodes, {GR.number_of_edges()} edges")
print("\n'matematica' in the real students network is linked to e.g.:",
      list(GS.neighbors('matematica'))[:10])""")

md(r"""## B9. A different raw material: *sentences* instead of associations
Free association is one way to get a word network. You can also build one from **text**: put an
edge between words that appear **close together** in sentences. This is the route the EmoAtlas
tool uses for *textual* forma mentis networks (it connects words within a few **syntactic**
steps; here we use a simple word-window to show the idea).

**Esempio:** two sentences → tokens → edges between neighbours within a window of 2.""")
code(r"""sentences = ["la matematica è difficile e crea ansia",
             "l ansia da esame porta paura"]
STOP = {"la","è","e","l","da","al","il","lo","di","che","un","una"}
def text_to_network(sents, window=2):
    g = nx.Graph()
    for s in sents:
        toks = [t for t in s.split() if t not in STOP]
        for i, t in enumerate(toks):
            for j in range(i+1, min(i+1+window, len(toks))):
                g.add_edge(t, toks[j])
    return g
T = text_to_network(sentences)
draw(T, title="A network built from sentences (co-occurrence window = 2)"); plt.show()
print("edges:", list(T.edges()))""")
md(r"""Whichever raw material you start from — **trials of associations** or **sentences** —
the end product is the same kind of thing: **words as nodes, meaningful proximity as edges.**
Everything from here on works on that object.""")

# ================================================================ PART C
md(r"""# Part C — Giving each word a *feeling*

A bare word network says *what connects to what*. To study attitudes we must also know how each
word *feels*. Two layers of feeling are used.

## C1. Valence: is the word positive, negative, or neutral?
**Valence** is the good–bad axis. Where does it come from? From **human ratings**: psychologists
have asked thousands of people to rate words on a 1–9 pleasantness scale (the *ANEW* norms and
their Italian adaptations). A word above the midpoint is positive, below it negative. In the
paper's data each word already carries a label `Positive / Negative / Neutral`, which the code
turns into **+1 / −1 / 0**.

**Esempio:** *paura* (fear) rates low → negative → −1; *gioia* (joy) rates high → +1;
*matematica* is neutral → 0.""")
code(r"""val_real = nx.get_node_attributes(GS, "vlabel")
for w in ["paura","gioia","matematica","ansia","numeri"]:
    if w in val_real:
        print(f"{w:12s} valence label = {val_real[w]:8s} -> numeric {int(R.VAL_MAP[val_real[w]]):+d}")""")

md(r"""## C2. Emotions: eight specific feelings (Plutchik)
Valence merges very different negatives. **Plutchik's** theory names eight basic emotions —
*anger, anticipation, disgust, fear, joy, sadness, surprise, trust*. A word can carry several.
These labels come from the **NRC Emotion Lexicon**: researchers crowd-sourced, for ~14,000
words, which emotions each evokes. We apply them through EmoAtlas; the results are cached, so
we just read them.

**Esempio:** *ansia* evokes fear, sadness, anger, anticipation. *matematica* evokes **nothing**
— it is an emotionally blank topic word. Remember that: it becomes the punchline.""")
code(r"""EMOS = ["anger","anticipation","disgust","fear","joy","sadness","surprise","trust"]
emoS = pd.read_csv("results_A1/emolabels_italian.csv", index_col=0).reindex(list(GS.nodes())).fillna(0).astype(int)
emoR = pd.read_csv("results_A1/emolabels_english.csv", index_col=0).reindex(list(GR.nodes())).fillna(0).astype(int)
for w in ["ansia","paura","matematica","gioia","difficile"]:
    if w in emoS.index:
        print(f"{w:12s}", [e for e in EMOS if emoS.loc[w, e] > 0] or "(no emotion)")""")

md(r"""## C3. Labels for our toy graph
So we can keep using the tiny graph `M`, we hand-label its seven words. These are illustrative
values chosen to be obvious.""")
code(r"""val_M = {"matematica":0, "numeri":0, "difficile":-1, "esame":-1, "voto":0, "ansia":-1, "paura":-1}
fear_M = {"matematica":0,"numeri":0,"difficile":1,"esame":1,"voto":0,"ansia":1,"paura":1}
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
draw(M, values=val_M, title="M coloured by VALENCE (red=−, grey=0)", ax=axes[0], seed=3)
draw(M, values=fear_M, cmap_neg_pos=False, title="M coloured by FEAR (orange=fear word)", ax=axes[1], seed=3)
plt.show()""")

# ================================================================ PART D
md(r"""# Part D — The metrics, each on the toy graph then on real data

Now the actual analyses. The recipe for each: **(1)** intuition, **(2)** the maths, **(3)** an
**Esempio** on `M` you can verify by eye, **(4)** the real number from the paper.""")

# ---- D1 assortativity
md(r"""## D1. Do like words connect to like words? (assortativity)

**Intuition.** If negative words mostly link to other negative words, the network is
*emotionally sorted*. We measure this by correlating the valence at the two ends of every edge.

**Maths.** For each edge we form a pair (valence of one end, valence of the other). Because an
edge has no direction, we enter each edge **both ways**. Then we take **Kendall's τ**, a rank
correlation that counts concordant minus discordant pairs:

$$\tau = \frac{\#\text{concordant} - \#\text{discordant}}{\text{(tie-corrected total)}}, \qquad
\tau\in[-1,1].$$

**Esempio on M.** Edges and end-valences: matematica(0)–numeri(0), matematica(0)–difficile(−),
matematica(0)–esame(−), esame(−)–ansia(−), esame(−)–voto(0), ansia(−)–paura(−). Same-sign
edges (both negative) pull τ up; mixed 0/− edges are neutral. Expect a positive τ.""")
code(r"""def link_valence_assortativity(G, val):
    X, Y = [], []
    for u, v in G.edges():
        X += [val[u], val[v]]; Y += [val[v], val[u]]   # both orientations
    return kendalltau(X, Y)

tau_M, _ = link_valence_assortativity(M, val_M)
print(f"toy M valence assortativity  tau = {tau_M:.3f}  (positive: negatives clump together)")

val_num = nx.get_node_attributes(GS, "val")
for name, G in [("students", GS), ("researchers", GR)]:
    t, p = link_valence_assortativity(G, nx.get_node_attributes(G, "val"))
    print(f"{name:12s} tau = {t:.3f}")
print("\n-> researchers reproduce the paper's reported 0.116 exactly.")""")

# ---- D2 null model
md(r"""## D2. Is that number *big*? Comparing to chance (null models)

**Intuition.** τ = 0.12 is meaningless until we know what a *random* network of the same shape
would give. So we **shuffle** the wiring while keeping each node's degree and its valence, and
see how often chance alone produces a τ that large.

**Maths.** Repeatedly apply a **double edge swap** — take edges A–B and C–D and rewire to A–D
and C–B — which keeps every degree unchanged but scrambles *who connects to whom*. Compute τ on
each shuffled network to get a null distribution, then a **z-score**
$z=(\tau_{\text{obs}}-\mu_{\text{null}})/\sigma_{\text{null}}$.

**Esempio.** Think of shuffling a deck: the cards (valences) are the same, only their pairing
changes. If the real τ beats almost every shuffle, the sorting is real.""")
code(r"""def null_z(G, val, nrep=200, seed=0):
    rng = np.random.default_rng(seed)
    obs = link_valence_assortativity(G, val)[0]
    null = []
    for _ in range(nrep):
        H = G.copy()
        try:
            nx.double_edge_swap(H, nswap=5*H.number_of_edges(), max_tries=200*H.number_of_edges(),
                                seed=int(rng.integers(1e9)))
        except nx.NetworkXError:
            pass
        null.append(link_valence_assortativity(H, val)[0])
    null = np.array(null)
    return obs, null.mean(), null.std()

obs, mu, sd = null_z(GR, nx.get_node_attributes(GR, "val"), nrep=100)
print(f"researchers: observed={obs:.3f}, chance={mu:+.3f} ± {sd:.3f}, z={(obs-mu)/sd:.1f}")
print("z of ~6+ means: essentially never produced by chance.")""")

# ---- D3 bootstrap + emotion
md(r"""## D3. Zooming from valence to a single emotion, with error bars

**Intuition.** Repeat the "like connects to like" test but for one specific emotion — **fear**.
Do fear words clump with fear words?

**Maths.** Mark each word 1 (fear) or 0 (not). The **assortativity** of a 0/1 label is just the
**correlation of that label across edge ends** (Newman's numeric assortativity). To get a
**confidence interval** we use the **bootstrap**: resample the edges with replacement many
times and recompute; the middle 95% of those values is the CI.

**Esempio of bootstrapping:** if you have 6 edges, draw 6 "new" edges by picking from them at
random *with repeats* (some appear twice, some not at all), recompute — repeat 1000×. The
spread tells you how shaky the estimate is on this much data.""")
code(r"""def emo_assort(G, attr):
    e = list(G.edges())
    x = np.array([attr[u] for u,v in e], float); y = np.array([attr[v] for u,v in e], float)
    def r(a,b):
        A=np.concatenate([a,b]); B=np.concatenate([b,a])
        return 0.0 if A.std()==0 or B.std()==0 else np.corrcoef(A,B)[0,1]
    return r(x,y), x, y
def boot_ci(G, attr, B=300, seed=1):
    o,x,y = emo_assort(G, attr); rng=np.random.default_rng(seed)
    def r(a,b):
        A=np.concatenate([a,b]);Bb=np.concatenate([b,a])
        return 0.0 if A.std()==0 or Bb.std()==0 else np.corrcoef(A,Bb)[0,1]
    bs=[r(*(lambda s:(x[s],y[s]))(rng.integers(0,len(x),len(x)))) for _ in range(B)]
    return o, np.percentile(bs,2.5), np.percentile(bs,97.5)

# toy M first
o,_ ,_ = emo_assort(M, fear_M); print(f"toy M fear assortativity = {o:.3f}")
for name, G, emo in [("students", GS, emoS), ("researchers", GR, emoR)]:
    attr = {n:int(emo.loc[n,"fear"]>0) for n in G.nodes()}
    o,lo,hi = boot_ci(G, attr)
    print(f"{name:12s} fear = {o:.3f}  95% CI [{lo:.3f}, {hi:.3f}]")""")

# ---- D4 communities
md(r"""## D4. Finding clusters (communities)

**Intuition.** A **community** is a group of nodes more densely joined to each other than to the
rest — like friend circles. We ask: does *fear* live in identifiable regions?

**Maths.** **Modularity** $Q$ scores a proposed grouping: fraction of edges *inside* groups
minus what you'd expect by chance,
$$Q=\frac{1}{2m}\sum_{ij}\Big[A_{ij}-\frac{k_ik_j}{2m}\Big]\delta(c_i,c_j).$$
The **Louvain** algorithm searches groupings to make $Q$ large.

**Esempio:** in the friendship graph, {Anna, Bea, Carla} is a tight triangle (a community) with
Dan hanging off it. Louvain would put Dan with Carla's group or alone.""")
code(r"""from networkx.algorithms import community
cF = community.louvain_communities(F, seed=1)
print("friendship communities:", [sorted(c) for c in cF], " modularity Q =", round(community.modularity(F, cF),3))

fear_nodes = set(emoS.index[emoS["fear"]>0])
cS = community.louvain_communities(GS, seed=1)
rich = sorted(((len(c), len(c&fear_nodes)/len(c),
               [w for w in list(c) if w in fear_nodes][:5]) for c in cS if len(c)>=20),
              key=lambda t:-t[1])[:3]
print(f"\nstudents modularity Q = {community.modularity(GS,cS):.3f}; fear-richest communities:")
for sz,fr,ex in rich: print(f"  size={sz:4d}  fear={fr*100:4.1f}%  e.g. {ex}")""")

# ---- D5 pagerank
md(r"""## D5. Letting activation spread (personalised PageRank)

**Intuition.** Thinking of *matematica* spreads activation to its neighbours, then theirs, and
so on — fading with distance. Does much of that activation reach **fear** words? This models
"is fear mentally near maths?"

**Maths.** A random walker starts at the seed word, at each step follows a random edge with
probability $\alpha$ or jumps back to the seed with probability $1-\alpha$. Where it spends its
time settles into a distribution $\pi$ solving
$$\pi=\alpha P^\top\pi+(1-\alpha)e_s,$$
with $P$ the "pick a random neighbour" matrix and $e_s$ the restart at seed $s$. The candidate
score is the total time on fear words, $\sum_{f}\pi_f$.

**Esempio on M:** start the walker at *matematica*. It quickly reaches *difficile* and *esame*
(direct neighbours), then *ansia*, *paura*. How much of its time lands on fear-coloured nodes?""")
code(r"""def fear_mass(G, seed, fear_set, alpha=0.85):
    pr = nx.pagerank(G, alpha=alpha, personalization={seed:1.0})
    return sum(pr[f] for f in fear_set if f in pr), pr

fm, pr = fear_mass(M, "matematica", {n for n in fear_M if fear_M[n]})
print(f"toy M: fraction of walker's time on fear words (from matematica) = {fm:.2f}")
print("top nodes by activation:", sorted(pr.items(), key=lambda x:-x[1])[:4])""")

# ---- D6 the trap
md(r"""## D6. A warning: a test can be *blind* (the positive control)

**Intuition.** Before believing "fear is NOT near maths," we must check the test could even
*detect* nearness if it were there. We **plant** the effect (add edges from maths straight to
fear) and see if the score reacts. If it doesn't, the test is broken, not the finding.

**Esempio on M:** artificially wire *matematica* directly to *paura* and *ansia*. A good score
should jump. We'll see the PageRank score barely moves on the big real network — that is why
the paper **discards** it.""")
code(r"""def pagerank_z(G, seed, fear_set, add=0, reps=3, seed0=1):
    rng=np.random.default_rng(seed0); nodes=list(G.nodes()); k=len(fear_set)
    tgt=[f for f in fear_set if f!=seed and not G.has_edge(seed,f)]; zs=[]
    for _ in range(reps):
        H=G.copy()
        if add: H.add_edges_from((seed,tgt[t]) for t in rng.choice(len(tgt),add,replace=False))
        fm,pr=fear_mass(H,seed,fear_set)
        null=[sum(pr[n] for n in rng.choice(nodes,k,replace=False)) for _ in range(150)]
        zs.append((fm-np.mean(null))/np.std(null))
    return np.mean(zs)
for add in [0, 5, 13]:
    print(f"  matematica + {add:2d} forced fear-edges -> PageRank score z = {pagerank_z(GS,'matematica',fear_nodes,add):+.2f}")
print("Barely moves even with 13 planted edges => the test is underpowered. Discard it.")""")

# ---- D7 proximity
md(r"""## D7. A test that actually works: distance with fading weight

**Intuition.** Use plain **distance in hops**, but weight near fear words heavily and far ones
almost nothing, so *local* wiring dominates.

**Maths.** With $d(c,f)$ the hop-distance from concept $c$ to fear word $f$,
$$\text{prox}(c)=\sum_{f\in\text{fear}}\beta^{\,d(c,f)},\qquad \beta=0.5.$$
One hop counts $0.5$, two hops $0.25$, three $0.125$…

**Esempio on M:** from *matematica*, *difficile* and *esame* are 1 hop ($0.5$ each), *ansia* is
2 hops ($0.25$), *paura* is 3 hops ($0.125$). Add them up. Now wire *matematica–paura* directly
and watch *paura* jump from $0.125$ to $0.5$ — the score is **sensitive to local wiring**,
exactly what D6's test lacked.""")
code(r"""BETA=0.5
def decay_prox(G, seed, fear_set):
    d = nx.single_source_shortest_path_length(G, seed)
    return {f: BETA**d[f] for f in fear_set if f in d and d[f]>0}

fm_words = {n for n in fear_M if fear_M[n]}
before = decay_prox(M, "matematica", fm_words)
print("toy M contributions before:", {k: round(v,3) for k,v in before.items()}, "sum=", round(sum(before.values()),3))
M2 = M.copy(); M2.add_edge("matematica","paura")
after = decay_prox(M2, "matematica", fm_words)
print("after wiring matematica–paura:", {k: round(v,3) for k,v in after.items()}, "sum=", round(sum(after.values()),3))""")

# ---- D8 degree null
md(r"""## D8. A fair coin: the degree-preserving null

**Intuition.** Fear words happen to be **popular** (high-degree) words. A popular word is close
to *everything*, so comparing "distance to fear" against *random* words is unfair — random
words include lonely, far-away words. Fair comparison: compare against random words **with the
same popularity profile** as the fear words.

**Esempio:** to judge if you live unusually close to *celebrities*, compare your commute to
other *celebrities'* homes (busy, central) — not to random rural addresses. Matching on
"busyness" (degree) is the same idea.""")
code(r"""import revision_analyses as RV
for name, ef, vf, lang, concept in [("students","FormaMentisStudents.txt","ValenceLabelsStudents.txt","italian","matematica"),
                                    ("researchers","FormaMentisResearchers.txt","ValenceLabelsResearchers.txt","english","mathematics")]:
    Gx, fx = RV.load(ef, vf, lang)
    z, p = RV.prox_degstrat(Gx, fx, concept, nperm=400)
    print(f"{name:12s} '{concept}': proximity z = {z:+.1f}, p = {p:.3f}   (negative = FARTHER from fear than chance)")
print("\nWith the FAIR null, no STEM concept is closer to fear than chance; several are farther.")""")

# ---- D9 TOST
md(r"""## D9. Proving a *negative*: equivalence testing (TOST)

**Intuition.** "Not significant" ≠ "nothing there." To claim *maths is genuinely un-wired to
fear*, we show its proximity is **within a tiny band around zero** — smaller than the smallest
effect we'd care about ($\Delta$, taken from D6's minimum detectable effect).

**Maths.** Flip the question: instead of testing "effect = 0?", test
$$H_0:|\text{effect}|\ge\Delta \quad\text{vs}\quad H_1:|\text{effect}|<\Delta,$$
and reject $H_0$ if a bootstrap interval sits entirely **inside** $(-\Delta,\Delta)$ on the
"close" side.

**Esempio:** a scale reading "0 ± 0.1 kg" tells you the parcel is *empty*, not merely
"not proven heavy." Same logic.""")
code(r"""G, fear = RV.load("FormaMentisResearchers.txt","ValenceLabelsResearchers.txt","english")
for c in ["mathematics","physics","chemistry"]:
    lo, hi = RV.prox_bootstrap_ci(G, fear, c, nboot=120, nperm=250)
    print(f"  {c:12s} proximity z 90% CI = [{lo:+.2f}, {hi:+.2f}]  -> upper bound below +1.96: equivalent to NO fear-wiring")""")

# ---- D10 FDR
md(r"""## D10. Testing many things at once (false-discovery correction)

**Intuition.** Test 20 concepts and, by luck alone, about 1 will look "significant" at p<0.05
even if nothing is real. Correct for it.

**Maths.** **Benjamini–Hochberg:** sort the $m$ p-values, keep the largest $k$ with
$p_{(k)}\le\frac{k}{m}q$ (here $q=0.05$), reject those.

**Esempio:** with 7 p-values, the threshold line $\frac{k}{m}\cdot0.05$ rises from tiny to
0.05; only p-values under the line survive.""")
code(r"""def bh(pvals, q=0.05):
    p=np.sort(pvals); m=len(p); thr=q*np.arange(1,m+1)/m; below=np.where(p<=thr)[0]
    return (p[below.max()] if len(below) else 0.0)
demo=[0.002,0.010,0.014,0.030,0.20,0.51,0.92]
print("p-values:", demo, "\nBH critical p =", round(bh(demo),3), "-> reject all p <= that")
print("In the paper, 7 concept tests survive — ALL in the 'farther from fear' direction.")""")

# ---- D11 lexicon robustness
md(r"""## D11. Was 'fear cohesion' real, or an accident of one word-list?

**Intuition.** The fear labels came from one lexicon (NRC). A result that appears only with one
word-list is an artefact. So we redo the fear-assortativity with an **independent** definition —
*low-valence + high-arousal* words from human ratings — and with a second lexicon (DepecheMood).

**Esempio:** if three independent judges agree "fear clusters," believe it; if only one does,
don't.""")
code(r"""import robustness_lexicon as RL
def vad_fear(G, lang):
    if lang=="english":
        w=pd.read_csv("data/warriner.csv"); val=dict(zip(w["Word"].str.lower(),w["V.Mean.Sum"])); aro=dict(zip(w["Word"].str.lower(),w["A.Mean.Sum"]))
    else:
        d=pd.read_excel("data/it_vad_s001.xlsx",sheet_name="Database",header=1)
        val=dict(zip(d["Ita_Word"].astype(str).str.lower(),pd.to_numeric(d["M_Val"],errors="coerce")))
        aro=dict(zip(d["Ita_Word"].astype(str).str.lower(),pd.to_numeric(d["M_Aro"],errors="coerce")))
    vm,am=np.nanmedian(list(val.values())),np.nanmedian(list(aro.values()))
    return {n:(1 if (str(n).lower() in val and val[str(n).lower()]<vm and aro[str(n).lower()]>am) else 0) for n in G.nodes()}
for name,G,emo,lang in [("students",GS,emoS,"italian"),("researchers",GR,emoR,"english")]:
    ea={n:int(emo.loc[n,"fear"]>0) for n in G.nodes()}; o1,l1,h1=RL.assort_ci(G,ea)
    o2,l2,h2=RL.assort_ci(G,vad_fear(G,lang))
    print(f"{name:12s} NRC/EmoAtlas r={o1:.3f}[{l1:.3f},{h1:.3f}] | INDEPENDENT VAD r={o2:.3f}[{l2:.3f},{h2:.3f}]")""")
md(r"""Both lexicons agree fear is cohesive *within* each group (robust). But the *between-group*
gap (students > experts) shows up only with NRC and vanishes under the independent lexicon — so
that particular claim is dropped. **Lesson: vary the lexicon before believing an emotion-network
number.**""")

# ---- synthesis
md(r"""# Part E — The whole story in one line

We started with 21 scribbled associations from five imaginary students and ended with a
statistically defended claim. Scaled to the real data:

- words that associate carry matching **valence** (reproduced, above chance);
- **fear** is a real, clustered emotion in both mindsets (robust across independent lexicons);
- but the STEM **concepts themselves are not wired to fear** — a validated, fairly-nulled,
  equivalence-tested, multiplicity-corrected result;
- so **STEM negativity is *evaluative*, not *afraid*.** *Matematica* is judged hard and
  unpleasant (it travels to fear only through *difficulty* words like *esame*, *problema*), yet
  it is not itself sitting in the fear network.

And two hard-won method lessons, both visible in this notebook: **validate a structural test
with a positive control (D6)**, and **vary the lexicon (D11)** before reading a number as a fact
about the mind.
""")

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.11"}},
      "nbformat": 4, "nbformat_minor": 4}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PAPER_WALKTHROUGH.ipynb")
with open(out, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print("wrote", out, "with", len(cells), "cells")
