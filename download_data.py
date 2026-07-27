"""
Fetch the third-party datasets from their original sources into ./data/.
Nothing here is redistributed in the repository (the NRC lexicon in particular
does not permit redistribution); this script downloads each from its canonical
public location. Run once before the analyses:

    python download_data.py
"""
import os, io, zipfile, urllib.request, ssl

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA, exist_ok=True)
_CTX = ssl.create_default_context()

SOURCES = {
    # Stella et al. (2019) forma mentis networks — OSF xyfwg, CC-BY 4.0
    "stem_zip": ("https://osf.io/download/qcpnh/", "ComplexFormaMentis.zip"),
    # Warriner, Kuperman & Brysbaert (2013) English VAD norms (XANEW mirror)
    "warriner": ("https://raw.githubusercontent.com/JULIELab/XANEW/master/Ratings_Warriner_et_al.csv", "warriner.csv"),
    # DepecheMood++ (Araque et al. 2022) — English & Italian lemma lexicons
    "depeche_en": ("https://raw.githubusercontent.com/marcoguerini/DepecheMood/master/DepecheMood%2B%2B/DepecheMood_english_lemma_full.tsv", "depeche_english.tsv"),
    "depeche_it": ("https://raw.githubusercontent.com/marcoguerini/DepecheMood/master/DepecheMood%2B%2B/DepecheMood_italian_lemma_full.tsv", "depeche_italian.tsv"),
    # NRC Emotion Lexicon (Mohammad & Turney 2013), English word-level (research-only license; not redistributed)
    "nrc_en": ("https://raw.githubusercontent.com/Franck-Dernoncourt/NRC_Emotion_Lexicon/master/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt", "nrc_english.txt"),
    # Fairfield et al. (2017) Italian VAD norms — PLOS ONE supplementary S1, CC-BY
    "it_vad": ("https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0169472.s001&type=supplementary", "it_vad_s001.xlsx"),
}


def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (reproducibility script)"})
    with urllib.request.urlopen(req, context=_CTX, timeout=120) as r:
        return r.read()


def main():
    for key, (url, name) in SOURCES.items():
        dest = os.path.join(DATA, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 1000:
            print(f"[skip] {name} already present")
            continue
        print(f"[get ] {name} <- {url.split('//')[1][:60]}...")
        blob = fetch(url, dest)
        with open(dest, "wb") as f:
            f.write(blob)
        print(f"       wrote {name} ({len(blob):,} bytes)")

    # extract the Stella networks
    stem_dir = os.path.join(DATA, "stem")
    zpath = os.path.join(DATA, "ComplexFormaMentis.zip")
    if os.path.exists(zpath):
        os.makedirs(stem_dir, exist_ok=True)
        with zipfile.ZipFile(zpath) as z:
            z.extractall(stem_dir)
        print(f"[ok  ] extracted forma mentis edge lists -> data/stem/")

    print("\nAll datasets ready in ./data/. Next: python run_all.py")


if __name__ == "__main__":
    main()
