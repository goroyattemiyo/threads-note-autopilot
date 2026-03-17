"""週次インサイト収集"""
import sys
import requests
from datetime import datetime, timezone, timedelta
from utils import get_logger, get_threads_credentials, get_sheets_client

logger = get_logger("insights")
JST = timezone(timedelta(hours=9))
BASE_URL = "https://graph.threads.net/v1.0"
MAX_POSTS = 50

def fetch_insights(thread_id, access_token):
    url = f"{BASE_URL}/{thread_id}/insights"
    params = {"metric": "views,likes,replies,reposts,quotes", "access_token": access_token}
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            result = {}
            for m in resp.json().get("data", []):
                vals = m.get("values", [{}])
                result[m.get("name", "")] = vals[0].get("value", 0) if vals else 0
            return result
        else:
            logger.warning(f"取得失敗 {thread_id}: {resp.status_code}")
            return None
    except requests.RequestException as e:
        logger.warning(f"エラー {thread_id}: {e}")
        return None

def run_insights():
    access_token, _ = get_threads_credentials()
    sp = get_sheets_client()
    log_ws = sp.worksheet("投稿ログ")
    log_rows = log_ws.get_all_records()
    thread_ids = [str(r.get("投稿ID", "")).strip() for r in log_rows if str(r.get("投稿ID", "")).strip()]
    if not thread_ids:
        logger.info("投稿IDなし。終了。")
        return
    thread_ids = thread_ids[-MAX_POSTS:]
    logger.info(f"対象: {len(thread_ids)} 件")
    insight_ws = sp.worksheet("インサイト")
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    success = 0
    for tid in thread_ids:
        metrics = fetch_insights(tid, access_token)
        if metrics:
            row = [now, tid, metrics.get("views",0), metrics.get("likes",0),
                   metrics.get("replies",0), metrics.get("reposts",0), metrics.get("quotes",0)]
            insight_ws.append_row(row, value_input_option="USER_ENTERED")
            success += 1
            logger.info(f"  OK {tid}: views={metrics.get('views',0)} likes={metrics.get('likes',0)}")
    logger.info(f"完了: {success}/{len(thread_ids)} 件")
    if success == 0:
        logger.error("1件も取得できませんでした")
        sys.exit(1)

if __name__ == "__main__":
    run_insights()
