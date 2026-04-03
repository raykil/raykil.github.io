"""
summarize.py — Generate one-line summaries for each article using Claude.

Usage:
    python summarize.py

Reads every .ipynb in articles/<dirname>/, extracts the text, calls the
Claude API, and writes summaries to static/summaries.json.
Run this once whenever you add or update an article.
"""

import json
import os
import re
from pathlib import Path

import anthropic

ARTICLES_DIR = Path("articles")
OUTPUT_FILE  = Path("static/summaries.json")
MODEL        = "claude-opus-4-6"


def extract_notebook_text(ipynb_path: Path) -> str:
    """Pull all markdown and code-cell source text out of a notebook."""
    with open(ipynb_path, encoding="utf-8") as f:
        nb = json.load(f)

    parts = []
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))
        if source.strip():
            parts.append(source)

    return "\n\n".join(parts)


def summarize(text: str, client: anthropic.Anthropic) -> str:
    """Ask Claude for one intriguing sentence that captures the article."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=128,
        system=(
            "You are a science communicator writing teaser copy for a researcher's blog. "
            "Given the content of an article, write exactly ONE sentence — "
            "curious, precise, and a little provocative — that makes a reader want to read more. "
            "No preamble, no quotes, just the sentence."
        ),
        messages=[
            {"role": "user", "content": f"Article content:\n\n{text[:6000]}"}
        ],
    )
    return response.content[0].text.strip()


def main():
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    summaries = {}

    # Load existing summaries so we don't re-generate unchanged articles
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, encoding="utf-8") as f:
            summaries = json.load(f)

    for article_dir in sorted(ARTICLES_DIR.iterdir()):
        if not article_dir.is_dir():
            continue

        dirname = article_dir.name
        notebooks = list(article_dir.glob("*.ipynb"))
        if not notebooks:
            print(f"  [skip] {dirname} — no .ipynb found")
            continue

        if dirname in summaries:
            print(f"  [skip] {dirname} — already summarized")
            continue

        print(f"  [summarize] {dirname} ...")
        text = extract_notebook_text(notebooks[0])
        if not text.strip():
            print(f"  [skip] {dirname} — empty notebook")
            continue

        summary = summarize(text, client)
        summaries[dirname] = summary
        print(f"    → {summary}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(summaries)} summaries saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
