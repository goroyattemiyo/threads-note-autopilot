"""ことばの距離プロジェクト用 Google Sheets 初期セットアップ。"""
import os
import sys

import gspread
from google.auth import default as google_auth_default

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEETS_CONFIG = {
    "投稿キュー": [
        "投稿日",
        "時間帯",
        "投稿文",
        "種別",
        "ネタID",
        "投稿済",
        "投稿ID",
        "エラー",
    ],
    "ネタストック": [
        "ID",
        "日付",
        "場面",
        "最初の言葉",
        "カテゴリ",
        "フラットな言葉",
        "少し前向きな言葉",
        "視点変更",
        "根拠/出典",
        "使用済",
    ],
    "投稿ログ": [
        "投稿日時",
        "投稿ID",
        "投稿文",
        "種別",
        "ステータス",
    ],
    "インサイト": [
        "取得日",
        "投稿ID",
        "views",
        "likes",
        "replies",
        "reposts",
        "quotes",
    ],
}


def require_env(key: str) -> str:
    value = os.environ.get(key, "")
    if not value:
        print(f"ERROR: {key} 環境変数が未設定です")
        sys.exit(1)
    return value


def setup():
    spreadsheet_id = require_env("SPREADSHEET_ID")
    credentials, _ = google_auth_default(scopes=SCOPES)
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open_by_key(spreadsheet_id)
    print(f"スプレッドシート接続完了: {spreadsheet.title}")

    existing = [ws.title for ws in spreadsheet.worksheets()]
    print(f"既存シート: {existing}")

    for sheet_name, headers in SHEETS_CONFIG.items():
        if sheet_name in existing:
            ws = spreadsheet.worksheet(sheet_name)
            print(f"  既存シート使用: {sheet_name}")
        else:
            ws = spreadsheet.add_worksheet(
                title=sheet_name,
                rows=1000,
                cols=len(headers),
            )
            print(f"  新規シート作成: {sheet_name}")

        ws.update([headers], "A1")
        end_column = chr(64 + len(headers))
        ws.format(
            f"A1:{end_column}1",
            {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9},
            },
        )
        print(f"    ヘッダー設定完了 ({len(headers)}列)")

    for ws in spreadsheet.worksheets():
        if ws.title in ["Sheet1", "シート1"]:
            spreadsheet.del_worksheet(ws)
            print(f"  不要シート削除: {ws.title}")

    print("")
    print("=" * 50)
    print("ことばの距離プロジェクト用セットアップ完了")
    print(f"URL: {spreadsheet.url}")
    print("=" * 50)


if __name__ == "__main__":
    setup()
