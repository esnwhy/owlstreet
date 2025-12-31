import json
import os
import pathlib
import requests
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DATA_DIR = pathlib.Path("data")
UNIV_PATH = DATA_DIR / "nasdaq100.json"
CIK_PATH = DATA_DIR / "sec_ticker_cik.json"

SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "OwlStreet/0.1 (contact: your_email@example.com)")
SEC_HEADERS = {
    "User-Agent": SEC_USER_AGENT,
    "Accept-Encoding": "gzip, deflate",
}

def load_json(path: pathlib.Path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def sec_get(url: str):
    r = requests.get(url, headers=SEC_HEADERS, timeout=30)
    r.raise_for_status()
    return r.json()

def get_sec_submissions(cik10: str):
    return sec_get(f"https://data.sec.gov/submissions/CIK{cik10}.json")

def get_sec_companyfacts(cik10: str):
    return sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json")

def latest_usd_fact(companyfacts: dict, tag: str):
    """Return latest USD fact for a given us-gaap tag."""
    try:
        items = companyfacts["facts"]["us-gaap"][tag]["units"]["USD"]
    except Exception:
        return None

    items = [x for x in items if isinstance(x, dict) and "end" in x and "val" in x]
    if not items:
        return None

    items.sort(key=lambda x: x["end"])
    x = items[-1]
    return {
        "tag": tag,
        "val": x["val"],
        "end": x["end"],
        "fy": x.get("fy"),
        "fp": x.get("fp"),
        "form": x.get("form"),
    }

@app.get("/api/universe/nasdaq100")
def universe():
    u = load_json(UNIV_PATH)
    if not u:
        raise HTTPException(500, "Nasdaq100 universe not found. Run scripts/update_ndx_universe.py")
    return u

@app.get("/api/ticker/{symbol}")
def ticker_detail(symbol: str):
    symbol = symbol.upper()

    universe = load_json(UNIV_PATH) or []
    cikmap = load_json(CIK_PATH) or {}

    meta = next((x for x in universe if x.get("symbol") == symbol), None)
    if not meta:
        raise HTTPException(404, "Symbol not in Nasdaq 100 universe (or universe not updated).")

    cik = (cikmap.get(symbol) or {}).get("cik")
    if not cik:
        raise HTTPException(404, "CIK not found for this ticker (SEC mapping missing).")

    submissions = get_sec_submissions(cik)
    facts = get_sec_companyfacts(cik)

    highlights = {
        "売上高(最新)": latest_usd_fact(facts, "Revenues"),
        "純利益(最新)": latest_usd_fact(facts, "NetIncomeLoss"),
        "総資産(最新)": latest_usd_fact(facts, "Assets"),
        "現金等(最新)": latest_usd_fact(facts, "CashAndCashEquivalentsAtCarryingValue"),
    }

    recent = (submissions.get("filings") or {}).get("recent") or {}
    filings = []
    forms = recent.get("form", [])
    accn = recent.get("accessionNumber", [])
    filing_dates = recent.get("filingDate", [])
    primary_docs = recent.get("primaryDocument", [])

    for i in range(min(15, len(forms))):
        filings.append(
            {
                "form": forms[i],
                "filingDate": filing_dates[i] if i < len(filing_dates) else None,
                "accessionNumber": accn[i] if i < len(accn) else None,
                "primaryDocument": primary_docs[i] if i < len(primary_docs) else None,
            }
        )

    return {
        "symbol": symbol,
        "name": meta.get("name") or submissions.get("name"),
        "sector": meta.get("sector"),
        "industry": meta.get("industry"),
        "cik": cik,
        "財務ハイライト": highlights,
        "最新提出書類": filings,
    }
