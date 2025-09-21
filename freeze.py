import os, shutil, subprocess
from flask_frozen import Freezer
from app import app, scriptPath

build_dir = f"{scriptPath}/build"
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

freezer = Freezer(app)
os.makedirs(build_dir, exist_ok=True)
freezer.freeze()

# Checking that freeze worked well.
if not os.path.isdir(build_dir):
    raise RuntimeError("❌ build/ directory is not found. Aborting publishing...")

# Remembering the current branch. It should be "main".
current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
static_branch_exists = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/static"]).returncode==0
if static_branch_exists:
    subprocess.run(["git", "checkout", "static"], check=True)