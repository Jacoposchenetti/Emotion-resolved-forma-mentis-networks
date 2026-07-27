"""
Robustness check #1 — do the two headline results survive an INDEPENDENT emotion
lexicon? EmoAtlas labels derive from NRC (Mohammad & Turney, 2013). DepecheMood++
(Araque et al.) is built by a different method (mood-voting over news) and has a
fear-like category: AFRAID (English) / PREOCCUPATO (Italian). We relabel each
node's "fear" indicator from DepecheMood and re-run:
  (a) fear assortativity + bootstrap 95% CI, both groups  -> does students>experts hold?
  (b) spreading-activation fear null for STEM concepts     -> is it still n.s.?
Also reports coverage and concordance (Jaccard) with the EmoAtlas fear labels.
"""
import os, numpy as np, pandas as pd, networkx as nx
import reproduce_stem_fmn as R, fear_module_analysis as F

DATA = os.path.join(os.path.dirname(__file__), "data")
OUT = F.OUT
FEAR_COL = {"english": "AFRAID", "italian": "PREOCCUPATO"}


def load_depeche_fear(lang):
    df = pd.read_csv(os.path.join(DATA, f"depeche_{lang}.tsv"), sep="\t", index_col=0)
    cats = [c for c in df.columns if c != "freq"]
    fear = FEAR_COL[lang]
    argmax = df[cats].idxmax(axis=1)
    is_fear = (argmax == fear)                       # word's dominant mood is fear-like
    return set(str(w).lower() for w in df.index[is_fear]), set(str(w).lower() for w in df.index)


def dm_fear_attr(G, lang):
    fearset, vocab = load_depeche_fear(lang)
    attr, covered = {}, 0
    for n in G.nodes():
        w = str(n).lower()
        if w in vocab:
            covered += 1
        attr[n] = 1 if w in fearset else 0
    return attr, covered / G.number_of_nodes()


def assort_ci(G, attr, B=500, seed=42):
    edges = list(G.edges())
    x = np.array([attr[u] for u, v in edges], float)
    y = np.array([attr[v] for u, v in edges], float)
    def a(xx, yy):
        X = np.concatenate([xx, yy]); Y = np.concatenate([yy, xx])
        return 0.0 if X.std() == 0 or Y.std() == 0 else np.corrcoef(X, Y)[0, 1]
    obs = a(x, y)
    rng = np.random.default_rng(seed)
    bt = np.array([a(*(lambda s: (x[s], y[s]))(rng.integers(0, len(edges), len(edges))))
                   for _ in range(B)])
    return obs, np.percentile(bt, 2.5), np.percentile(bt, 97.5)


def spreading_fear_dm(G, attr, concepts, n_perm=1000, seed=42):
    fear_nodes = [n for n in G.nodes() if attr[n] == 1]
    n_fear = len(fear_nodes)
    nodes = list(G.nodes())
    rng = np.random.default_rng(seed)
    out = {}
    for w in concepts:
        if w not in G:
            continue
        pr = nx.pagerank(G, alpha=0.85, personalization={w: 1.0})
        pr_arr = np.array([pr[n] for n in nodes])
        obs = sum(pr[f] for f in fear_nodes)
        null = np.array([pr_arr[rng.choice(len(nodes), n_fear, replace=False)].sum()
                         for _ in range(n_perm)])
        z = (obs - null.mean()) / null.std() if null.std() > 0 else np.nan
        out[w] = z
    return out


def concordance(G, dm_attr, lang):
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0)
    emo = emo.reindex(list(G.nodes())).fillna(0)
    emo_fear = set(emo.index[emo["fear"] > 0])
    dm_fear = set(n for n in G.nodes() if dm_attr[n] == 1)
    inter = len(emo_fear & dm_fear); union = len(emo_fear | dm_fear)
    return len(emo_fear), len(dm_fear), inter, (inter / union if union else 0)


def run(name, ef, vf, lang, concepts):
    print(f"\n{'='*64}\n{name}  (DepecheMood fear = {FEAR_COL[lang]})\n{'='*64}")
    G = R.build(ef, vf)
    attr, cov = dm_fear_attr(G, lang)
    nfear = sum(attr.values())
    print(f"DepecheMood coverage of nodes: {100*cov:.0f}%   DM-fear nodes: {nfear} "
          f"({100*nfear/G.number_of_nodes():.1f}%)")
    ne, nd, inter, jac = concordance(G, attr, lang)
    print(f"concordance with EmoAtlas fear: EmoAtlas={ne}, DM={nd}, shared={inter}, Jaccard={jac:.2f}")
    obs, lo, hi = assort_ci(G, attr)
    print(f"(a) DM-fear assortativity r = {obs:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]")
    z = spreading_fear_dm(G, attr, concepts)
    hard = [c for c in ["matematica", "fisica", "chimica", "mathematics", "physics", "chemistry"] if c in z]
    print(f"(b) spreading fear-z (hard science): " +
          ", ".join(f"{c}={z[c]:+.1f}" for c in hard))
    allsig = [c for c in z if abs(z[c]) > 1.96]
    print(f"    significant STEM concepts (|z|>1.96): {allsig if allsig else 'NONE'}")
    return (obs, lo, hi)


if __name__ == "__main__":
    s = run("STUDENTS", "FormaMentisStudents.txt", "ValenceLabelsStudents.txt",
            "italian", F.STEM_IT)
    r = run("RESEARCHERS", "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt",
            "english", F.STEM_EN)
    print(f"\n{'='*64}\nHEADLINE ROBUSTNESS (DepecheMood, independent of NRC/EmoAtlas)\n{'='*64}")
    print(f"fear assortativity: Students {s[0]:+.3f}[{s[1]:+.3f},{s[2]:+.3f}]  vs  "
          f"Researchers {r[0]:+.3f}[{r[1]:+.3f},{r[2]:+.3f}]")
    print("students>experts replicates" if s[1] > r[2] else
          "CIs overlap -> group difference NOT replicated with DepecheMood")
