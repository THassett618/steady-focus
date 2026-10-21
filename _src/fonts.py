"""Self-host the two brand fonts as small Latin woff2 files (no Google Fonts round trip, no swap shift).

Run:  python _src/fonts.py   (needs: pip install fonttools brotli)
Out:  fonts/bricolage.woff2 (opsz 12-96, wght 700-800), fonts/atkinson-400.woff2, fonts/atkinson-700.woff2
Both fonts are SIL Open Font License; sources in _src/fonts/.
"""
import io, pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "_src" / "fonts"
OUT = ROOT / "fonts"
OUT.mkdir(exist_ok=True)
LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2190-2193,U+2212,U+2215,U+00A2"


def sub(font, out):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum", "lnum"]
    opts.name_IDs = ["*"]
    s = subset.Subsetter(opts)
    s.populate(unicodes=subset.parse_unicodes(LATIN))
    s.subset(font)
    font.flavor = "woff2"
    font.save(out)
    print(out, out.stat().st_size // 1024, "KB")


f = TTFont(SRC / "Bricolage.ttf")
f = instancer.instantiateVariableFont(f, {"wdth": 100, "wght": (700, 800)})
buf = io.BytesIO(); f.save(buf); buf.seek(0); f = TTFont(buf, lazy=False)
sub(f, OUT / "bricolage.woff2")
sub(TTFont(SRC / "Atkinson-Regular.ttf"), OUT / "atkinson-400.woff2")
sub(TTFont(SRC / "Atkinson-Bold.ttf"), OUT / "atkinson-700.woff2")
