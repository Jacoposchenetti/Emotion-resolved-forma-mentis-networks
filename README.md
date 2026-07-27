# Emotion-resolved forma mentis networks

**Valence without fear: STEM negativity is evaluative, not affectively wired.**

A fully reproducible reanalysis and extension of Stella, De Nigris, Aloric & Siew
(2019), *"Forma mentis networks quantify crucial differences in STEM perception
between students and experts"* ([PLOS ONE 14(10): e0222870](https://doi.org/10.1371/journal.pone.0222870);
data on [OSF xyfwg](https://osf.io/xyfwg/)).

Where the original study summarised the affect in these free-association networks as
three-level **valence**, this project resolves it into Plutchik's eight emotions
(via [EmoAtlas](https://github.com/MassimoStel/emoatlas)) and adds the structural test
that valence omits. The headline results:

1. **The original valence findings reproduce** (network sizes exact; researcher valence
   assortativity 0.116 and neighbourhood clustering 0.324 recovered to rounding;
   *matematica* 44% negative associates vs the reported ~43%).
2. **Fear is a robustly cohesive emotion** in both mindsets — the cohesion holds across
   four emotion lexicons, two of them independent of NRC (and on the vocabulary they
   jointly cover).
3. **STEM concepts are not wired to fear.** Under a degree-preserving null no core STEM
   concept is closer to fear than chance in either group; several are significantly
   *farther* (FDR-corrected), and an equivalence test puts their proximity below the
   detectable-effect threshold. STEM negativity is evaluative and lexical (it travels
   through "difficulty" vocabulary), not a connection into the affective fear network.

Two methodological cautions fall out of the analysis and are part of the contribution:
a commonly used spreading-activation statistic is **underpowered** for this question
(shown with an injection positive control), and a single emotion lexicon can manufacture
a group difference that **does not replicate** across lexicons.

## Reproduce

```bash
# 1. environment (Python 3.9–3.11 recommended)
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. fetch the datasets from their original sources into ./data/
python download_data.py

# 3. run the whole pipeline (reproduction -> extension -> revision -> PDFs)
python run_all.py
```

`run_all.py` runs every step in order and rebuilds the manuscript and response-letter
PDFs. Emotion labels are read from the committed `results_A1/emolabels_*.csv`, so
**EmoAtlas is not required** for the default path. Individual scripts also run
standalone (each has a `__main__`).

## What is in here

| File | Role |
|---|---|
| `download_data.py` | fetch all third-party datasets into `data/` |
| `run_all.py` | run the full pipeline end to end |
| `reproduce_stem_fmn.py` | reproduce Stella et al. (2019) valence results + null models |
| `emotion_resolved_fmn.py` | Plutchik emotion labelling, prevalence, concept "auras" |
| `fear_module_analysis.py` | Louvain fear modules, spreading activation, bridge words |
| `robustness_lexicon.py` | independent-lexicon check (DepecheMood) |
| `positive_control_null.py` | injection positive control that fails the naive PageRank test |
| `proximity_fixed.py` | validated distance-based proximity test + injection validation |
| `revision_analyses.py` | degree-preserving null, common-vocab re-test, TOST equivalence, Louvain stability, BH-FDR |
| `md_to_pdf.py` | render a Markdown paper to a line-numbered PDF |
| `MANUSCRIPT.md` / `.pdf` | the paper (line-numbered PDF) |
| `RESPONSE_LETTER.md` / `.pdf` | point-by-point response to a simulated review |
| `REVIEW.md`, `REPORT.md`, `OUTLINE.md`, `CITATION_CHECK.md` | reproduction report, simulated review, outline, verified citations |
| `results_A1/` | figures, z-score tables, and cached emotion labels |

## Data sources and licenses

Datasets are **not** redistributed here; `download_data.py` fetches each from its source.

| Dataset | Source | License |
|---|---|---|
| Forma mentis networks | Stella et al. (2019), OSF `xyfwg` | CC-BY 4.0 |
| English VAD norms | Warriner, Kuperman & Brysbaert (2013) | research use |
| Italian VAD norms | Fairfield et al. (2017), PLOS ONE `pone.0169472` S1 | CC-BY |
| DepecheMood++ | Araque, Gatti, Staiano & Guerini (2022) | CC-BY-NC-SA |
| NRC Emotion Lexicon | Mohammad & Turney (2013) | research use, **no redistribution** |

## Regenerating emotion labels (optional)

The Plutchik labels in `results_A1/emolabels_{italian,english}.csv` were produced with
EmoAtlas 0.1.6, which pins `spacy==3.7.2` and needs the large spaCy models
(`it_core_news_lg`, `en_core_web_lg`) plus NLTK WordNet — so a dedicated **Python
3.9–3.11** environment. To rebuild them, install EmoAtlas in such an environment, delete
the two cached CSVs, and run `emotion_resolved_fmn.py`.

## Citation

If you use this code, please cite the original data paper (Stella et al., 2019) and this
repository. The manuscript with full methods, results, and references is `MANUSCRIPT.pdf`.

## License

Code: MIT (`LICENSE`). Data: see each source above.
