import os, shutil, subprocess
from time import strftime
from flask_frozen import Freezer
from app import app, scriptPath

# 1) Freezing the current webpage
build_dir = f"{scriptPath}/build"
if os.path.exists(build_dir): shutil.rmtree(build_dir)
freezer = Freezer(app)
os.makedirs(build_dir, exist_ok=True)
freezer.freeze()
if not os.path.isdir(build_dir):
    raise RuntimeError("❌ build/ directory is not found. Aborting publishing...")
else: print("✅ Freezing worked well!")

# 2) Making git worktree called tmp_static
worktree_dir = scriptPath.replace("raykil.github.io", "tmp_static")
if not os.path.exists(worktree_dir):
    subprocess.run(["git", "worktree", "add", worktree_dir, "static"], check=True)

# 3) Cleaning up the worktree except .git
for item in os.listdir(worktree_dir):
    if item=='.git': continue
    itempath = f"{worktree_dir}/{item}"
    if os.path.isdir(itempath): shutil.rmtree(itempath)
    else: os.remove(itempath)

# 4) Unpacking contents in build to worktree
for item in os.listdir(build_dir):
    source = f"{build_dir}/{item}"
    destination = f"{worktree_dir}/{item}"
    if os.path.isdir(source): shutil.copytree(source, destination, dirs_exist_ok=True)
    else: shutil.copy2(source, destination)
with open(f"{worktree_dir}/.nojekyll", 'w') as f: f.write("")

# 5) Pushing worktree to static branch on GitHub
subprocess.run(["git", "-C", worktree_dir, "add", "-A"], check=True) # git add
should_commit = subprocess.run(["git", "-C", worktree_dir, "diff", "--cached", "--quiet"]).returncode != 0
if should_commit:
    msg = f"Publish static site {strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "-C", worktree_dir, "commit", "-m", msg], check=True) # git commit
    subprocess.run(["git", "-C", worktree_dir, "push", "origin", "static"], check=True) # git push
    print("✅ Static site successfully pushed to static branch on GitHub!")

# 6) Removing tmp_static worktree
subprocess.run(["git", "worktree", "remove", "-f", worktree_dir], check=True)
shutil.rmtree(worktree_dir, ignore_errors=True)