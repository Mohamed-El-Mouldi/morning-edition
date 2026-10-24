import feedparser
import json
from datetime import date, datetime, timezone
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
            "link": entry.link.split("?")[0],
            "published": parse_date(entry),
        }
        articles.append(article)
    return articles

def fetch_all():
    all_articles = []
    for section, url in FEEDS.items():
        all_articles.extend(fetch_section(section, url))
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

def parse_date(entry):
    """Return the entry's date as an ISO string, or "" if it has none."""
    parsed=entry.get("published_parsed")
    if not date:
        return ""
    return datetime(*parsed[:6], tzinfo=timezone.utc).isoformat()

def remove_duplicates(articles):
    """Keep only the first article for each link."""
    seen = set()
    unique = []
    for article in articles:
        if article["link"] not in seen:
            seen.add(article["link"])
            unique.append(article)
    return unique

def sort_newest_first(articles):
    return sorted(articles, key=lambda a: a["published"], reverse=True)

if __name__ == "__main__":
    articles = fetch_all()
    before = len(articles)
    articles = remove_duplicates(articles)
    articles = sort_newest_first(articles)
    print(f"Fetched {before}, removed {before - len(articles)} duplicates")

    path = DATA_DIR / f"{date.today().isoformat()}.json"
    save_articles(articles, path)
    print(f"Saved {len(articles)} articles to {path}")

    loaded = load_articles(path)
    print("Newest three:")
    for a in loaded[:3]:
        print(f"  {a['published']}  [{a['section']}]  {a['title']}")