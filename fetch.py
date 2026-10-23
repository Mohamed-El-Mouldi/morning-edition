import feedparser
import json
from datetime import date
from pathlib import Path

FEEDS = {
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "football": "https://feeds.bbci.co.uk/sport/football/rss.xml",
    "spain": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
}
def fetch_section(section, url, limit=5):
    """Return a list of article dicts for one feed."""
    feed = feedparser.parse(url)
    if feed.bozo and not feed.entries:
        print(f"⚠ couldn't read {section} feed: {feed.bozo_exception}")
        return []
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

DATA_DIR = Path("data")

def save_articles(articles, path):
    """Write the list of articles to a JSON file."""
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

def load_articles(path):
    """Read the list of articles back from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    articles = fetch_all()
    path = DATA_DIR / f"{date.today().isoformat()}.json"
    save_articles(articles, path)
    print(f"Saved {len(articles)} articles to {path}")

    # Check that it worked by reading the file back
    loaded = load_articles(path)
    print(f"Loaded {len(loaded)} articles back. First one:")
    print(loaded[0]["title"])