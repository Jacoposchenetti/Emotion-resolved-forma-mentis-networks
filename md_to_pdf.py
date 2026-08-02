"""Render MANUSCRIPT.md to a submission-style PDF with continuous line numbers."""
import os, re, matplotlib
from fpdf import FPDF

HERE = os.path.dirname(__file__)
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
OUT = os.path.join(HERE, "results_A1")
FIGS = [
    ("Figure 1. Forma mentis ego-networks of the mathematics cue, coloured by valence "
     "(red = negative, green = positive, grey = neutral); the cue is outlined in black. In students "
     "(A) mathematics sits in a predominantly negative aura (44% of its 100 associates negative); in "
     "researchers (B) it does not (0% of 49). A representative sample is shown, valence proportions "
     "preserved.", os.path.join(OUT, "fig1_formamentis.png")),
    ("Figure 2. Fear assortativity across four emotion lexicons (bootstrap 95% CI). "
     "Within-group cohesion is robust (3/4 lexicons, incl. the independent VAD); the "
     "student-expert gap appears only for EmoAtlas.", os.path.join(OUT, "lexicon_robustness.png")),
    ("Figure 3. Injection positive control for the fixed proximity test: z now crosses "
     "significance once ~10-30% of a concept's edges are redirected to fear.",
     os.path.join(OUT, "proximity_control_extended.png")),
    ("Figure 4. Validated proximity of STEM concepts to fear under a degree-preserving null. "
     "No concept is closer than chance in either group; several are significantly farther "
     "(FDR-corrected).", os.path.join(OUT, "proximity_result.png")),
]

LEFT, RIGHT, TOP, BOT = 28.0, 18.0, 18.0, 18.0
PAGE_W, PAGE_H = 210.0, 297.0
CONTENT_W = PAGE_W - LEFT - RIGHT
NUM_X = 12.0


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", s)   # links -> text (url)
    s = s.replace("**", "").replace("`", "")
    s = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", s)  # *italic*
    return s


class Doc(FPDF):
    def __init__(self):
        super().__init__(format="A4", unit="mm")
        self.set_auto_page_break(False)
        self.set_margins(LEFT, TOP, RIGHT)
        for st, fn in [("", "DejaVuSans.ttf"), ("B", "DejaVuSans-Bold.ttf"),
                       ("I", "DejaVuSans-Oblique.ttf")]:
            self.add_font("DJ", st, os.path.join(FDIR, fn))
        self.add_font("MONO", "", os.path.join(FDIR, "DejaVuSansMono.ttf"))
        self.lineno = 0
        self.numbering = True
        self.add_page()
        self.set_xy(LEFT, TOP)

    def _wrap(self, text, size, style=""):
        self.set_font("DJ", style, size)
        words, lines, cur = text.split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if self.get_string_width(t) <= CONTENT_W:
                cur = t
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines or [""]

    def _newpage(self):
        self.add_page(); self.set_xy(LEFT, TOP)

    def emit(self, text, size=10.5, style="", lh=5.0, gap_before=0.0, gap_after=1.4,
             mono=False, number=True):
        if gap_before:
            self.set_y(self.get_y() + gap_before)
        if mono:
            fs = size
            self.set_font("MONO", "", fs)
            while self.get_string_width(text) > CONTENT_W and fs > 6.0:
                fs -= 0.5; self.set_font("MONO", "", fs)
            lines = [text]
        else:
            lines = self._wrap(text, size, style)
        for ln in lines:
            if self.get_y() + lh > PAGE_H - BOT:
                self._newpage()
            y = self.get_y()
            if number and self.numbering:
                self.lineno += 1
                self.set_font("DJ", "", 7)
                self.set_text_color(150)
                self.set_xy(NUM_X, y + (lh - 3) / 2)
                self.cell(12, 3, str(self.lineno), align="R")
                self.set_text_color(0)
            if mono:
                self.set_font("MONO", "", fs)
            else:
                self.set_font("DJ", style, size)
            self.set_xy(LEFT, y)
            self.cell(CONTENT_W, lh, ln)
            self.set_xy(LEFT, y + lh)
        self.set_y(self.get_y() + gap_after)

    def figures(self):
        import matplotlib.image as mpimg
        for cap, path in FIGS:
            self._newpage()
            self.numbering = False
            cap_y = TOP + 120
            if os.path.exists(path):
                h, w = mpimg.imread(path).shape[:2]
                disp_h = CONTENT_W * (h / w)
                self.image(path, x=LEFT, y=TOP + 4, w=CONTENT_W)
                cap_y = TOP + 4 + disp_h + 5
            self.set_xy(LEFT, cap_y)
            self.set_font("DJ", "I", 9.5)
            self.multi_cell(CONTENT_W, 5, strip_md(cap))


def build(src="MANUSCRIPT.md", out="MANUSCRIPT.pdf", with_figures=True):
    doc = Doc()
    with open(os.path.join(HERE, src), encoding="utf-8") as f:
        raw = f.read().split("\n")
    para = []
    def flush():
        # reflow accumulated body lines into ONE paragraph (single newlines are not breaks)
        if para:
            doc.emit(strip_md(" ".join(para)), size=10.5, style="", lh=5.0)
            para.clear()

    for line in raw:
        s = line.rstrip()
        if not s.strip():
            flush(); doc.set_y(doc.get_y() + 1.6)
            continue
        if s.startswith("# "):
            flush(); doc.emit(strip_md(s[2:]), size=15, style="B", lh=7.2, gap_before=1, gap_after=3)
        elif s.startswith("## "):
            flush(); doc.emit(strip_md(s[3:]), size=12.5, style="B", lh=6.0, gap_before=3, gap_after=1.6)
        elif s.startswith("### "):
            flush(); doc.emit(strip_md(s[4:]), size=11, style="B", lh=5.6, gap_before=2, gap_after=1.2)
        elif re.match(r"^\s{2,}\S", line):           # preformatted table row
            flush(); doc.emit(line.strip(), size=8, mono=True, lh=4.4, gap_after=0.2)
        elif s.strip().startswith("*") and s.strip().endswith("*"):
            flush(); doc.emit(strip_md(s), size=9, style="I", lh=4.6, gap_after=1.4)
        else:
            para.append(s.strip())
    flush()
    if with_figures:
        doc.figures()
    outp = os.path.join(HERE, out)
    doc.output(outp)
    print("wrote", outp, "pages:", doc.page, "numbered lines:", doc.lineno)


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        build(sys.argv[1], sys.argv[2], with_figures=("--no-figures" not in sys.argv))
    else:
        build()
