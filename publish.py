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
else:
    print("✅ Freezing worked well!")

# Remembering the current branch. It should be "main".
# current_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
# static_branch_exists = subprocess.run(["git", "show-ref", "--verify", "--quiet", "refs/heads/static"]).returncode==0
# if static_branch_exists:
#     # let's first assume every changes are pushed and we are not getting git stash issue.
#     subprocess.run(["git", "checkout", "static"], check=True)
#     subprocess.run(["git", "rm", "-rf", "."], check=False)
#     subprocess.run(["git", "clean", "-fdx", "-e", "build"], check=False)

#     for item in os.listdir(build_dir):
#         print("item:", item)
#         # shutil.copytree(f"{build_dir}/{item}", dst, dirs_exist_ok=True)