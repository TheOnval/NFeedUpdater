from dotenv import load_dotenv
import os
import requests

load_dotenv()
feed_url = os.getenv("FEED_URL")

if not feed_url:
    print("⚠️ Nessun FEED_URL trovato.")
else:
    print(f"🎯 Recupero feed da: {feed_url}")
    response = requests.get(feed_url)
    if response.status_code == 200:
        with open("NFeed_Live.json", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✔️ Feed salvato in NFeed_Live.json")
    else:
        print(f"❌ Errore: {response.status_code}")
