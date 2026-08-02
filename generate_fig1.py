# -*- coding: utf-8 -*-
"""Figure 1 — forma mentis ego-networks of the mathematics cue, coloured by valence."""
import os, numpy as np, networkx as nx, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import reproduce_stem_fmn as R

OUT = os.path.join(os.path.dirname(__file__), "results_A1")
NEG, POS, NEU = "#c0392b", "#27ae60", "#c8ccd0"
CUE = "#2c3e50"
rng = np.random.default_rng(7)


def ego_sample(G, cue, max_neighbors):
    """Cue + a sample of its neighbours preserving valence proportions."""
    vlab = nx.get_node_attributes(G, "vlabel")
    nbrs = list(G.neighbors(cue))
    if len(nbrs) > max_neighbors:
        by_val = {"Negative": [], "Positive": [], "Neutral": []}
        for n in nbrs:
            by_val.get(vlab.get(n, "Neutral"), by_val["Neutral"]).append(n)
        keep = []
        for v, lst in by_val.items():
            k = round(max_neighbors * len(lst) / len(nbrs))
            keep += list(rng.choice(lst, size=min(k, len(lst)), replace=False)) if lst else []
        nbrs = keep
    return [cue] + nbrs


def draw_panel(ax, G, cue, title, max_neighbors, n_labels):
    vlab = nx.get_node_attributes(G, "vlabel")
    ego = ego_sample(G, cue, max_neighbors)
    H = G.subgraph(ego).copy()
    fixed = {cue: (0.0, 0.0)}
    pos = nx.spring_layout(H, k=0.9, seed=3, pos=fixed, fixed=[cue], iterations=200)
    colmap = {"Negative": NEG, "Positive": POS, "Neutral": NEU}
    node_col = [CUE if n == cue else colmap.get(vlab.get(n, "Neutral"), NEU) for n in H.nodes()]
    node_sz = [1500 if n == cue else 240 for n in H.nodes()]
    nx.draw_networkx_edges(H, pos, ax=ax, edge_color="#d0d3d7", width=0.7)
    nx.draw_networkx_nodes(H, pos, ax=ax, node_color=node_col, node_size=node_sz,
                           edgecolors=["black" if n == cue else "white" for n in H.nodes()],
                           linewidths=[1.6 if n == cue else 0.5 for n in H.nodes()])
    # label the cue + the highest-degree neighbours (most central to the aura)
    deg = dict(H.degree())
    nbr_labels = sorted((n for n in H.nodes() if n != cue), key=lambda n: -deg[n])[:n_labels]
    nx.draw_networkx_labels(H, pos, labels={n: n for n in nbr_labels}, ax=ax,
                            font_size=7.2, font_color="#222")
    nx.draw_networkx_labels(H, pos, labels={cue: cue.upper()}, ax=ax,
                            font_size=8.5, font_color="black", font_weight="bold")
    ax.set_title(title, fontsize=11, loc="left")
    ax.axis("off")
    c = {"Negative": 0, "Positive": 0, "Neutral": 0}
    for n in G.neighbors(cue):
        c[vlab.get(n, "Neutral")] = c.get(vlab.get(n, "Neutral"), 0) + 1
    tot = sum(c.values())
    ax.text(0.5, -0.04, f"{100*c['Negative']//tot}% negative · {100*c['Positive']//tot}% positive "
            f"· {100*c['Neutral']//tot}% neutral  (of {tot} associates)",
            transform=ax.transAxes, ha="center", va="top", fontsize=8.2, color="#555")


def main():
    GS = R.build("FormaMentisStudents.txt", "ValenceLabelsStudents.txt")
    GR = R.build("FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt")
    fig, axes = plt.subplots(1, 2, figsize=(11, 5.3))
    draw_panel(axes[0], GS, "matematica", "A   Students (Italian high-schoolers)", 42, 13)
    draw_panel(axes[1], GR, "mathematics", "B   Researchers (international experts)", 49, 12)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=11,
                      markeredgecolor="white", label=l)
               for c, l in [(NEG, "negative"), (POS, "positive"), (NEU, "neutral"),
                            (CUE, "cue word")]]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    path = os.path.join(OUT, "fig1_formamentis.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print("wrote", path)


if __name__ == "__main__":
    main()
