# raykil.github.io

Published at [https://raykil.github.io](https://raykil.github.io).

## Stack
- **Flask** — routing, templates, and all page rendering
- **Quarto** — converts individual article notebooks (`.ipynb`) to HTML
- **Frozen-Flask** — snapshots the Flask app to static HTML for GitHub Pages

## Development
```
python app.py        # start local server at http://127.0.0.1:5000
python app.py -q     # re-render Quarto articles first, then start server
```

## Adding an Article
1. Create `articles/<name>/` with an `index.qmd` and a `.ipynb` notebook.
2. Add an entry to `articles/index.json`.
3. Run `python app.py -q` to verify locally.

## Publishing
```
python publish.py        # freeze + push to static branch (GitHub Pages)
python publish.py -q     # use -q only when an article was added or changed
```
`publish.py` generates `build/`, which contains the frozen static HTML that gets pushed to the `static` branch and served at `raykil.github.io`. The `build/` directory is gitignored and recreated on every publish.
