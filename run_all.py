"""
Reproduce the whole analysis end to end.

Prerequisites:
    python download_data.py          # fetch datasets into ./data/
    pip install -r requirements.txt

Then:
    python run_all.py

Emotion labels are read from the cached results_A1/emolabels_*.csv (committed), so
EmoAtlas is NOT required. To regenerate the labels from scratch, delete those two
files and run emotion_resolved_fmn.py with an EmoAtlas environment first
(see README, "Regenerating emotion labels").
"""
import subprocess, sys, os, time

HERE = os.path.dirname(os.path.abspath(__file__))
STEPS = [
    ("Reproduce Stella et al. (2019) valence results", ["reproduce_stem_fmn.py"]),
    ("Emotion-resolved profiling (prevalence, auras)", ["emotion_resolved_fmn.py"]),
    ("Fear modules, spreading activation, bridges",     ["fear_module_analysis.py"]),
    ("Lexicon robustness (DepecheMood check)",          ["robustness_lexicon.py"]),
    ("Positive control (naive PageRank test fails)",    ["positive_control_null.py"]),
    ("Validated proximity test",                        ["proximity_fixed.py"]),
    ("Revision analyses (degree null, TOST, FDR, ...)", ["revision_analyses.py"]),
    ("Build manuscript PDF",       ["md_to_pdf.py", "MANUSCRIPT.md", "MANUSCRIPT.pdf"]),
    ("Build response-letter PDF",  ["md_to_pdf.py", "RESPONSE_LETTER.md", "RESPONSE_LETTER.pdf", "--no-figures"]),
]


def main():
    for i, (label, args) in enumerate(STEPS, 1):
        print(f"\n{'='*70}\n[{i}/{len(STEPS)}] {label}\n{'='*70}")
        t = time.time()
        subprocess.check_call([sys.executable, os.path.join(HERE, args[0])] + args[1:], cwd=HERE)
        print(f"   done in {time.time()-t:.0f}s")
    print("\nAll steps complete. Figures/tables in results_A1/, PDFs in repo root.")


if __name__ == "__main__":
    main()
