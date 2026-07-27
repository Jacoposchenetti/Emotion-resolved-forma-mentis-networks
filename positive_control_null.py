"""
Positive control for the spreading-activation null (Result 3.5).
Question a reviewer will ask: "is the null result just low power?"
We show the test DETECTS embedding when it exists, two ways:

(A) Seed-in-region control: seed PR on words that ARE in the fear module
    (fear-labelled, excluded from the fear-mass sum) -> z should be strongly +.
(B) Dose-response injection: start from a real STEM concept, add j synthetic
    edges to random fear nodes, recompute fear-mass z. z must cross 1.96 at
    small j -> the observed z~0 for real STEM concepts is a true absence,
    not insufficient power.

Uses the EmoAtlas fear labels (the labels behind the main null claim).
"""
import os, numpy as np, pandas as pd, networkx as nx, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
import reproduce_stem_fmn as R, fear_module_analysis as F
OUT = F.OUT


def load(ef, vf, lang):
    G = R.build(ef, vf)
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0)
    emo = emo.reindex(list(G.nodes())).fillna(0).astype(int)
    fear = [n for n in G.nodes() if emo.loc[n, "fear"] > 0]
    return G, set(fear)


def fear_mass_z(G, fearset, seed_word, n_perm=1000, rng=None, exclude_seed=False):
    rng = rng or np.random.default_rng(0)
    nodes = list(G.nodes())
    pr = nx.pagerank(G, alpha=0.85, personalization={seed_word: 1.0})
    fnodes = [f for f in fearset if not (exclude_seed and f == seed_word)]
    n_fear = len(fnodes)
    pr_arr = np.array([pr[n] for n in nodes])
    obs = sum(pr[f] for f in fnodes)
    null = np.array([pr_arr[rng.choice(len(nodes), n_fear, replace=False)].sum()
                     for _ in range(n_perm)])
    return (obs - null.mean()) / null.std() if null.std() > 0 else np.nan


def control_A(G, fearset, k=8, seed=42):
    """Seed on high-degree fear words (self excluded from mass)."""
    rng = np.random.default_rng(seed)
    deg = dict(G.degree())
    fear_hubs = sorted(fearset, key=lambda w: -deg[w])[:k]
    zs = [(w, fear_mass_z(G, fearset, w, rng=rng, exclude_seed=True)) for w in fear_hubs]
    return zs


def control_B(G, fearset, concept, js=(0, 1, 2, 3, 5, 8, 13), reps=8, seed=42):
    """Dose-response: inject j edges concept->random fear nodes."""
    rng = np.random.default_rng(seed)
    fear_list = [f for f in fearset if f != concept and not G.has_edge(concept, f)]
    curve = []
    for j in js:
        zvals = []
        for _ in range(reps if j > 0 else 1):
            H = G.copy()
            if j > 0:
                targets = rng.choice(len(fear_list), size=min(j, len(fear_list)), replace=False)
                H.add_edges_from((concept, fear_list[t]) for t in targets)
            zvals.append(fear_mass_z(H, fearset, concept, n_perm=500,
                                     rng=np.random.default_rng(int(rng.integers(1e9)))))
        curve.append((j, np.mean(zvals), np.std(zvals)))
    return curve


def run(name, ef, vf, lang, concept):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    G, fearset = load(ef, vf, lang)
    print(f"fear nodes: {len(fearset)}")
    print("(A) seed-in-fear-region control (z should be strongly positive):")
    for w, z in control_A(G, fearset):
        print(f"     seed='{w}'  fear-mass z = {z:+.1f}")
    print(f"(B) dose-response injection from '{concept}':")
    curve = control_B(G, fearset, concept)
    crossed = None
    for j, m, s in curve:
        flag = "  <-- crosses 1.96" if m > 1.96 and crossed is None else ""
        if m > 1.96 and crossed is None:
            crossed = j
        print(f"     +{j:2d} edges: z = {m:+5.1f} ± {s:.1f}{flag}")
    print(f"     -> smallest injection detected as significant: j={crossed}")
    return concept, curve, crossed


if __name__ == "__main__":
    c1, cur1, cr1 = run("STUDENTS", "FormaMentisStudents.txt",
                        "ValenceLabelsStudents.txt", "italian", "matematica")
    c2, cur2, cr2 = run("RESEARCHERS", "FormaMentisResearchers.txt",
                        "ValenceLabelsResearchers.txt", "english", "mathematics")
    # figure
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    for (c, cur, col) in [(c1, cur1, "#c44"), (c2, cur2, "#48c")]:
        js = [j for j, _, _ in cur]; ms = [m for _, m, _ in cur]; ss = [s for _, _, s in cur]
        ax.errorbar(js, ms, yerr=ss, marker="o", capsize=3, color=col, label=f"seed = {c}")
    ax.axhspan(-1.96, 1.96, color="0.88", label="n.s. band")
    ax.axhline(0, color="k", lw=.6)
    ax.set_xlabel("synthetic edges injected from STEM concept to fear nodes")
    ax.set_ylabel("fear-reachability z")
    ax.set_title("Positive control: the spreading test detects fear-embedding at small doses\n"
                 "(real STEM concepts sit at j=0, z≈0 → the null is a true absence, not low power)")
    ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(os.path.join(OUT, "positive_control_dose_response.png"), dpi=150)
    print("\nsaved positive_control_dose_response.png")
