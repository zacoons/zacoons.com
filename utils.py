from os import listdir
from os.path import exists, join
from pathlib import Path
from markdown import markdown
from datetime import datetime
from bs4 import BeautifulSoup

# load config
conf = type("", (), {})()
with open(".conf") as conf_file:
    conf_file_lines = conf_file.read().splitlines()
    for line in conf_file_lines:
        key_value_pair = line.split("=", 1)
        setattr(conf, key_value_pair[0], key_value_pair[1])

class Post:
    def __init__(self, filepath):
        self.postname = Path(filepath).stem
        postname_parts = self.postname.split("-")
        self.title = " ".join(postname_parts[3:])
        self.date = datetime(*map(int, postname_parts[:3]))
        self.datestr = self.date.strftime("%d %b %Y")
        with open(filepath) as f:
            self.html = markdown(f.read())
   
def get_post(filename):
    filepath = "posts/" + filename
    if not exists(filepath):
        return None
    return Post(filepath)

def get_posts(max_count=0):
    posts = []
    filenames = listdir("posts")
    if max_count:
        filenames = filenames[:max_count]
    return [get_post(filename) for filename in reversed(filenames)]

def get_description(html, characters=130):
    bs = BeautifulSoup(html, features="html.parser")
    p_tag_lines = map(lambda l: l.get_text(), bs.findAll("p"))
    if characters == 0:
        return " ".join(p_tag_lines)
    return " ".join(p_tag_lines)[:characters - 3] + "..."