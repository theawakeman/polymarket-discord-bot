import os
import time
import json
import requests

API_URL = os.getenv("POLYMARKET_API", "https://clob.polymarket.com/markets")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")  # REQUIRED
POLL_SEC = int(os.getenv("POLYMARKET_POLL_SEC", "60"))
KEYWORDS = [k.strip().lower() for k in os.getenv("KEYWORDS", "").split(",") if k.strip()]
STATE_FILE = os.getenv("STATE_FILE", "state.json")

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()

def save_state(known):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(list(known), f)
    except Exception as e:
        print("WARN: could not persist state:", e)

def passes_filter(market):
    if not KEYWORDS:
        return True
    q = (market.get("question") or market.get("title") or "").lower()
    return any(k in q for k in KEYWORDS)

def build_url(market):
    # Try to use provided URL if any; else construct from slug if available
    if "url" in market and market["url"]:
        return market["url"]
    slug = market.get("slug") or ""
    if slug:
        return f"https://polymarket.com/event/{slug}"
    return ""

def send_discord_alert(market):
    if not DISCORD_WEBHOOK:
        print("ERROR: DISCORD_WEBHOOK is not set.")
        return
    title = market.get("question") or market.get("title") or "Nuevo mercado"
    url = build_url(market)
    content = f"🆕 **Nuevo mercado en Polymarket**\n**{title}**\n{url}"
    payload = {"content": content}
    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        if r.status_code >= 300:
            print("Discord webhook error:", r.status_code, r.text[:200])
    except Exception as e:
        print("Discord request failed:", e)

def fetch_markets():
    try:
        r = requests.get(API_URL, timeout=15)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            return data
        return data.get("markets", [])
    except Exception as e:
        print("Fetch error:", e)
        return []

def main():
    known = load_state()
    print("Bot iniciado. Poll:", POLL_SEC, "s. Filtro KEYWORDS:", KEYWORDS)
    first_cycle = True
    while True:
        markets = fetch_markets()
        new_any = False
        for m in markets:
            mid = str(m.get("id") or m.get("_id") or m.get("slug") or m.get("question"))
            if not mid:
                continue
            if mid not in known and passes_filter(m):
                if not first_cycle:
                    send_discord_alert(m)
                known.add(mid)
                new_any = True
        if new_any:
            save_state(known)
            first_cycle = False
        time.sleep(POLL_SEC)

if __name__ == "__main__":
    main()
