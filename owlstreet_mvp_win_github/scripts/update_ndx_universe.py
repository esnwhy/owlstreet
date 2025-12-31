# scripts/update_ndx_universe.py
import json
import pathlib
import requests

OUT = pathlib.Path("data/nasdaq100.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

URL = "https://api.nasdaq.com/api/quote/list-type/nasdaq100"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nasdaq.com/",
}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    j = r.json()

    rows = (j.get("data") or {}).get("rows") or []
    universe = []
    for x in rows:
        universe.append(
            {
                "symbol": (x.get("symbol") or "").upper(),
                "name": x.get("name"),
                "sector": x.get("sector"),
                "industry": x.get("industry"),
            }
        )

    universe = [u for u in universe if u["symbol"]]
    OUT.write_text(json.dumps(universe, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(universe)} tickers -> {OUT}")

if __name__ == "__main__":
    main()
