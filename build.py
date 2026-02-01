from os import popen, path, mkdir, remove
from shutil import rmtree, copytree, copy
from loguru import logger
from json import load

# Read the lock file
upstream_url = "https://github.com/0x24a/AmiaBlog.git"

with open("amiablog.lock", "r") as f:
    lock = load(f)
    upstream_version = lock["version"]

logger.info(f'Performing AmiaBlog build with version "{upstream_version}".')
if path.exists("build"):
    logger.warning("Remove previous build artifacts")
    rmtree("build")
logger.info("Creating build directory")
mkdir("build")
logger.info("Pulling upstream repository")
popen(f"git clone {upstream_url} build/AmiaBlog/").read()
if upstream_version != "latest":
    logger.info("Checking out specific version")
    popen(f"cd build/AmiaBlog && git checkout {upstream_version}").read()
logger.info("Copying build assets")
rmtree("build/AmiaBlog/posts")
copytree("posts", "build/AmiaBlog/posts")
rmtree("build/AmiaBlog/attachments")
copytree("attachments", "build/AmiaBlog/attachments")
remove("build/AmiaBlog/config.json")
copy("config.json", "build/AmiaBlog/config.json")
logger.info("Initializing virtual environment")
popen("cd build/AmiaBlog && uv sync").read()
logger.info("Running static build")
popen("cd build/AmiaBlog && uv run staticify.py").read()
if path.exists("dist"):
    logger.warning("Removing previous distribution")
    rmtree("dist")
logger.info("Copying back the distribution")
copytree("build/AmiaBlog/dist", "dist")
logger.info("Cleaning up")
rmtree("build")
logger.info("Done")
