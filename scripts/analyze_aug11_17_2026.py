import os
import json
import requests
import gspread
from google.auth import default as google_auth_default

SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
TARGET_DATES = {f"2026/08/{d:02d}" for d in range(11,18)}
BASE_URL = "https://graph.threads.net/v1.0"


def norm_date(v):
    return str(v or "").strip().replace("-", "/")


def fetch_metrics(post_id):
    r = requests.get(
        f"{BASE_URL}/{post_id}/insights",
        params={"metric":"views,likes,replies,reposts,quotes","access_token":ACCESS_TOKEN},
        timeout=30,
    )
    r.raise_for_status()
    out = {"views":0,"likes":0,"replies":0,"reposts":0,"quotes":0}
    for metric in r.json().get("data", []):
        values = metric.get("values", [])
        out[metric.get("name")] = values[0].get("value",0) if values else 0
    return out


def main():
    creds, _ = google_auth_default(scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    rows = ss.worksheet("投稿キュー").get_all_records()
    results = []
    for row in rows:
        date = norm_date(row.get("投稿日"))
        if date not in TARGET_DATES:
            continue
        post_id = str(row.get("投稿ID","")).strip()
        if not post_id:
            continue
        try:
            m = fetch_metrics(post_id)
        except Exception as e:
            m = {"error": str(e)}
        results.append({
            "date": date,
            "slot": str(row.get("時間帯","")).strip(),
            "text": str(row.get("投稿文","")).strip(),
            "type": str(row.get("種別","")).strip(),
            "neta_id": str(row.get("ネタID","")).strip(),
            "post_id": post_id,
            **m,
        })
    results.sort(key=lambda x: (x["date"], x["slot"]))
    os.makedirs("data", exist_ok=True)
    with open("data/aug11_17_reactions_2026.json","w",encoding="utf-8") as f:
        json.dump(results,f,ensure_ascii=False,indent=2)
    print(f"count={len(results)}")
    for r in results:
        if "error" in r:
            print(r["date"],r["slot"],"ERROR",r["error"])
        else:
            print(r["date"],r["slot"],r["views"],r["likes"],r["replies"],r["reposts"],r["quotes"],r["text"][:35].replace("\n"," "))

if __name__ == "__main__":
    main()
