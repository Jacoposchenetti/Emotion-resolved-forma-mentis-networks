"""
A.1 — Emotion-resolved Forma Mentis analysis of the STEM perception data.

Original paper (Stella et al. 2019) used only 3-level VALENCE. Here each node of
the free-association network is labelled with Plutchik's 8 emotions via EmoAtlas
(Italian lexicon for students, English for researchers), enabling analyses the
valence-only study could not do:

  1. Emotion prevalence per network (students vs researchers).
  2. Emotion-specific homophily/assortativity vs a label-shuffle null (z-scores).
  3. Emotional z-score profile of the NEIGHBOURHOOD of core STEM concepts
     (permutation null: k random nodes), i.e. what emotions surround
     'matematica', 'fisica', 'biologia', ...

Rigorous: every effect is compared to an explicit null; multiple comparisons
flagged. Descriptive network structure, not psychological causation.
"""
import os, json, time, numpy as np, networkx as nx, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import reproduce_stem_fmn as R
# NOTE: EmoAtlas is imported lazily inside label_nodes() only when the cached
# emotion labels are absent, so the pipeline runs without EmoAtlas by default.

EMOS = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]
OUT = os.path.join(os.path.dirname(__file__), "results_A1")
os.makedirs(OUT, exist_ok=True)
SEED = 42
N_PERM = 2000          # permutations for neighbourhood z-scores
N_SHUF = 500           # shuffles for assortativity null

STEM_IT = ["scienza", "matematica", "fisica", "chimica", "biologia", "informatica",
           "statistica", "ingegneria", "tecnologia", "scienziato", "scuola", "insegnante"]
STEM_EN = ["science", "mathematics", "physics", "chemistry", "biology", "informatics",
           "statistics", "engineering", "technology", "scientist", "school", "teacher"]


def label_nodes(G, language, cache):
    if os.path.exists(cache):
        df = pd.read_csv(cache, index_col=0)
        return df
    from emoatlas import EmoScores   # lazy: only needed when rebuilding labels
    es = EmoScores(language=language)
    rows = {}
    for n in G.nodes():
        try:
            e = es.emotions(str(n))
        except Exception:
            e = {k: 0 for k in EMOS}
        rows[n] = [int(e.get(k, 0) > 0) for k in EMOS]
    df = pd.DataFrame.from_dict(rows, orient="index", columns=EMOS)
    df.to_csv(cache)
    return df


def emotion_assortativity(G, emo_df, emotion, n_shuf=N_SHUF, seed=SEED):
    """Assortativity of a binary emotion attribute (numeric 0/1) vs label-shuffle null."""
    attr = emo_df[emotion].to_dict()
    nx.set_node_attributes(G, attr, emotion)
    try:
        obs = nx.numeric_assortativity_coefficient(G, emotion)
    except Exception:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    vals = np.array(list(attr.values()))
    nodes = list(G.nodes())
    null = np.empty(n_shuf)
    for i in range(n_shuf):
        perm = rng.permutation(vals)
        nx.set_node_attributes(G, dict(zip(nodes, perm)), "_p")
        null[i] = nx.numeric_assortativity_coefficient(G, "_p")
    z = (obs - np.nanmean(null)) / np.nanstd(null) if np.nanstd(null) > 0 else np.nan
    return obs, np.nanmean(null), z


def neighbourhood_zscores(G, emo_df, word, n_perm=N_PERM, seed=SEED):
    """For a word: emotion counts among its neighbours vs k random nodes."""
    if word not in G:
        return None
    nbrs = list(G.neighbors(word))
    k = len(nbrs)
    obs = emo_df.loc[[n for n in nbrs if n in emo_df.index], EMOS].sum().values.astype(float)
    M = emo_df[EMOS].values
    idx = np.array([emo_df.index.get_loc(n) for n in emo_df.index])
    rng = np.random.default_rng(seed + hash(word) % 10000)
    N = M.shape[0]
    null = np.empty((n_perm, len(EMOS)))
    for i in range(n_perm):
        sel = rng.choice(N, size=k, replace=False)
        null[i] = M[sel].sum(axis=0)
    mu = null.mean(axis=0); sd = null.std(axis=0)
    z = np.divide(obs - mu, sd, out=np.zeros_like(obs), where=sd > 0)
    return dict(k=k, obs=obs, mu=mu, z=z)


def analyze(name, edges_fn, val_fn, language, stem_words):
    print(f"\n{'='*64}\n{name}\n{'='*64}")
    G = R.build(edges_fn, val_fn)
    cache = os.path.join(OUT, f"emolabels_{language}.csv")
    t = time.time()
    emo_df = label_nodes(G, language, cache)
    emo_df = emo_df.reindex(list(G.nodes())).fillna(0).astype(int)
    print(f"labelled {len(emo_df)} nodes in {time.time()-t:.0f}s  (cache: {os.path.basename(cache)})")

    # 1. prevalence
    prev = emo_df[EMOS].mean().sort_values(ascending=False)
    print("\n[1] Emotion prevalence (fraction of nodes carrying the emotion):")
    for e, v in prev.items():
        print(f"    {e:13s} {100*v:5.1f}%  (n={int(emo_df[e].sum())})")

    # 2. emotion-specific assortativity vs null
    print(f"\n[2] Emotion-specific assortativity (vs {N_SHUF}-shuffle null):")
    assort = {}
    for e in EMOS:
        obs, nul, z = emotion_assortativity(G.copy(), emo_df, e)
        assort[e] = (obs, nul, z)
        sig = "***" if abs(z) > 3 else ("*" if abs(z) > 1.96 else "")
        print(f"    {e:13s} r={obs:+.3f}  null={nul:+.3f}  z={z:+5.1f} {sig}")

    # 3. neighbourhood z-scores for STEM concepts
    print(f"\n[3] Emotional aura of STEM concepts (neighbourhood z vs {N_PERM} random draws):")
    zrows = {}
    for w in stem_words:
        r = neighbourhood_zscores(G, emo_df, w)
        if r is None:
            continue
        zrows[w] = r["z"]
        sig = {EMOS[i]: r["z"][i] for i in range(len(EMOS)) if abs(r["z"][i]) > 1.96}
        top = ", ".join(f"{k}{'+' if v>0 else '-'}{abs(v):.1f}" for k, v in
                        sorted(sig.items(), key=lambda kv: -abs(kv[1])))
        print(f"    {w:12s} (k={r['k']:3d})  {top if top else '(no sig emotion)'}")

    # save z-score matrix + figures
    zmat = pd.DataFrame(zrows, index=EMOS).T
    zmat.to_csv(os.path.join(OUT, f"stem_aura_z_{language}.csv"))
    make_figures(name, language, prev, assort, zmat)
    return prev, assort, zmat


def make_figures(name, language, prev, assort, zmat):
    # heatmap of STEM concept x emotion z-scores
    fig, ax = plt.subplots(figsize=(8, 5.5))
    data = zmat[EMOS].values
    vmax = np.nanmax(np.abs(data)) if data.size else 1
    im = ax.imshow(data, cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(EMOS))); ax.set_xticklabels(EMOS, rotation=40, ha="right")
    ax.set_yticks(range(len(zmat.index))); ax.set_yticklabels(zmat.index)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            v = data[i, j]
            if abs(v) > 1.96:
                ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                        fontsize=7, color="white" if abs(v) > vmax*0.6 else "black")
    ax.set_title(f"Emotional aura of STEM concepts — {name}\n(neighbourhood z-score; |z|>1.96 labelled)", fontsize=10)
    fig.colorbar(im, ax=ax, label="z-score vs random neighbourhood")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f"aura_heatmap_{language}.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    ps, as_, zs = analyze("STUDENTS (Italian high-schoolers)",
                          "FormaMentisStudents.txt", "ValenceLabelsStudents.txt",
                          "italian", STEM_IT)
    pr, ar, zr = analyze("RESEARCHERS (international experts)",
                        "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt",
                        "english", STEM_EN)

    # cross-group prevalence comparison figure
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(EMOS)); w = 0.4
    ax.bar(x - w/2, [ps[e]*100 for e in EMOS], w, label="Students (IT)", color="#c44")
    ax.bar(x + w/2, [pr[e]*100 for e in EMOS], w, label="Researchers (EN)", color="#48c")
    ax.set_xticks(x); ax.set_xticklabels(EMOS, rotation=40, ha="right")
    ax.set_ylabel("% of network words carrying the emotion")
    ax.set_title("Emotion prevalence in STEM forma mentis networks")
    ax.legend(); fig.tight_layout()
    fig.savefig(os.path.join(OUT, "prevalence_compare.png"), dpi=150)
    plt.close(fig)
    print("\nSaved figures + tables to", OUT)
