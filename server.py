from bottle import Bottle, static_file, template, abort, HTTPError
from os import listdir
from os.path import exists
from utils import get_post, get_posts, conf, get_description
from markdown import markdown

app = Bottle()

def apply_template(base: str):
    base_lines = base.splitlines()
    page_props = base_lines[0].split(" ;z; ")
    base = "".join(base_lines[1:])
    return template("template.html",
        base=base,
        title=page_props[0],
        description=page_props[1],
        stylesheet=page_props[2] if len(page_props) > 2 else "",
        updated_date=conf.UPDATED_DATE)

def get_html_page(filename, **kwargs):
    base = template("pages/" + filename + ".html", **kwargs)
    return apply_template(base)

@app.get("/")
def home():
    return get_html_page("home",
        featured=conf.FEATURED,
        featured_o=conf.FEATURED_O,
        featured_y=conf.FEATURED_Y,
        posts=get_posts(5))

@app.get("/blog")
def blog():
    return get_html_page("blog", posts=get_posts())

@app.get("/blog/<postname>")
def post(postname):
    p = get_post(postname + ".md")
    if not p:
        abort(404)
    return get_html_page("post",
        title=p.title,
        description=get_description(p.html),
        datestr=p.datestr,
        content=p.html)

@app.get("/<route:path>")
def base_handler(route: str):
    if exists("pages/" + route + ".html"):
        return get_html_page(route)
    
    md_filepath = "pages/" + route + ".md"
    if exists(md_filepath):
        with open(md_filepath) as file:
            file_text_lines = file.read().splitlines()
            inner_html = markdown("\n".join(file_text_lines[1:]))
            base = file_text_lines[0] + "\n<article class='width'>" + inner_html + "</article>"
            return apply_template(base)
    
    return static_file(route, root="public")

@app.error(404)
def error404(error: HTTPError):
    return get_html_page("404")

if __name__ == "__main__":
    app.run(debug=True)