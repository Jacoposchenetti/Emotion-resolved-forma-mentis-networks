# -*- coding: utf-8 -*-
"""Publication-quality figures for the Meta-Psychology manuscript.
Unified style (Okabe-Ito colourblind-safe palette, clean axes, 300 dpi)."""
import os, numpy as np, networkx as nx, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import reproduce_stem_fmn as R, robustness_lexicon as RL, revision_analyses as RV
import proximity_fixed as PX, fear_module_analysis as F

OUT = F.OUT
plt.rcParams.update({
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.titlesize": 12, "axes.labelsize": 11, "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.labelsize": 10, "ytick.labelsize": 10,
    "legend.fontsize": 9, "legend.frameon": False,
})
# Okabe-Ito
C_STU, C_RES = "#D55E00", "#0072B2"
C_NEG, C_POS, C_NEU = "#D55E00", "#009E73", "#BEBEBE"

GS = R.build("FormaMentisStudents.txt", "ValenceLabelsStudents.txt")
GR = R.build("FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt")


# ---------- Figure 1: forma mentis ego-networks coloured by valence ----------
def ego_panel(ax, G, concept, title, k=16, seed=4):
    val = nx.get_node_attributes(G, "val")
    rng = np.random.default_rng(seed)
    nbrs = list(G.neighbors(concept))
    # stratified sampling: preserve the TRUE valence proportions of the aura
    neg = [n for n in nbrs if val[n] < 0]; pos = [n for n in nbrs if val[n] > 0]
    neu = [n for n in nbrs if val[n] == 0]; tot = len(nbrs)
    kn = round(k * len(neg) / tot); kp = round(k * len(pos) / tot); ku = k - kn - kp
    pick = lambda pool, m: list(rng.choice(pool, min(m, len(pool)), replace=False)) if pool else []
    sel = pick(neg, kn) + pick(pos, kp) + pick(neu, ku)
    H = G.subgraph([concept] + sel)
    pos = nx.spring_layout(H, seed=seed, k=0.9)
    cols = [C_NEG if val[n] < 0 else C_POS if val[n] > 0 else C_NEU for n in H.nodes()]
    sizes = [1500 if n == concept else 620 for n in H.nodes()]
    edgec = ["black" if n == concept else "#555" for n in H.nodes()]
    lw = [2.2 if n == concept else 0.8 for n in H.nodes()]
    nx.draw_networkx_edges(H, pos, ax=ax, edge_color="#cccccc", width=1.0)
    nx.draw_networkx_nodes(H, pos, ax=ax, node_color=cols, node_size=sizes,
                           edgecolors=edgec, linewidths=lw)
    nx.draw_networkx_labels(H, pos, ax=ax, font_size=7.5)
    ax.set_title(title, fontsize=12); ax.axis("off")
    ax.text(0.5, -0.04, f"{100*len(neg)/tot:.0f}% of all {tot} associates negative "
            f"(sample shown, proportions preserved)",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="#444")


def fig1():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.2))
    ego_panel(axes[0], GS, "matematica", "A  Students — matematica")
    ego_panel(axes[1], GR, "mathematics", "B  Researchers — mathematics")
    handles = [Line2D([0], [0], marker="o", ls="", mfc=c, mec="#555", ms=11, label=l)
               for c, l in [(C_NEG, "negative"), (C_POS, "positive"), (C_NEU, "neutral")]]
    fig.legend(handles=handles, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Forma mentis ego-networks of the mathematics cue, coloured by valence",
                 fontsize=12.5, y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1_formamentis.png")); plt.close(fig)
    print("fig1 done")


# ---------- Figure 2: fear assortativity across four lexicons ----------
def fig2():
    lex_order = ["EmoAtlas", "NRC-direct", "VAD", "DepecheMood"]
    label = {"EmoAtlas": "EmoAtlas (NRC-synset)", "NRC-direct": "NRC word-level",
             "VAD": "VAD quadrant (independent)", "DepecheMood": "DepecheMood (independent)"}
    res = {"students": {}, "researchers": {}}
    for name, G, lang in [("students", GS, "italian"), ("researchers", GR, "english")]:
        attrs = RV.fear_attrs_all(G, lang)
        for lx in lex_order:
            if lx in attrs:
                res[name][lx] = RL.assort_ci(G, attrs[lx])
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    y = np.arange(len(lex_order))
    for grp, col, off in [("students", C_STU, 0.16), ("researchers", C_RES, -0.16)]:
        for i, lx in enumerate(lex_order):
            if lx not in res[grp]:
                continue
            o, lo, hi = res[grp][lx]
            ax.errorbar(o, i + off, xerr=[[o - lo], [hi - o]], fmt="o", color=col,
                        capsize=3, ms=6, lw=1.4, label=grp.capitalize() if i == 0 else "")
    ax.axvline(0, color="#888", lw=0.8, ls="--")
    ax.set_yticks(y); ax.set_yticklabels([label[l] for l in lex_order]); ax.invert_yaxis()
    ax.set_xlabel("Fear assortativity  r  (95% CI)")
    ax.set_title("Within-group fear cohesion is robust; the student–expert gap\nappears only for EmoAtlas")
    ax.legend(loc="lower right")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "lexicon_robustness.png")); plt.close(fig)
    print("fig2 done")


# ---------- Figure 3: positive control (PageRank vs validated proximity) ----------
def fig3():
    G, fear = RV.load("FormaMentisStudents.txt", "ValenceLabelsStudents.txt", "italian")
    js = [0, 5, 10, 15, 20, 30]
    # validated decay proximity z
    cd, _ = PX.injection_control(G, fear, "matematica", js=tuple(js), reps=4)
    dz = [z for _, z in cd]
    # PageRank fear-mass z
    from positive_control_null import fear_mass_z
    rng = np.random.default_rng(1)
    fl = [f for f in fear if f != "matematica" and not G.has_edge("matematica", f)]
    pz = []
    for j in js:
        vals = []
        for _ in range(4):
            H = G.copy()
            if j:
                t = rng.choice(len(fl), j, replace=False)
                H.add_edges_from(("matematica", fl[x]) for x in t)
            vals.append(fear_mass_z(H, fear, "matematica", n_perm=200,
                                    rng=np.random.default_rng(int(rng.integers(1e9))), exclude_seed=True))
        pz.append(np.mean(vals))
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    ax.axhspan(-1.96, 1.96, color="#eeeeee", label="non-significant band")
    ax.axhline(1.96, color="#888", lw=0.7, ls=":")
    ax.plot(js, pz, "o-", color="#999999", lw=1.8, ms=6, label="PageRank fear-mass (discarded)")
    ax.plot(js, dz, "o-", color=C_STU, lw=1.8, ms=6, label="decay proximity (validated)")
    ax.set_xlabel("synthetic edges injected: matematica → fear nodes")
    ax.set_ylabel("detection z-score")
    ax.set_title("Positive control: only the validated test detects injected fear-embedding")
    ax.legend(loc="upper left")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "proximity_control_extended.png")); plt.close(fig)
    print("fig3 done")


# ---------- Figure 4: validated proximity under degree-preserving null ----------
def fig4():
    concepts = F.STEM_IT
    data = {}
    for name, ef, vf, lang, cl in [("Students", "FormaMentisStudents.txt", "ValenceLabelsStudents.txt", "italian", F.STEM_IT),
                                   ("Researchers", "FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt", "english", F.STEM_EN)]:
        G, fear = RV.load(ef, vf, lang)
        data[name] = {c: RV.prox_degstrat(G, fear, c, nperm=400)[0] for c in cl if c in G}
    zS = [data["Students"].get(c, np.nan) for c in F.STEM_IT]
    zR = [data["Researchers"].get(e, np.nan) for e in F.STEM_EN]
    fig, ax = plt.subplots(figsize=(9.2, 4.7))
    x = np.arange(len(concepts)); w = 0.4
    ax.axhspan(-1.96, 1.96, color="#eeeeee", label="non-significant band")
    ax.bar(x - w/2, zS, w, color=C_STU, label="Students")
    ax.bar(x + w/2, zR, w, color=C_RES, label="Researchers")
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels(concepts, rotation=40, ha="right")
    ax.set_ylabel("proximity-to-fear  z  (negative = farther than chance)")
    ax.set_title("Under a degree-preserving null, no STEM concept is closer to fear than chance")
    ax.legend(loc="lower left", ncol=3)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "proximity_result.png")); plt.close(fig)
    print("fig4 done")


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("all publication figures written to", OUT)
