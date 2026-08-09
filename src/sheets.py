"""Google Sheets 操作モジュール"""
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
JST = ZoneInfo("Asia/Tokyo")


class SheetManager:
    """Google Sheets の読み書きを担当"""

    def __init__(self, credentials_json: str, spreadsheet_id: str):
        creds_dict = json.loads(credentials_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        gc = gspread.authorize(creds)
        self.spreadsheet = gc.open_by_key(spreadsheet_id)

    def _get_worksheet(self, sheet_name: str):
        """シートを取得"""
        return self.spreadsheet.worksheet(sheet_name)

    @staticmethod
    def _normalize_date(value: str) -> str:
        """Sheets 上の日付表記を YYYY/MM/DD に寄せる。"""
        return str(value).strip().replace("-", "/")

    def get_next_post(self, queue_sheet: str, time_slot: str) -> dict | None:
        """投稿キューからJST基準で次の未投稿を取得する。

        Args:
            queue_sheet: シート名
            time_slot: "morning" or "evening"

        Returns:
            {"row": int, "date": str, "time_slot": str, "text": str,
             "type": str, "neta_id": str} or None
        """
        ws = self._get_worksheet(queue_sheet)
        records = ws.get_all_records()
        today = datetime.now(JST).strftime("%Y/%m/%d")

        for i, row in enumerate(records):
            row_date = self._normalize_date(row.get("投稿日", ""))
            row_slot = str(row.get("時間帯", "")).strip()
            row_posted = str(row.get("投稿済", "")).strip().upper()
            row_text = str(row.get("投稿文", ""))

            if (
                row_date == today
                and row_slot == time_slot
                and row_posted not in ("TRUE", "ERROR")
                and row_text.strip()
            ):
                return {
                    "row": i + 2,  # ヘッダー行 + 0-indexed
                    "date": row_date,
                    "time_slot": row_slot,
                    "text": row_text,
                    "type": str(row.get("種別", "")),
                    "neta_id": str(row.get("ネタID", "")),
                }
        return None

    def mark_as_posted(self, queue_sheet: str, row: int, post_id: str):
        """投稿済みフラグとIDを記録"""
        ws = self._get_worksheet(queue_sheet)
        ws.update_cell(row, 6, "TRUE")    # F列: 投稿済
        ws.update_cell(row, 7, post_id)   # G列: 投稿ID

    def mark_as_error(self, queue_sheet: str, row: int, error_msg: str):
        """エラーを記録"""
        ws = self._get_worksheet(queue_sheet)
        ws.update_cell(row, 6, "ERROR")              # F列: 投稿済
        ws.update_cell(row, 8, error_msg[:200])       # H列: エラー

    def log_post(self, log_sheet: str, post_id: str, text: str,
                 post_type: str, status: str):
        """投稿ログにJSTで記録"""
        ws = self._get_worksheet(log_sheet)
        now = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")
        ws.append_row([now, post_id, text[:50], post_type, status])

    def get_queue_status(self, queue_sheet: str) -> dict:
        """キューの状態を取得"""
        ws = self._get_worksheet(queue_sheet)
        records = ws.get_all_records()
        total = len(records)
        posted = sum(1 for r in records if str(r.get("投稿済", "")).upper() == "TRUE")
        errors = sum(1 for r in records if str(r.get("投稿済", "")).upper() == "ERROR")
        pending = total - posted - errors
        return {
            "total": total,
            "posted": posted,
            "errors": errors,
            "pending": pending,
        }
