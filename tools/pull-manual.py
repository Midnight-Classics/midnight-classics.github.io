"""Copy the finished booklet from the Tachometer repo into this site.

Copies index.html, manual.css, manual.pdf and every picture that index.html
references (frames/*.png, the back-page SVG) from the Tachometer repo's
docs/manual folder into docs/booklet/ here, so a booklet rebuild is a
one-command refresh:

    python tools/pull-manual.py
    python tools/pull-manual.py "D:/somewhere/else/Tachometer/docs/manual"

The source is only ever read. manual.css is copied unchanged; the only change
made to the copy of index.html is one extra <link> to web.css (this site's own
wrapper stylesheet, which scales the 134 mm pages down to a phone's width).
web.css is never touched by this script.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

DEFAULT_SOURCE = Path(
    r"C:\Users\chees\OneDrive\Documents\Projects\Austin Sprite"
    r"\Gauge Prototypes\Tachometer\docs\manual"
)
REPO = Path(__file__).resolve().parent.parent
DEFAULT_DEST = REPO / "docs" / "booklet"

WRAPPER_LINK = '<link rel="stylesheet" href="web.css">'
CSS_LINK = re.compile(r'(<link[^>]*href="manual\.css"[^>]*>)')
SRC_ATTR = re.compile(r'\bsrc="([^"]+)"')


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE,
                    help="the Tachometer repo's docs/manual folder (default: %(default)s)")
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST,
                    help="where the site serves the booklet from (default: %(default)s)")
    args = ap.parse_args()
    src, dest = args.source.resolve(), args.dest.resolve()

    html_path = src / "index.html"
    if not html_path.is_file():
        print(f"error: no index.html in {src}", file=sys.stderr)
        return 1
    html = html_path.read_text(encoding="utf-8")

    # every local file the booklet's HTML points at (pictures in frames/)
    pictures = sorted({s for s in SRC_ATTR.findall(html) if "://" not in s and not s.startswith("data:")})
    missing = [p for p in pictures + ["manual.css", "manual.pdf"] if not (src / p).is_file()]
    if missing:
        print("error: the source is missing: " + ", ".join(missing), file=sys.stderr)
        return 1

    # refresh: clear the old frames so a renamed picture does not linger
    frames = dest / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    dest.mkdir(parents=True, exist_ok=True)

    for rel in pictures + ["manual.css", "manual.pdf"]:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src / rel, target)

    if WRAPPER_LINK not in html:
        html, n = CSS_LINK.subn(r"\1\n" + WRAPPER_LINK, html, count=1)
        if n != 1:
            print("error: could not find the manual.css <link> to add web.css after", file=sys.stderr)
            return 1
    (dest / "index.html").write_text(html, encoding="utf-8", newline="\n")

    if not (dest / "web.css").is_file():
        print(f"warning: {dest / 'web.css'} is missing; the booklet will not scale on phones", file=sys.stderr)

    print(f"copied index.html, manual.css, manual.pdf and {len(pictures)} pictures")
    print(f"  from {src}")
    print(f"  to   {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
