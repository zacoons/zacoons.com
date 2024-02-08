from utils import get_posts
from urllib.parse import quote_plus

with open("public/.rss", "w") as f:
    f.writelines([
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
        "<rss xmlns:atom=\"http://www.w3.org/2005/Atom\" version=\"2.0\">",
        "<channel>",
            "<atom:link href=\"https://zacoons.com/.rss\" rel=\"self\" type=\"application/rss+xml\"/>"
            "<title>zacoons' blog</title>",
            "<link>https://zacoons.com/blog</link>",
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
                *post.html.splitlines(),
                "]]></description>",
            "</item>"
        ])
    f.writelines([
        "</channel>",
        "</rss>"
    ])