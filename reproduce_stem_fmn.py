"""
Reproduction of the core analyses in:
  Stella, De Nigris, Aloric & Siew (2019),
  "Forma mentis networks quantify crucial differences in STEM perception
   between students and experts", PLOS ONE 14(10): e0222870.
Data: OSF xyfwg (ComplexFormaMentis.zip).

Reproduces, independently from the paper's own code:
  (A) Network sizes (nodes/edges)
  (B) Link-level valence assortativity  (Kendall tau, symmetrized over edges)
  (C) Neighborhood-level valence clustering (node valence vs mean-neighbor valence)
  (D) Degree-preserving null models for (B) and (C), 50 realizations
  (E) Word-level negativity: fraction of an item's associates that are Negative
"""
import os, sys, collections, numpy as np, networkx as nx
from scipy.stats import kendalltau

DATA = os.path.join(os.path.dirname(__file__), "data", "stem")
VAL_MAP = {"Positive": 1.0, "Negative": -1.0, "Neutral": 0.0}
SEED = 42
N_NULL = 50

def load_edges(fn):
    E = []
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            p = line.split("\t")
            if len(p) >= 2 and p[0].strip() and p[1].strip():
                E.append((p[0].strip(), p[1].strip()))
    return E

def load_valence(fn):
    d = {}
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            p = line.split("\t")
            if len(p) >= 2 and p[0].strip():
                d[p[0].strip()] = p[1].strip()
    return d

def build(edges_fn, val_fn):
    E = load_edges(edges_fn)
    V = load_valence(val_fn)
    G = nx.Graph()
    G.add_edges_from(E)
    # numeric valence as node attribute; missing -> Neutral(0)
    num = {n: VAL_MAP.get(V.get(n, "Neutral"), 0.0) for n in G.nodes()}
    nx.set_node_attributes(G, num, "val")
    nx.set_node_attributes(G, {n: V.get(n, "Neutral") for n in G.nodes()}, "vlabel")
    return G

def link_assortativity(G):
    """Symmetrized Kendall tau of endpoint valences over all edges."""
    val = nx.get_node_attributes(G, "val")
    X, Y = [], []
    for u, v in G.edges():
        X.append(val[u]); Y.append(val[v])
        X.append(val[v]); Y.append(val[u])  # symmetrize
    tau, p = kendalltau(X, Y)
    return tau, p

def neighbor_clustering(G, only_valenced_center=True):
    """Kendall tau between a node's valence and mean valence of its neighbors.
    Paper restricts the correlation to valenced (non-neutral) center words."""
    val = nx.get_node_attributes(G, "val")
    X, Y = [], []
    for n in G.nodes():
        if only_valenced_center and val[n] == 0:
            continue
        nbrs = list(G.neighbors(n))
        if not nbrs:
            continue
        X.append(val[n])
        Y.append(np.mean([val[m] for m in nbrs]))
    tau, p = kendalltau(X, Y)
    return tau, p

def null_distribution(G, func, n=N_NULL, seed=SEED):
    """Degree-preserving double-edge-swap null; valence stays fixed on nodes."""
    rng = np.random.default_rng(seed)
    E = G.number_of_edges()
    taus = []
    for i in range(n):
        H = G.copy()
        # ~10 swaps per edge for good mixing
        try:
            nx.double_edge_swap(H, nswap=10 * E, max_tries=100 * E,
                                seed=int(rng.integers(0, 1_000_000)))
        except nx.NetworkXError:
            pass  # not enough swaps possible; use what we got
        taus.append(func(H)[0])
    taus = np.array(taus)
    return taus.mean(), taus.std(), taus

def word_negativity(G, word):
    if word not in G:
        return None
    lbl = nx.get_node_attributes(G, "vlabel")
    nbrs = list(G.neighbors(word))
    c = collections.Counter(lbl[m] for m in nbrs)
    tot = len(nbrs)
    return tot, c, {k: round(100 * c.get(k, 0) / tot, 1) for k in ("Positive", "Negative", "Neutral")}

def analyze(name, edges_fn, val_fn, targets):
    G = build(edges_fn, val_fn)
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    print(f"(A) nodes={G.number_of_nodes()}  edges={G.number_of_edges()}  "
          f"[paper nodes={targets['nodes']}]")
    vc = collections.Counter(nx.get_node_attributes(G, 'vlabel').values())
    print(f"    valence counts: {dict(vc)}")

    tau_l, p_l = link_assortativity(G)
    print(f"(B) link-level valence assortativity  Kendall tau = {tau_l:.4f}  "
          f"(p={p_l:.1e})   [paper tau={targets['link']}]")

    tau_n, p_n = neighbor_clustering(G)
    print(f"(C) neighborhood valence clustering   Kendall tau = {tau_n:.4f}  "
          f"(p={p_n:.1e})   [paper tau={targets['neigh']}]")

    print(f"(D) null models ({N_NULL} degree-preserving realizations)...")
    m_l, s_l, _ = null_distribution(G, link_assortativity)
    m_n, s_n, _ = null_distribution(G, neighbor_clustering)
    z_l = (tau_l - m_l) / s_l if s_l > 0 else float('inf')
    z_n = (tau_n - m_n) / s_n if s_n > 0 else float('inf')
    print(f"    link-level null  tau_r = {m_l:+.4f} +/- {s_l:.4f}  (z={z_l:.1f})   "
          f"[paper tau_r={targets['link_null']}]")
    print(f"    neigh-level null tau_r = {m_n:+.4f} +/- {s_n:.4f}  (z={z_n:.1f})   "
          f"[paper tau_r={targets['neigh_null']}]")

    if targets.get('word'):
        w = targets['word']
        r = word_negativity(G, w)
        if r:
            tot, c, pct = r
            print(f"(E) '{w}': {tot} associates -> {pct}%  "
                  f"[paper: ~{targets['word_pct']}% negative]")
    return G

if __name__ == "__main__":
    analyze("STUDENTS (Italian high-schoolers)",
            "FormaMentisStudents.txt", "ValenceLabelsStudents.txt",
            dict(nodes=4483, link="0.163", neigh="0.385",
                 link_null="-0.0001", neigh_null="0.053",
                 word="matematica", word_pct=43))
    analyze("RESEARCHERS (international experts)",
            "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt",
            dict(nodes=1616, link="0.116", neigh="0.323",
                 link_null="n/r", neigh_null="0.060",
                 word="mathematics", word_pct=None))
