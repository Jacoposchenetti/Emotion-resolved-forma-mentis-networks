"""
Revision analyses addressing the simulated reviewers' four in-data requests.
R1-2  degree-preserving (degree-stratified) null for the proximity test
R1-1  common-vocabulary re-test of the four fear lexicons
R1-3  TOST-style equivalence framing of the proximity null vs the injection MDE
R1m   Louvain stability (modularity + fear-module) and BH-FDR over concept tests
"""
import os, numpy as np, pandas as pd, networkx as nx, collections
from networkx.algorithms import community
import reproduce_stem_fmn as R, robustness_lexicon as RL, fear_module_analysis as F, proximity_fixed as PX
OUT = F.OUT; BETA = 0.5
STEM = {"italian": F.STEM_IT, "english": F.STEM_EN}


def load(ef, vf, lang):
    G = R.build(ef, vf)
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0).reindex(list(G.nodes())).fillna(0).astype(int)
    fear = set(n for n in G.nodes() if emo.loc[n, "fear"] > 0)
    return G, fear


def decay(dist, nodeset):
    return sum(BETA ** dist[n] for n in nodeset if n in dist and dist[n] > 0)


# ---------- R1-2 degree-stratified null ----------
def prox_degstrat(G, fear, concept, nperm=1000, seed=42, nbin=10):
    dist = nx.single_source_shortest_path_length(G, concept)
    obs = decay(dist, fear)
    nodes = list(G.nodes()); deg = np.array([G.degree(n) for n in nodes])
    edges = np.quantile(deg, np.linspace(0, 1, nbin + 1))
    binid = np.clip(np.digitize(deg, edges[1:-1]), 0, nbin - 1)
    pool = {b: [nodes[i] for i in range(len(nodes)) if binid[i] == b] for b in range(nbin)}
    fbins = collections.Counter(binid[i] for i, n in enumerate(nodes) if n in fear)
    rng = np.random.default_rng(seed + abs(hash(concept)) % 9999)
    null = np.empty(nperm)
    for k in range(nperm):
        s = set()
        for b, c in fbins.items():
            p = pool[b]
            s |= set(np.array(p, dtype=object)[rng.choice(len(p), min(c, len(p)), replace=False)])
        null[k] = decay(dist, s)
    z = (obs - null.mean()) / null.std() if null.std() > 0 else np.nan
    p = 2 * min((np.sum(null >= obs) + 1) / (nperm + 1), (np.sum(null <= obs) + 1) / (nperm + 1))
    # bootstrap CI of z via resampling null? report z + empirical p
    return z, p


# ---------- R1-1 common-vocabulary lexicon re-test ----------
def coverage_sets(lang):
    dep = pd.read_csv(os.path.join(RL.DATA, f"depeche_{lang}.tsv"), sep="\t", index_col=0)
    dep_words = set(str(w).lower() for w in dep.index)
    if lang == "english":
        w = pd.read_csv(os.path.join(RL.DATA, "warriner.csv"))
        vad_words = set(w["Word"].astype(str).str.lower())
    else:
        df = pd.read_excel(os.path.join(RL.DATA, "it_vad_s001.xlsx"), sheet_name="Database", header=1)
        vad_words = set(df["Ita_Word"].astype(str).str.lower())
    return dep_words, vad_words


def fear_attrs_all(G, lang):
    """dict lexicon-> {node:0/1} using module builders."""
    import importlib
    a = {}
    emo = pd.read_csv(os.path.join(OUT, f"emolabels_{lang}.csv"), index_col=0).reindex(list(G.nodes())).fillna(0)
    a["EmoAtlas"] = {n: int(emo.loc[n, "fear"] > 0) for n in G.nodes()}
    # DepecheMood top-k
    dep = pd.read_csv(os.path.join(RL.DATA, f"depeche_{lang}.tsv"), sep="\t", index_col=0)
    sc = dict(zip((str(w).lower() for w in dep.index), dep[RL.FEAR_COL[lang]].values))
    k = int((emo["fear"] > 0).sum())
    cand = sorted(((n, sc[str(n).lower()]) for n in G if str(n).lower() in sc), key=lambda x: -x[1])
    fs = set(n for n, _ in cand[:k]); a["DepecheMood"] = {n: (1 if n in fs else 0) for n in G.nodes()}
    # VAD
    if lang == "english":
        w = pd.read_csv(os.path.join(RL.DATA, "warriner.csv")); val = dict(zip(w["Word"].astype(str).str.lower(), w["V.Mean.Sum"])); aro = dict(zip(w["Word"].astype(str).str.lower(), w["A.Mean.Sum"]))
    else:
        df = pd.read_excel(os.path.join(RL.DATA, "it_vad_s001.xlsx"), sheet_name="Database", header=1)
        val = dict(zip(df["Ita_Word"].astype(str).str.lower(), pd.to_numeric(df["M_Val"], errors="coerce"))); aro = dict(zip(df["Ita_Word"].astype(str).str.lower(), pd.to_numeric(df["M_Aro"], errors="coerce")))
    vm = np.nanmedian(list(val.values())); am = np.nanmedian(list(aro.values()))
    a["VAD"] = {n: (1 if (str(n).lower() in val and val[str(n).lower()] < vm and aro[str(n).lower()] > am) else 0) for n in G.nodes()}
    if lang == "english":
        nrc = {}
        for line in open(os.path.join(RL.DATA, "nrc_english.txt"), encoding="utf-8"):
            pp = line.rstrip("\n").split("\t")
            if len(pp) == 3 and pp[1] == "fear":
                nrc[pp[0].lower()] = int(pp[2])
        a["NRC-direct"] = {n: (1 if nrc.get(str(n).lower(), 0) == 1 else 0) for n in G.nodes()}
    return a


def common_vocab_retest(G, lang):
    dep_words, vad_words = coverage_sets(lang)
    covered = [n for n in G.nodes() if str(n).lower() in dep_words and str(n).lower() in vad_words]
    H = G.subgraph(covered).copy()
    attrs = fear_attrs_all(G, lang)
    print(f"   common-covered nodes: {len(covered)}/{G.number_of_nodes()}  subgraph edges: {H.number_of_edges()}")
    for name, at in attrs.items():
        sub = {n: at[n] for n in H.nodes()}
        if sum(sub.values()) < 3:
            print(f"     {name:12s} too few fear nodes in common subgraph ({sum(sub.values())})"); continue
        o, lo, hi = RL.assort_ci(H, sub)
        print(f"     {name:12s} r={o:+.3f} [{lo:+.3f},{hi:+.3f}]  (fear n={sum(sub.values())})")


# ---------- R1-3 equivalence (bootstrap CI of proximity z) ----------
def prox_bootstrap_ci(G, fear, concept, nboot=300, nperm=400, seed=7):
    """Bootstrap the proximity z by resampling edges; report 90% CI for TOST."""
    rng = np.random.default_rng(seed)
    zs = []
    edges = list(G.edges())
    for _ in range(nboot):
        H = nx.Graph(); H.add_nodes_from(G.nodes())
        idx = rng.integers(0, len(edges), len(edges))
        H.add_edges_from(edges[i] for i in idx)
        if concept not in H or H.degree(concept) == 0:
            continue
        dist = nx.single_source_shortest_path_length(H, concept)
        obs = decay(dist, fear)
        nodes = list(H.nodes()); N = len(nodes); k = len(fear)
        na = np.array([decay(dist, set(np.array(nodes, dtype=object)[rng.choice(N, k, replace=False)])) for _ in range(nperm)])
        zs.append((obs - na.mean()) / na.std() if na.std() > 0 else 0.0)
    zs = np.array(zs)
    return np.percentile(zs, 5), np.percentile(zs, 95)


# ---------- R1m Louvain stability + FDR ----------
def louvain_stability(G, fear, nseed=50):
    mods, ffrac = [], []
    for s in range(nseed):
        comms = community.louvain_communities(G, seed=s)
        mods.append(community.modularity(G, comms))
        best = max((len(c & fear) / len(c) for c in comms if len(c) >= 10), default=0)
        ffrac.append(best)
    return np.mean(mods), np.std(mods), np.mean(ffrac), np.std(ffrac)


def bh_fdr(pvals, q=0.05):
    p = np.array(pvals); n = len(p); order = np.argsort(p)
    thresh = q * (np.arange(1, n + 1)) / n
    passed = p[order] <= thresh
    kmax = np.where(passed)[0].max() + 1 if passed.any() else 0
    crit = p[order][kmax - 1] if kmax else 0
    return crit, kmax


if __name__ == "__main__":
    groups = [("STUDENTS", "FormaMentisStudents.txt", "ValenceLabelsStudents.txt", "italian"),
              ("RESEARCHERS", "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt", "english")]
    allp = []
    for name, ef, vf, lang in groups:
        G, fear = load(ef, vf, lang)
        print(f"\n{'='*66}\n{name}\n{'='*66}")
        print("[R1-2] proximity z under DEGREE-STRATIFIED null:")
        for c in STEM[lang]:
            if c not in G: continue
            z, p = prox_degstrat(G, fear, c)
            allp.append((name, c, p, z))
            sig = "***" if p < 0.05 else ""
            print(f"     {c:12s} z={z:+5.1f}  p={p:.3f} {sig}")
        print("[R1-1] common-vocabulary lexicon re-test:")
        common_vocab_retest(G, lang)
        print("[R1-3] equivalence: proximity z 90% CI for hard-science concepts:")
        for c in (["matematica","fisica","chimica"] if lang=="italian" else ["mathematics","physics","chemistry"]):
            if c in G:
                lo, hi = prox_bootstrap_ci(G, fear, c)
                verdict = "within trivial band (equiv. to no positive embedding)" if hi < 1.96 else "CI reaches significance"
                print(f"     {c:12s} 90% CI z=[{lo:+.2f},{hi:+.2f}]  -> {verdict}")
        print("[R1m] Louvain stability (50 seeds):")
        mm, ms, fm, fs = louvain_stability(G, fear)
        print(f"     modularity {mm:.3f} ± {ms:.3f} ; top fear-module fear-fraction {fm:.2f} ± {fs:.2f}")

    print(f"\n{'='*66}\n[R1m] BH-FDR over {len(allp)} concept proximity tests (q=0.05)\n{'='*66}")
    crit, npass = bh_fdr([p for _,_,p,_ in allp])
    print(f"   BH critical p = {crit:.4f}; {npass} tests significant after FDR:")
    for nm, c, p, z in sorted(allp, key=lambda x: x[2]):
        if p <= crit:
            print(f"     {nm:11s} {c:12s} z={z:+.1f} p={p:.3f}")
