import gen_rss # generates a fresh rss feed
from os import listdir, makedirs
from os.path import isdir, isfile
from utils import *
from shutil import copyfile, copytree, rmtree

rmtree("zacoons.com")
makedirs("zacoons.com")

for filename in listdir("pages"):
    new_file_dirpath = "zacoons.com"
    if not filename == "home.html":
        new_file_dirpath += "/" + ".".join(filename.split(".")[:-1])
        makedirs(new_file_dirpath)
    index_html = apply_template("pages/" + filename)
    with open(new_file_dirpath + "/index.html", "w", encoding="utf8") as index_file:
        index_file.write(index_html)

for post in get_posts():
    new_file_dirpath = "zacoons.com/blog/" + post.postname
    makedirs(new_file_dirpath, exist_ok=True)
    with open(new_file_dirpath + "/index.html", "w", encoding="utf8") as index_file:
        index_file.write(apply_template("templates/post.html", apply_post_vars_factory(post)))

for filename in listdir("public"):
    filepath = "public/" + filename
    if isdir(filepath):
        copytree(filepath, "zacoons.com/" + filename)
    if isfile(filepath):
        copyfile(filepath, "zacoons.com/" + filename)