"""月次トークン有効期限チェック"""
import sys
import requests
from utils import get_logger, get_threads_credentials

logger = get_logger("token_check")
BASE_URL = "https://graph.threads.net/v1.0"

def check_token():
    access_token, user_id = get_threads_credentials()
    logger.info("トークン有効性チェック開始...")
    try:
        resp = requests.get(f"{BASE_URL}/me", params={"access_token": access_token}, timeout=30)
    except requests.RequestException as e:
        logger.error(f"接続エラー: {e}")
        sys.exit(1)
    if resp.status_code == 200:
        data = resp.json()
        logger.info(f"OK トークン有効: user_id={data.get('id')}")
    else:
        error = resp.json().get("error", {})
        logger.error(f"トークン無効: {resp.status_code} {error.get('message','unknown')}")
        logger.error("対処: Meta Developer でトークン再生成 → GitHub Secrets 更新")
        sys.exit(1)
    try:
        debug_resp = requests.get(f"{BASE_URL}/access_token",
            params={"grant_type":"th_exchange_token","client_secret":"CHECK_ONLY","access_token":access_token}, timeout=30)
        if debug_resp.status_code == 200:
            expires_in = debug_resp.json().get("expires_in")
            if expires_in:
                days = expires_in // 86400
                logger.info(f"トークン残り: {days} 日")
                if days <= 7:
                    logger.error(f"残り{days}日！即座に更新してください")
                    sys.exit(1)
                elif days <= 30:
                    logger.warning(f"残り{days}日 — 30日以内に更新推奨")
    except Exception:
        pass
    logger.info("トークンチェック完了")

if __name__ == "__main__":
    check_token()
