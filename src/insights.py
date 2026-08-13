"""週次インサイト収集 - 投稿内容と反応を紐づけて保存。"""
import sys
from datetime import datetime, timedelta, timezone

import requests

from utils import get_logger, get_sheets_client, get_threads_credentials

logger = get_logger("insights")
JST = timezone(timedelta(hours=9))
BASE_URL = "https://graph.threads.net/v1.0"
MAX_POSTS = 50

LEGACY_INSIGHT_HEADERS = [
    "取得日",
    "投稿ID",
    "views",
    "likes",
    "replies",
    "reposts",
    "quotes",
]

INSIGHT_HEADERS = [
    "取得日",
    "投稿ID",
    "投稿日",
    "時間帯",
    "投稿文",
    "種別",
    "ネタID",
    "views",
    "likes",
    "replies",
    "reposts",
    "quotes",
]


def fetch_insights(thread_id, access_token):
    """Threads APIから投稿単位のインサイトを取得する。"""
    url = f"{BASE_URL}/{thread_id}/insights"
    params = {
        "metric": "views,likes,replies,reposts,quotes",
        "access_token": access_token,
    }
    try:
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            result = {}
            for metric in resp.json().get("data", []):
                values = metric.get("values", [{}])
                result[metric.get("name", "")] = (
                    values[0].get("value", 0) if values else 0
                )
            return result

        logger.warning(f"取得失敗 {thread_id}: {resp.status_code}")
        return None
    except requests.RequestException as exc:
        logger.warning(f"エラー {thread_id}: {exc}")
        return None


def build_post_metadata(spreadsheet, log_rows):
    """投稿IDをキーに、投稿キューの全文・種別・ネタID等を引ける辞書を作る。

    投稿キューに見つからない古い投稿は、投稿ログの短縮本文と種別を
    フォールバックとして使う。
    """
    metadata = {}

    queue_ws = spreadsheet.worksheet("投稿キュー")
    for row in queue_ws.get_all_records():
        thread_id = str(row.get("投稿ID", "")).strip()
        if not thread_id:
            continue
        metadata[thread_id] = {
            "date": str(row.get("投稿日", "")).strip(),
            "time_slot": str(row.get("時間帯", "")).strip(),
            "text": str(row.get("投稿文", "")),
            "type": str(row.get("種別", "")).strip(),
            "neta_id": str(row.get("ネタID", "")).strip(),
        }

    for row in log_rows:
        thread_id = str(row.get("投稿ID", "")).strip()
        if not thread_id or thread_id in metadata:
            continue
        metadata[thread_id] = {
            "date": "",
            "time_slot": "",
            "text": str(row.get("投稿文", "")),
            "type": str(row.get("種別", "")).strip(),
            "neta_id": "",
        }

    return metadata


def ensure_insight_schema(worksheet, metadata):
    """旧7列インサイトを新12列へ安全に移行する。

    既存の取得履歴は残し、投稿IDが投稿キューに存在すれば
    投稿日・時間帯・投稿文・種別・ネタIDも同時に補完する。
    """
    values = worksheet.get_all_values()
    worksheet.resize(cols=len(INSIGHT_HEADERS))

    if not values:
        worksheet.update([INSIGHT_HEADERS], "A1")
        return

    header = [str(value).strip() for value in values[0]]
    if header[: len(INSIGHT_HEADERS)] == INSIGHT_HEADERS:
        return

    if header[: len(LEGACY_INSIGHT_HEADERS)] != LEGACY_INSIGHT_HEADERS:
        raise RuntimeError(
            "インサイトのヘッダーが想定外です。自動移行を中止しました: "
            + " / ".join(header)
        )

    migrated = [INSIGHT_HEADERS]
    for old_row in values[1:]:
        padded = list(old_row) + [""] * max(0, 7 - len(old_row))
        thread_id = str(padded[1]).strip()
        post = metadata.get(thread_id, {})
        migrated.append(
            [
                padded[0],
                thread_id,
                post.get("date", ""),
                post.get("time_slot", ""),
                post.get("text", ""),
                post.get("type", ""),
                post.get("neta_id", ""),
                padded[2],
                padded[3],
                padded[4],
                padded[5],
                padded[6],
            ]
        )

    worksheet.clear()
    worksheet.update(migrated, "A1", value_input_option="USER_ENTERED")
    logger.info(f"インサイト旧スキーマを12列へ移行: {len(migrated) - 1}行")


def run_insights():
    access_token, _ = get_threads_credentials()
    spreadsheet = get_sheets_client()

    log_ws = spreadsheet.worksheet("投稿ログ")
    log_rows = log_ws.get_all_records()
    thread_ids = [
        str(row.get("投稿ID", "")).strip()
        for row in log_rows
        if str(row.get("投稿ID", "")).strip()
    ]
    if not thread_ids:
        logger.info("投稿IDなし。終了。")
        return

    # 同じ投稿IDがログに重複していても1回だけ取得する。
    thread_ids = list(dict.fromkeys(thread_ids))[-MAX_POSTS:]
    logger.info(f"対象: {len(thread_ids)} 件")

    metadata = build_post_metadata(spreadsheet, log_rows)
    insight_ws = spreadsheet.worksheet("インサイト")
    ensure_insight_schema(insight_ws, metadata)

    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    success = 0

    for thread_id in thread_ids:
        metrics = fetch_insights(thread_id, access_token)
        if metrics is None:
            continue

        post = metadata.get(thread_id, {})
        row = [
            now,
            thread_id,
            post.get("date", ""),
            post.get("time_slot", ""),
            post.get("text", ""),
            post.get("type", ""),
            post.get("neta_id", ""),
            metrics.get("views", 0),
            metrics.get("likes", 0),
            metrics.get("replies", 0),
            metrics.get("reposts", 0),
            metrics.get("quotes", 0),
        ]
        insight_ws.append_row(row, value_input_option="USER_ENTERED")
        success += 1
        logger.info(
            f"  OK {thread_id}: "
            f"views={metrics.get('views', 0)} "
            f"likes={metrics.get('likes', 0)} "
            f"replies={metrics.get('replies', 0)} "
            f"reposts={metrics.get('reposts', 0)} "
            f"quotes={metrics.get('quotes', 0)}"
        )

    logger.info(f"完了: {success}/{len(thread_ids)} 件")
    if success == 0:
        logger.error("1件も取得できませんでした")
        sys.exit(1)


if __name__ == "__main__":
    run_insights()
