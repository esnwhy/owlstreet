# scripts/update_sec_ticker_cik.py
import json
import os
import pathlib
import requests
from dotenv import load_dotenv

load_dotenv()

OUT = pathlib.Path("data/sec_ticker_cik.json")
OUT.parent.mkdir(parents=True, exist_ok=True)

URL = "https://www.sec.gov/files/company_tickers.json"

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "OwlStreet/0.1 (contact: your_email@example.com)")
HEADERS = {
    "User-Agent": SEC_USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    j = r.json()

    m = {}
    for _, v in j.items():
        ticker = (v.get("ticker") or "").upper()
        cik = str(v.get("cik_str") or "").zfill(10)
        if ticker and cik:
            m[ticker] = {"cik": cik, "title": v.get("title")}

    OUT.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {len(m)} tickers -> {OUT}")

if __name__ == "__main__":
    main()
