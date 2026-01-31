from os import popen, path, mkdir
from shutil import rmtree, copytree
from json import load

# Read the lock file
upstream_url = "https://github.com/0x24a/AmiaBlog.git"

with open('amiablog.lock', 'r') as f:
    lock = load(f)
    upstream_version = lock['version']

print(f"Performing AmiaBlog build with version \"{upstream_version}\".")
if path.exists("build"):
    print("- Remove previous build artifacts")
    rmtree("build")
print("- Creating build directory")
mkdir("build")
print("- Pulling upstream repository")
popen(f"git clone {upstream_url} build/AmiaBlog/").read()
if upstream_version != "latest":
    print("- Checking out specific version")
    popen(f"cd build/AmiaBlog && git checkout {upstream_version}").read()
print("- Removing posts in the build directory")
rmtree("build/AmiaBlog/posts")
print("- Copying posts to the build directory")
copytree("posts", "build/AmiaBlog/posts")
print("- Removing attachments in the build directory")
rmtree("build/AmiaBlog/attachments")
print("- Copying attachments to the build directory")
copytree("attachments", "build/AmiaBlog/attachments")