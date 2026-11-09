# midnight-classics.github.io

The public documentation site for Midnight Classics' Digital Smiths Tach Conversion kit, served at
<https://midnight-classics.github.io/> (the address on the booklet's QR code). It is an MkDocs site with the Material
theme: the pages are Markdown in `docs/`, the printed booklet is served as-is from `docs/booklet/`, and a GitHub
Actions workflow (`.github/workflows/deploy.yml`) builds it with `mkdocs build --strict` and publishes it to GitHub
Pages on every push to `main` (set the repository's Pages source to "GitHub Actions"). To preview locally,
`pip install -r requirements.txt` and run `mkdocs serve`, then open <http://127.0.0.1:8000/>. To refresh the booklet
after rebuilding it in the Tachometer repo, run `python tools/pull-manual.py` (or pass the path to that repo's
`docs/manual` folder if it is somewhere else): it copies `index.html`, `manual.css`, `manual.pdf` and the pictures
into `docs/booklet/`, adds one `<link>` to this site's `web.css` (which scales the pages to a phone's width; the
copied `manual.css` is never edited), and the next `mkdocs build --strict` fails if a page here links a picture
that no longer exists.
