"""
Publishes the website to the static branch on GitHub Pages.
Usage: python publish.py [-q]
  -q / --quarto: re-render Quarto articles before freezing.
Raymond Kil, April 2026
"""

import os, shutil, subprocess, argparse, json
from pathlib import Path
from time import strftime
from flask_frozen import Freezer
from app import app, scriptPath, load_articles

# ── Config ────────────────────────────────────────────────────────────────────
BUILD_DIR = Path(scriptPath) / "build"
app.config["FREEZER_DESTINATION"] = str(BUILD_DIR)
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["FREEZER_IGNORE_MIMETYPE_WARNINGS"] = True

freezer = Freezer(app)

@freezer.register_generator
def get_articles_info():
    for dirname in load_articles():
        yield {"dirname": dirname}

@freezer.register_generator
def article_files():
    articles_dir = Path(scriptPath) / "quarto_articles" / "articles"
    for dirname in load_articles():
        files_dir = articles_dir / dirname / "index_files"
        if files_dir.exists():
            for f in files_dir.rglob("*"):
                if f.is_file():
                    yield {"dirname": dirname, "filename": str(f.relative_to(files_dir))}

# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--quarto", action="store_true", help="Re-render Quarto articles before freezing.")
    args = parser.parse_args()

    # 1) Optionally re-render Quarto articles
    if args.quarto:
        print("🔄 Rendering Quarto articles...")
        subprocess.run(["quarto", "render"], cwd=scriptPath, check=True)
        print("✅ Quarto render done.")

    # 2) Freeze Flask app to static HTML
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    print("❄️  Freezing Flask app...")
    freezer.freeze()
    print("✅ Freeze done.")

    # 3) Set up git worktree pointing at the static branch
    worktree_dir = str(scriptPath).replace("raykil.github.io", "tmp_static")
    if not os.path.exists(worktree_dir):
        subprocess.run(["git", "worktree", "add", worktree_dir, "static"], check=True)

    # 4) Clean worktree (keep .git)
    for item in os.listdir(worktree_dir):
        if item == ".git":
            continue
        p = os.path.join(worktree_dir, item)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    # 5) Copy build output into worktree
    for item in os.listdir(BUILD_DIR):
        src = BUILD_DIR / item
        dst = Path(worktree_dir) / item
        shutil.copytree(src, dst, dirs_exist_ok=True) if src.is_dir() else shutil.copy2(src, dst)

    Path(worktree_dir, ".nojekyll").write_text("")

    # 6) Commit and push
    subprocess.run(["git", "-C", worktree_dir, "add", "-A"], check=True)
    has_changes = subprocess.run(
        ["git", "-C", worktree_dir, "diff", "--cached", "--quiet"]
    ).returncode != 0

    if has_changes:
        msg = f"Publish static site {strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "-C", worktree_dir, "commit", "-m", msg], check=True)
        subprocess.run(["git", "-C", worktree_dir, "push", "origin", "static"], check=True)
        print("✅ Published to static branch on GitHub!")
    else:
        print("ℹ️  No changes to publish.")

    # 7) Clean up worktree
    subprocess.run(["git", "worktree", "remove", "-f", worktree_dir], check=True)
    shutil.rmtree(worktree_dir, ignore_errors=True)
