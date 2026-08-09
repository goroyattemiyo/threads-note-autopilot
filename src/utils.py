"""
共通ユーティリティ
"""
import os
import sys
import json
import logging
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def require_env(key):
    value = os.environ.get(key)
    if not value:
        print(f"ERROR: {key} が未設定", file=sys.stderr)
        sys.exit(1)
    return value


def get_threads_credentials():
    """ことばの距離用Threads認証情報を汎用Secret名から取得する。"""
    return require_env("THREADS_ACCESS_TOKEN"), require_env("THREADS_USER_ID")


def get_sheets_client():
    """環境変数で指定したGoogle Sheetsを開く。"""
    creds_json = require_env("GOOGLE_SHEETS_CREDENTIALS")
    spreadsheet_id = require_env("SPREADSHEET_ID")
    creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(spreadsheet_id)
