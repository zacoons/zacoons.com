from os import listdir
from os.path import exists
from markdown import markdown
from datetime import datetime
from bs4 import BeautifulSoup
from re import findall, finditer
from minify_html import minify

# posts

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

# templating

class Extraction:
    def __init__(self, inner: str, inner_with_tags: str, new_html: str):
        self.inner = inner
        self.inner_with_tags = inner_with_tags
        self.new_html = new_html

def extract(pattern: str, page_html: str) -> Extraction:
    matches = list(finditer(pattern, page_html))
    if len(matches):
        start = matches[0]
        end = matches[-1]
        return Extraction(
            page_html[start.end(0):end.start(0)],
            page_html[start.start(0):end.end(0)],
            page_html[:start.start(0)] + page_html[end.end(0):]
        )
    return Extraction("", "", page_html)

def apply_post_vars_factory(post: Post):
    def apply(html: str) -> str:
        for key, value in post.__dict__.items():
            html = html.replace("{{" + str(key) + "}}", str(value))
        return html
    return apply

def insert_post_lists(page_html: str) -> str:
    with open("templates/postList.html", "r", encoding="utf8") as list_file:
        list_html = list_file.read()
    extraction = extract("\+item\+", list_html)
    page_html_matches = findall("({{posts(.*?)}})", page_html)
    for match in page_html_matches:
        items_html = ""
        max_count = int(match[1]) if match[1] else None
        for post in get_posts(max_count):
            items_html += apply_post_vars_factory(post)(extraction.inner)
        current_list_html = list_html.replace(extraction.inner_with_tags, items_html)
        page_html = page_html.replace(match[0], current_list_html)
    return page_html

def apply_var(page_html: str) -> str:
    with open(".var", encoding="utf8") as var_file:
        for line in var_file.readlines():
            key_value_pair = line.split("=", 1)
            page_html = page_html.replace("{{" + key_value_pair[0] + "}}", key_value_pair[1])
    return page_html

def apply_template(page_filepath: str, apply_vars_fn=None) -> str:
    with open("templates/page.html", "r", encoding="utf8") as template_file:
        template_html = template_file.read()

    with open(page_filepath, "r", encoding="utf8") as page_file:
        page_html = page_file.read()
    page_html = insert_post_lists(page_html)
    head_extraction = extract("\+head\+", page_html)
    page_html = head_extraction.new_html
    if page_filepath.endswith(".md"):
        page_html = "<article>" + markdown(page_html) + "</article>"
    
    template_html = template_html.replace("{{head_append}}", head_extraction.inner)
    template_html = template_html.replace("{{page_html}}", page_html)
    template_html = apply_var(template_html)
    if apply_vars_fn:
        template_html = apply_vars_fn(template_html)
    return minify(template_html, do_not_minify_doctype=True, ensure_spec_compliant_unquoted_attribute_values=True, keep_spaces_between_attributes=True)