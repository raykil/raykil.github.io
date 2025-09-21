import os, shutil
from flask_frozen import Freezer
from app import app, scriptPath

build_dir = f"{scriptPath}/build"
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

freezer = Freezer(app)
os.makedirs(build_dir, exist_ok=True)
freezer.freeze()