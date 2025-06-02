#!/usr/bin/env python3

import feedparser
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# === CONFIG ===
load_dotenv()
JSON_FEED_SOURCE = os.getenv("FEED_URL", "NFeed.json")
OUTPUT_FILE = "NFeed_Live.json"
MAX_ITEMS_PER_FEED = 10


def load_feeds(file_path):
    print(f"📥 Carico feed da {file_path}")
    if file_path.startswith("http"):
        import requests
        res = requests.get(file_path)
        feeds_data = res.json()
    else:
        with open(file_path, encoding="utf-8") as f:
            feeds_data = json.load(f)

    return feeds_data["feeds"]


def fetch_feed_items(feed_url, max_items=10):
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:max_items]:
        items.append({
            "titolo": entry.get("title", ""),
            "data": entry.get("published", entry.get("updated", "")),
            "fonte": feed.feed.get("title", "Unknown"),
            "autore": entry.get("author", "Anonimo"),
            "link": entry.get("link", "")
        })
    return items


def main():
    feeds = load_feeds(JSON_FEED_SOURCE)
    all_items = []
    unique_sources = set()
    print(f"🎯 Trovati {len(feeds)} feed da JSON")

    for feed in feeds:
        print(f"🔄 {feed['titolo']} → {feed['url']}")
        try:
            items = fetch_feed_items(feed['url'], MAX_ITEMS_PER_FEED)
            if items:
                print(f"📦 Articoli trovati: {len(items)}")
                all_items.extend(items)
                unique_sources.add(feed['titolo'])
            else:
                print("⚠️ Nessun articolo disponibile.")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Errore con {feed['url']}: {e}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"\n✔️ Salvato in {OUTPUT_FILE} con {len(all_items)} articoli da {len(unique_sources)} fonti.")


if __name__ == "__main__":
    main()
