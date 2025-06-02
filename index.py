import os
import requests
import feedparser
import xml.etree.ElementTree as ET
import json
from dotenv import load_dotenv

# === CONFIG ===
MAX_ITEMS_PER_FEED = 10
OUTPUT_FILE = "NFeed_Live.json"

# === LOAD ENV ===
load_dotenv()
opml_url = os.getenv("FEED_URL")

if not opml_url:
    print("❌ FEED_URL non trovato nel file .env")
    exit(1)

# === DOWNLOAD OPML ===
print(f"📥 Scarico OPML da: {opml_url}")
opml_data = requests.get(opml_url).text

# === PARSE OPML ===
feeds = []
try:
    root = ET.fromstring(opml_data)
    for outline in root.findall(".//outline"):
        url = outline.attrib.get("xmlUrl")
        title = outline.attrib.get("title") or outline.attrib.get("text")
        if url:
            feeds.append({"title": title, "url": url})
except Exception as e:
    print(f"❌ Errore parsing OPML: {e}")
    exit(1)

print(f"🎯 Trovati {len(feeds)} feed nel file OPML.")

# === FETCH RSS ===
all_items = []
for feed in feeds:
    print(f"🔄 {feed['title']} → {feed['url']}")
    try:
        parsed = feedparser.parse(feed['url'])
        entries = parsed.entries[:MAX_ITEMS_PER_FEED]
        for entry in entries:
            item = {
                "titolo": entry.get("title", ""),
                "data": entry.get("published", entry.get("updated", "")),
                "fonte": parsed.feed.get("title", feed["title"]),
                "autore": entry.get("author", "Anonimo"),
                "link": entry.get("link", "")
            }
            all_items.append(item)
    except Exception as e:
        print(f"⚠️ Errore nel feed {feed['url']}: {e}")

# === SALVA JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

print(f"✔️ Salvato in {OUTPUT_FILE} con {len(all_items)} articoli totali.")
