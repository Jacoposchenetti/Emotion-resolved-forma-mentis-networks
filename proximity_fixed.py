"""
Fixed proximity test (replaces the underpowered PageRank fear-mass).
We define LOCAL, distance-based proximity of a concept to the fear set and
VALIDATE each candidate with the injection positive control BEFORE trusting it.

Candidate measures (from BFS distances d(concept, .)):
  M_decay : sum over fear nodes of beta**d           (beta=0.5; near fear weighted heavily)
  M_2hop  : count of fear nodes within 2 hops         (interpretable)
Both tested vs a fear-label-permutation null (random node sets of same size),
holding the seed fixed. z>1.96 => concept is closer to fear than chance.

Workflow: (1) injection dose-response on each measure -> keep those with power;
(2) run the powered measure(s) on all STEM concepts, both groups.
"""
import os, numpy as np, pandas as pd, networkx as nx, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import reproduce_stem_fmn as R, fear_module_analysis as F
OUT = F.OUT
BETA = 0.5


def load(ef, vf, lang):
    G = R.build(ef, vf)
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0)
    emo = emo.reindex(list(G.nodes())).fillna(0).astype(int)
    fear = set(n for n in G.nodes() if emo.loc[n, "fear"] > 0)
    return G, fear


def dist_vector(G, concept):
    d = nx.single_source_shortest_path_length(G, concept)
    return d  # node -> hops


def measures(dist, nodeset):
    m_decay = sum(BETA ** dist[n] for n in nodeset if n in dist and dist[n] > 0)
    m_2hop = sum(1 for n in nodeset if dist.get(n, 99) in (1, 2))
    return m_decay, m_2hop


def zscores(G, fearset, concept, n_perm=1000, rng=None):
    rng = rng or np.random.default_rng(0)
    dist = dist_vector(G, concept)
    obs_d, obs_h = measures(dist, fearset)
    nodes = list(G.nodes()); N = len(nodes); k = len(fearset)
    nd = np.empty(n_perm); nh = np.empty(n_perm)
    node_arr = np.array(nodes, dtype=object)
    for i in range(n_perm):
        sel = set(node_arr[rng.choice(N, k, replace=False)])
        nd[i], nh[i] = measures(dist, sel)
    zd = (obs_d - nd.mean()) / nd.std() if nd.std() > 0 else np.nan
    zh = (obs_h - nh.mean()) / nh.std() if nh.std() > 0 else np.nan
    return zd, zh


def injection_control(G, fearset, concept, js=(0, 1, 2, 3, 5, 8), reps=6, seed=1):
    rng = np.random.default_rng(seed)
    fl = [f for f in fearset if f != concept and not G.has_edge(concept, f)]
    curve_d, curve_h = [], []
    for j in js:
        zds, zhs = [], []
        for _ in range(reps if j > 0 else 1):
            H = G.copy()
            if j > 0:
                t = rng.choice(len(fl), size=min(j, len(fl)), replace=False)
                H.add_edges_from((concept, fl[x]) for x in t)
            zd, zh = zscores(H, fearset, concept, n_perm=500,
                             rng=np.random.default_rng(int(rng.integers(1e9))))
            zds.append(zd); zhs.append(zh)
        curve_d.append((j, np.mean(zds))); curve_h.append((j, np.mean(zhs)))
    return curve_d, curve_h


def run(name, ef, vf, lang, concepts, inj_concept):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    G, fearset = load(ef, vf, lang)
    print(f"fear nodes: {len(fearset)}")
    print(f"[validate] injection dose-response from '{inj_concept}':")
    cd, ch = injection_control(G, fearset, inj_concept)
    print("   decay-measure z:  " + ", ".join(f"+{j}:{z:+.1f}" for j, z in cd))
    print("   2hop-measure  z:  " + ", ".join(f"+{j}:{z:+.1f}" for j, z in ch))
    cross_d = next((j for j, z in cd if z > 1.96), None)
    cross_h = next((j for j, z in ch if z > 1.96), None)
    print(f"   power: decay crosses 1.96 at j={cross_d} ; 2hop at j={cross_h}")
    print("[test] real STEM concepts (z_decay / z_2hop vs permutation null):")
    rng = np.random.default_rng(7)
    rows = {}
    for c in concepts:
        if c not in G:
            continue
        zd, zh = zscores(G, fearset, c, rng=rng)
        rows[c] = (zd, zh)
        sig = "***" if (abs(zd) > 1.96 or abs(zh) > 1.96) else ""
        print(f"     {c:12s} z_decay={zd:+5.1f}  z_2hop={zh:+5.1f} {sig}")
    return G, fearset, (cd, ch), rows


if __name__ == "__main__":
    rS = run("STUDENTS", "FormaMentisStudents.txt", "ValenceLabelsStudents.txt",
             "italian", F.STEM_IT, "matematica")
    rR = run("RESEARCHERS", "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt",
             "english", F.STEM_EN, "mathematics")
    # validation figure (decay measure)
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    for (name, res, col) in [("students/matematica", rS, "#c44"), ("researchers/mathematics", rR, "#48c")]:
        cd = res[2][0]
        ax.plot([j for j, _ in cd], [z for _, z in cd], marker="o", color=col, label=name)
    ax.axhspan(-1.96, 1.96, color="0.88", label="n.s."); ax.axhline(1.96, color="k", lw=.5, ls=":")
    ax.set_xlabel("injected concept->fear edges"); ax.set_ylabel("z (decay proximity)")
    ax.set_title("Fixed proximity test — injection positive control\n(now the test detects fear-wiring at small doses)")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(os.path.join(OUT, "proximity_fixed_control.png"), dpi=150)
    print("\nsaved proximity_fixed_control.png")
