import feedparser
FEEDS = {
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "football": "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "spain": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
}
def fetch_section(section, url, limit=5):
    """Return a list of article dicts for one feed."""
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:limit]:
        article = {
            "section":section,
            "source":feed.feed.title,
            "title":entry.title,
            "link":entry.link,
            "published":entry.get("published", ""),
        }
        articles.append(article)
        pass
    return articles

def fetch_all():
    all_articles = []
    for section, url in FEEDS.items():
        all_articles.extend(fetch_section(section, url))
        pass
    return all_articles

if __name__ == "__main__":
    articles = fetch_all()
    for a in articles:
        print(f"[{a['section']}] {a['title']}  ({a['source']})")
    print(f"\nTotal: {len(articles)} articles")