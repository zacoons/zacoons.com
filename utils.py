from os import listdir
from os.path import exists
from markdown import markdown
from datetime import datetime
from bs4 import BeautifulSoup

class Post:
    def __init__(self, filepath: str):
        self.postname = filepath.split("/")[-1].replace(".md", "")
        postname_parts = self.postname.split("-")
        self.title = " ".join(postname_parts[3:])
        self.date = datetime(*map(int, postname_parts[:3]))
        self.datestr = self.date.strftime("%d %b %Y")
        with open(filepath) as f:
            self.html = markdown(f.read())

def get_post(filename: str) -> Post:
    filepath = "posts/" + filename
    if not exists(filepath):
        return None
    return Post(filepath)

def get_posts(max_count: int = None) -> list[Post]:
    filenames = list(reversed(listdir("posts")))
    if max_count:
        filenames = filenames[:max_count]
    return [get_post(filename) for filename in filenames]

def get_description(html: str, characters: int = 130) -> str:
    bs = BeautifulSoup(html, features="html.parser")
    p_tag_lines = map(lambda l: l.get_text(), bs.findAll("p"))
    if characters == 0:
        return " ".join(p_tag_lines)
    return " ".join(p_tag_lines)[:characters - 3] + "..."