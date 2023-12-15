from bottle import Bottle, static_file, template
from os import listdir
from json import loads
from bs4 import BeautifulSoup
from utils import get_post, get_posts

app = Bottle()

def get_page(filename, title, description, stylesheet="", **kwargs):
    base = template("pages/" + filename, **kwargs)
    conf = loads(open("conf.json").read())
    return template("template.html",
        base=base,
        title=title,
        description=description,
        stylesheet=stylesheet,
        updated_date=conf["updated_date"])

# Pages

@app.get("/")
def home():
    conf = loads(open("conf.json").read())
    return get_page("home.html",
        "zacoons' place",
        "A place of awesome epicness that is very awesome. Includes blog and epic coding.",
        "home.css",
        marquee=conf["marquee"],
        featured=conf["featured"],
        featured_o=conf["featured_o"],
        featured_y=conf["featured_y"],
        posts=get_posts(5))

@app.get("/blog")
def blog():
    return get_page("blog.html",
        "THE BOLG - zacoons' blog",
        "The title is pretty self explanatory. It's my blog: THE BOLG",
        posts=get_posts())

@app.get("/blog/<postname>")
def post(postname):
    p = get_post(postname + ".md")
    bs_content = BeautifulSoup(p.content, features="html.parser")
    p_tag_lines = map(lambda l: l.get_text(), bs_content.findAll("p"))
    return get_page("post.html",
        p.title + " - zacoons' blog",
        " ".join(p_tag_lines)[:130] + "...",
        post_title=p.title,
        datestr=p.datestr,
        content=p.content)

@app.get("/skuare")
def skuare():
    return get_page("skuare.html",
        "Skuare - zacoons' place",
        "A nifty little puzzle game where the goal is to turn all of the tiles green. I dare you to beat size 10.",
        "skuare.css")
    
# Static

@app.error(404)
def error404(error):
    return get_page("404.html",
        "404",
        "Four, oh four, thou art such a daft sum. I bet you can't even find your own thumb.")

@app.get('/<filepath:path>')  
def server_static(filepath):
    return static_file(filepath, root="public")

if __name__ == '__main__':
    app.run(debug=True)