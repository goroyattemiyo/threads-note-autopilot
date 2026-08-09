"""
共通ユーティリティ
"""
import os
import sys
import logging

import gspread
from google.auth import default as google_auth_default

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
    """WIF/ADCで認証し、環境変数で指定したGoogle Sheetsを開く。"""
    spreadsheet_id = require_env("SPREADSHEET_ID")
    credentials, _ = google_auth_default(scopes=SCOPES)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(spreadsheet_id)
