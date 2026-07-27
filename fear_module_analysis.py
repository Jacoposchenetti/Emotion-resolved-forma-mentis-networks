"""
A.1 follow-up — formalising the "fear module", bridge words, and statistics.

(1) Community detection (Louvain) -> locate the fear-rich module; measure how
    reachable fear is from each STEM concept via spreading activation
    (personalised PageRank) against a fear-label permutation null (controls for
    the seed word's own centrality: PR is fixed, only which nodes are 'fear'
    is shuffled).
(2) Bridge words: the 1-hop gateways lying on shortest paths from STEM concepts
    to nearby fear words -> intervention targets.
(3) Statistics: permutation test on the students-vs-experts emotion prevalence
    difference (with explicit language caveat) + bootstrap CI on fear
    assortativity per network.
"""
import os, numpy as np, networkx as nx, pandas as pd, collections
from networkx.algorithms import community
import reproduce_stem_fmn as R

EMOS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
OUT = os.path.join(os.path.dirname(__file__), "results_A1")
SEED = 42
STEM_IT = ["scienza", "matematica", "fisica", "chimica", "biologia", "informatica",
           "statistica", "ingegneria", "tecnologia", "scienziato", "scuola", "insegnante"]
STEM_EN = ["science", "mathematics", "physics", "chemistry", "biology", "informatics",
           "statistics", "engineering", "technology", "scientist", "school", "teacher"]


def load(edges_fn, val_fn, lang):
    G = R.build(edges_fn, val_fn)
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0)
    emo = emo.reindex(list(G.nodes())).fillna(0).astype(int)
    return G, emo


# ---------- (1) fear module + spreading activation ----------
def fear_module(G, emo):
    comms = community.louvain_communities(G, seed=SEED)
    fear = set(emo.index[emo["fear"] > 0])
    rows = []
    for i, c in enumerate(comms):
        if len(c) < 10:
            continue
        nf = len(c & fear)
        rows.append((i, len(c), nf, nf / len(c)))
    rows.sort(key=lambda r: -r[3])
    return comms, rows, fear


def spreading_fear(G, emo, concepts, n_perm=1000, seed=SEED):
    fear_nodes = list(emo.index[emo["fear"] > 0])
    n_fear = len(fear_nodes)
    nodes = list(G.nodes())
    idx = {n: k for k, n in enumerate(nodes)}
    rng = np.random.default_rng(seed)
    out = {}
    for w in concepts:
        if w not in G:
            continue
        pr = nx.pagerank(G, alpha=0.85, personalization={w: 1.0})
        pr_arr = np.array([pr[n] for n in nodes])
        obs = sum(pr[f] for f in fear_nodes)
        # null: random |fear|-sized label sets, sum PR mass (seed fixed)
        null = np.array([pr_arr[rng.choice(len(nodes), n_fear, replace=False)].sum()
                         for _ in range(n_perm)])
        z = (obs - null.mean()) / null.std() if null.std() > 0 else np.nan
        p = (np.sum(null >= obs) + 1) / (n_perm + 1)
        out[w] = dict(fear_mass=obs, z=z, p=p)
    return out


# ---------- (2) bridge words ----------
def bridge_words(G, emo, concepts, max_hops=2, top=12):
    fear = set(emo.index[emo["fear"] > 0])
    overall = collections.Counter()
    per = {}
    for c in concepts:
        if c not in G:
            continue
        cnt = collections.Counter()
        # fear words reachable within max_hops
        lengths = nx.single_source_shortest_path_length(G, c, cutoff=max_hops)
        targets = [f for f in fear if f in lengths and 0 < lengths[f] <= max_hops]
        for f in targets:
            try:
                path = nx.shortest_path(G, c, f)
            except nx.NetworkXNoPath:
                continue
            if len(path) >= 3:          # bridge = first intermediate node
                cnt[path[1]] += 1
                overall[path[1]] += 1
            elif len(path) == 2:        # direct fear neighbour
                cnt["<direct>"] += 1
        per[c] = cnt.most_common(5)
    return per, overall.most_common(top)


# ---------- (3) statistics ----------
def prevalence_perm(emoS, emoR, n_perm=5000, seed=SEED):
    rng = np.random.default_rng(seed)
    a = emoS[EMOS].values.astype(float)
    b = emoR[EMOS].values.astype(float)
    obs = a.mean(0) - b.mean(0)
    pooled = np.vstack([a, b]); nA = a.shape[0]
    null = np.empty((n_perm, len(EMOS)))
    for i in range(n_perm):
        perm = rng.permutation(pooled.shape[0])
        null[i] = pooled[perm[:nA]].mean(0) - pooled[perm[nA:]].mean(0)
    p = (np.sum(np.abs(null) >= np.abs(obs), axis=0) + 1) / (n_perm + 1)
    return dict(zip(EMOS, zip(obs, p)))


def fear_assort_boot(G, emo, B=500, seed=SEED):
    """Bootstrap CI of fear numeric assortativity (endpoint-indicator corr)."""
    lab = emo["fear"].to_dict()
    edges = list(G.edges())
    x = np.array([lab[u] for u, v in edges], float)
    y = np.array([lab[v] for u, v in edges], float)
    # symmetrised Pearson correlation of endpoint indicators
    def assort(xx, yy):
        X = np.concatenate([xx, yy]); Y = np.concatenate([yy, xx])
        if X.std() == 0 or Y.std() == 0:
            return 0.0
        return np.corrcoef(X, Y)[0, 1]
    obs = assort(x, y)
    rng = np.random.default_rng(seed)
    boot = np.array([assort(*(lambda s: (x[s], y[s]))(rng.integers(0, len(edges), len(edges))))
                     for _ in range(B)])
    return obs, np.percentile(boot, 2.5), np.percentile(boot, 97.5)


def run(name, edges_fn, val_fn, lang, concepts):
    print(f"\n{'='*66}\n{name}\n{'='*66}")
    G, emo = load(edges_fn, val_fn, lang)
    comms, rows, fear = fear_module(G, emo)
    print(f"[1a] Louvain: {len(comms)} communities. Fear-richest modules (size>=10):")
    for i, sz, nf, frac in rows[:5]:
        members = [n for n in comms[i] if n in fear][:8]
        print(f"     comm#{i}: size={sz:4d}  fear={nf:3d} ({100*frac:4.1f}%)  e.g. {members}")
    print(f"     (global fear prevalence = {100*len(fear)/G.number_of_nodes():.1f}%)")

    print(f"[1b] Spreading activation -> fear reachability (PR mass on fear vs label-perm null):")
    sa = spreading_fear(G, emo, concepts)
    for w, d in sorted(sa.items(), key=lambda kv: -kv[1]["z"]):
        sig = "***" if d["p"] < 0.001 else ("**" if d["p"] < 0.01 else ("*" if d["p"] < 0.05 else ""))
        print(f"     {w:12s} z={d['z']:+5.1f}  p={d['p']:.3f} {sig}")

    print(f"[2] Bridge words (STEM concept -> fear region, top gateways):")
    per, overall = bridge_words(G, emo, concepts)
    print(f"     GLOBAL top bridges: {[(w,c) for w,c in overall]}")
    for c in ["matematica", "fisica", "chimica", "mathematics", "physics", "chemistry"]:
        if c in per and per[c]:
            print(f"       {c:12s}: {per[c]}")
    return G, emo


if __name__ == "__main__":
    GS, eS = run("STUDENTS (Italian)", "FormaMentisStudents.txt",
                 "ValenceLabelsStudents.txt", "italian", STEM_IT)
    GR, eR = run("RESEARCHERS (English)", "FormaMentisResearchers.txt",
                 "ValenceLabelsResearchers.txt", "english", STEM_EN)

    print(f"\n{'='*66}\n[3] STATISTICS\n{'='*66}")
    print("[3a] Prevalence difference (Students - Researchers), label-perm p")
    print("     ** language-confounded: groups differ in language/lexicon; read as descriptive **")
    pv = prevalence_perm(eS, eR)
    for e in EMOS:
        diff, p = pv[e]
        sig = "*" if p < 0.05 else ""
        print(f"     {e:13s} diff={100*diff:+5.1f} pp   p={p:.4f} {sig}")

    print("[3b] Fear assortativity bootstrap 95% CI (within-network, language-fair):")
    for tag, G, emo in [("Students", GS, eS), ("Researchers", GR, eR)]:
        obs, lo, hi = fear_assort_boot(G, emo)
        print(f"     {tag:12s} r_fear = {obs:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]")
