import feedparser
URL="https://feeds.bbci.co.uk/news/world/rss.xml"
feed=feedparser.parse(URL)
articles=feed.entries[:5]
for article in articles:
    print(article.title)
