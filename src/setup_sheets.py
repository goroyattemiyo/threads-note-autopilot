import gspread
from google.oauth2.service_account import Credentials
import json
import sys
import os

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SPREADSHEET_ID = "1LBzuBpfMBIFPtnsF9Pbhs9LmC0lBgQSOGTQ5uK1Y_7Y"

def setup():
    creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
    if not creds_json:
        print("ERROR: GOOGLE_SHEETS_CREDENTIALS 環境変数が未設定です")
        sys.exit(1)

    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)

    spreadsheet = gc.open_by_key(SPREADSHEET_ID)
    print(f"スプレッドシート接続完了: {spreadsheet.title}")

    sheets_config = {
        "投稿キュー": ["投稿日", "時間帯", "投稿文", "種別", "ネタID", "投稿済", "投稿ID", "エラー"],
        "ネタストック": ["ID", "日付", "商品名", "ブランド", "価格", "悩み", "フック案", "カテゴリ", "使用済"],
        "投稿ログ": ["投稿日時", "投稿ID", "投稿文", "種別", "ステータス"],
        "インサイト": ["取得日", "投稿ID", "views", "likes", "replies", "reposts", "quotes"],
        "note実績": ["記事タイトル", "公開日", "価格", "累計売上", "PV", "購入数", "購入率", "メモ"],
    }

    existing = [ws.title for ws in spreadsheet.worksheets()]
    print(f"既存シート: {existing}")

    for sheet_name, headers in sheets_config.items():
        if sheet_name in existing:
            ws = spreadsheet.worksheet(sheet_name)
            print(f"  既存シート使用: {sheet_name}")
        else:
            ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers))
            print(f"  新規シート作成: {sheet_name}")

        ws.update([headers], "A1")
        ws.format("A1:{}1".format(chr(64 + len(headers))), {
            "textFormat": {"bold": True},
            "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
        })
        print(f"    ヘッダー設定完了 ({len(headers)}列)")

    # デフォルトの Sheet1 があれば削除
    for ws in spreadsheet.worksheets():
        if ws.title in ["Sheet1", "シート1"]:
            spreadsheet.del_worksheet(ws)
            print(f"  不要シート削除: {ws.title}")

    print("")
    print("=" * 50)
    print("セットアップ完了！")
    print(f"URL: {spreadsheet.url}")
    print("=" * 50)

if __name__ == "__main__":
    setup()
