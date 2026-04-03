import os, shutil, subprocess
from pathlib import Path
from time import strftime

scriptPath = os.path.dirname(os.path.abspath(__file__))
build_dir  = f"{scriptPath}/_site"

# 1) Render the Quarto project to _site/
subprocess.run(["quarto", "render"], cwd=scriptPath, check=True)
if not os.path.isdir(build_dir):
    raise RuntimeError("❌ _site/ directory not found after quarto render. Aborting.")
else:
    print("✅ Quarto render succeeded!")

# 2) Making git worktree called tmp_static
worktree_dir = scriptPath.replace("raykil.github.io", "tmp_static")
if not os.path.exists(worktree_dir):
    subprocess.run(["git", "worktree", "add", worktree_dir, "static"], check=True)

# 3) Cleaning up the worktree except .git
for item in os.listdir(worktree_dir):
    if item == '.git':
        continue
    itempath = f"{worktree_dir}/{item}"
    if os.path.isdir(itempath):
        shutil.rmtree(itempath)
    else:
        os.remove(itempath)

# 4) Unpacking _site/ contents into worktree
for item in os.listdir(build_dir):
    source      = f"{build_dir}/{item}"
    destination = f"{worktree_dir}/{item}"
    if os.path.isdir(source):
        shutil.copytree(source, destination, dirs_exist_ok=True)
    else:
        shutil.copy2(source, destination)
with open(f"{worktree_dir}/.nojekyll", 'w') as f:
    f.write("")

# 5) Pushing worktree to static branch on GitHub
subprocess.run(["git", "-C", worktree_dir, "add", "-A"], check=True)
should_commit = subprocess.run(
    ["git", "-C", worktree_dir, "diff", "--cached", "--quiet"]
).returncode != 0
if should_commit:
    msg = f"Publish static site {strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "-C", worktree_dir, "commit", "-m", msg], check=True)
    subprocess.run(["git", "-C", worktree_dir, "push", "origin", "static"], check=True)
    print("✅ Static site successfully pushed to static branch on GitHub!")
else:
    print("ℹ️  No changes to publish.")

# 6) Removing tmp_static worktree
subprocess.run(["git", "worktree", "remove", "-f", worktree_dir], check=True)
shutil.rmtree(worktree_dir, ignore_errors=True)
