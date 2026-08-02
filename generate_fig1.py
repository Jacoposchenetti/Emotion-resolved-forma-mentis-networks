# -*- coding: utf-8 -*-
"""Figure 1 — forma mentis ego-networks of the mathematics cue.
ALL first associates are shown, arranged by valence around the cue, so the coloured
arc lengths equal the reported valence proportions (no sub-sampling)."""
import os, numpy as np, networkx as nx, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import reproduce_stem_fmn as R

OUT = os.path.join(os.path.dirname(__file__), "results_A1")
NEG, POS, NEU, CUE = "#c0392b", "#27ae60", "#c8ccd0", "#2c3e50"
ORDER = ["Negative", "Neutral", "Positive"]
COL = {"Negative": NEG, "Neutral": NEU, "Positive": POS}


def draw_panel(ax, G, cue, title, labels_per_class):
    vlab = nx.get_node_attributes(G, "vlabel")
    nbrs = list(G.neighbors(cue))
    # order all associates by valence class -> contiguous coloured arcs
    grouped = {k: [n for n in nbrs if vlab.get(n, "Neutral") == k] for k in ORDER}
    ordered = [n for k in ORDER for n in grouped[k]]
    N = len(ordered)
    ang = np.linspace(0.5 * np.pi, 0.5 * np.pi - 2 * np.pi, N, endpoint=False)  # clockwise from top
    posx = {n: (np.cos(a), np.sin(a)) for n, a in zip(ordered, ang)}
    ang_of = {n: a for n, a in zip(ordered, ang)}

    for n in ordered:                                    # ego edges (cue -> associate)
        ax.plot([0, posx[n][0]], [0, posx[n][1]], color="#e2e4e7", lw=0.5, zorder=1)
    for n in ordered:
        ax.scatter(*posx[n], s=95, c=COL[vlab.get(n, "Neutral")], edgecolors="white",
                   linewidths=0.4, zorder=2)
    ax.scatter(0, 0, s=2300, c=CUE, edgecolors="black", linewidths=1.4, zorder=3)
    ax.text(0, 0, cue, ha="center", va="center", color=CUE, fontsize=8.5, fontweight="bold",
            zorder=5, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=CUE, lw=1.1))

    # label a few associates per valence class, spaced within the interior of each arc
    for k in ORDER:
        g = grouped[k]
        if not g:
            continue
        idx = (np.linspace(0.15, 0.85, min(labels_per_class, len(g))) * (len(g) - 1)).round().astype(int)
        for j in np.unique(idx):
            n = g[j]; a = ang_of[n]
            lr = 1.13
            ha = "left" if np.cos(a) > 0.08 else "right" if np.cos(a) < -0.08 else "center"
            ax.text(lr * np.cos(a), lr * np.sin(a), n, ha=ha, va="center",
                    fontsize=6.8, color="#333", zorder=4)

    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.35); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=11, loc="left")
    c = {k: len(grouped[k]) for k in ORDER}
    ax.text(0, -1.4, f"{round(100*c['Negative']/N)}% negative · {round(100*c['Positive']/N)}% "
            f"positive · {round(100*c['Neutral']/N)}% neutral   (all {N} associates shown)",
            ha="center", va="top", fontsize=8.4, color="#555")


def main():
    GS = R.build("FormaMentisStudents.txt", "ValenceLabelsStudents.txt")
    GR = R.build("FormaMentisResearchers.txt", "ValenceLabelsResearchers.txt")
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.6))
    draw_panel(axes[0], GS, "matematica", "A   Students (Italian high-schoolers)", 5)
    draw_panel(axes[1], GR, "mathematics", "B   Researchers (international experts)", 5)
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markersize=11,
                      markeredgecolor="white", label=l)
               for c, l in [(NEG, "negative"), (POS, "positive"), (NEU, "neutral"), (CUE, "cue word")]]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=9,
               bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    path = os.path.join(OUT, "fig1_formamentis.png")
    fig.savefig(path, dpi=200, bbox_inches="tight")
    print("wrote", path)


if __name__ == "__main__":
    main()
