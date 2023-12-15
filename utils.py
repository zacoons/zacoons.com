from os import listdir
from os.path import exists, join
from pathlib import Path
from markdown import markdown
from datetime import datetime
from urllib.parse import quote_plus
from bottle import abort

class Post:
    def __init__(self, filepath):
        self.postname = Path(filepath).stem
        postname_parts = self.postname.split("-")
        self.title = " ".join(postname_parts[3:])
        self.date = datetime(*map(int, postname_parts[:3]))
        self.datestr = self.date.strftime("%d %b %Y")
        self.content = markdown(open(filepath).read())
   
def get_post(filename):
    filepath = "posts/" + filename
    if(not exists(filepath)):
        abort(404)
        return
    return Post(filepath)

def get_posts(max_count=0):
    posts = []
    filenames = listdir("posts")
    if max_count:
        filenames = filenames[:max_count]
    for filename in reversed(filenames):
        posts.append(get_post(filename))
    return posts

def gen_rss():
    with open("public/rss.xml", "w") as f:
        f.writelines([
            "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
            "<rss xmlns:atom=\"http://www.w3.org/2005/Atom\" version=\"2.0\">",
            "<channel>",
                "<atom:link href=\"https://zacoons.com/rss.xml\" rel=\"self\" type=\"application/rss+xml\"/>"
                "<title>zacoons' blog</title>",
                "<link>https://zacoons.com/</link>",
                "<description>Recent posts on zacoons' blog</description>",
                "<language>en</language>",
            
        ])
        for post in get_posts(5):
            datestr = post.date.strftime("%a, %d %b %Y %H:%M:%S")
            f.writelines([
                "<item>",
                    "<title>{0}</title>".format(post.title),
                    "<link>https://zacoons.com/blog/{0}</link>".format(quote_plus(post.postname)),
                    "<guid>https://zacoons.com/blog/{0}</guid>".format(quote_plus(post.postname)),
                    "<pubDate>{0} +0000</pubDate>".format(datestr),
                    "<author>zac@zacoons.com (Zac)</author>",
                    "<description><![CDATA[",
                    *post.content.splitlines(),
                    "]]></description>",
                "</item>"
            ])
        f.writelines([
            "</channel>",
            "</rss>"
        ])