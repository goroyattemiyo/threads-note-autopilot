"""Threads API ラッパー"""
import time
import requests


class ThreadsAPI:
    """Threads Graph API との通信を担当"""

    BASE_URL = "https://graph.threads.net/v1.0"
    MAX_RETRIES = 3
    RETRY_BASE_WAIT = 3

    def __init__(self, access_token: str, user_id: str):
        self.access_token = access_token
        self.user_id = user_id

    def _request_with_retry(self, method: str, url: str, **kwargs) -> dict:
        """リトライ付きHTTPリクエスト（指数バックオフ）"""
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                resp = requests.request(method, url, timeout=30, **kwargs)
                data = resp.json()

                if "error" in data:
                    error_code = data["error"].get("code", 0)
                    # 認証エラー・レート制限はリトライしない
                    if error_code in (190, 4):
                        print(f"ERROR: 認証/レート制限エラー (code={error_code})")
                        return {"error": data["error"]}
                    raise requests.exceptions.RequestException(
                        f"API error: {data['error']}"
                    )

                return data

            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    wait = self.RETRY_BASE_WAIT * (2 ** attempt)
                    print(f"  リトライ {attempt + 1}/{self.MAX_RETRIES} ({wait}秒後)")
                    time.sleep(wait)

        print(f"ERROR: {self.MAX_RETRIES}回リトライ失敗: {last_error}")
        return {"error": str(last_error)}

    def create_container(self, text: str, reply_to_id: str | None = None) -> dict:
        """テキスト投稿コンテナを作成。reply_to_id があれば返信として作成する。"""
        url = f"{self.BASE_URL}/{self.user_id}/threads"
        params = {
            "media_type": "TEXT",
            "text": text,
            "access_token": self.access_token,
        }
        if reply_to_id:
            params["reply_to_id"] = reply_to_id
        return self._request_with_retry("POST", url, data=params)

    def publish(self, creation_id: str) -> dict:
        """コンテナを公開"""
        url = f"{self.BASE_URL}/{self.user_id}/threads_publish"
        params = {
            "creation_id": creation_id,
            "access_token": self.access_token,
        }
        return self._request_with_retry("POST", url, data=params)

    def post_text(self, text: str, reply_to_id: str | None = None) -> dict:
        """テキスト投稿の一連フロー（コンテナ作成→公開）。"""
        label = "返信コンテナ" if reply_to_id else "コンテナ"
        print(f"  {label}作成中...")
        container = self.create_container(text, reply_to_id=reply_to_id)
        if "error" in container:
            return container

        creation_id = container.get("id")
        if not creation_id:
            return {"error": "コンテナIDが取得できませんでした"}

        # 公開前に少し待つ（Meta推奨）
        time.sleep(2)

        print(f"  公開中... (creation_id={creation_id})")
        result = self.publish(creation_id)
        if "error" not in result:
            print(f"  投稿成功: id={result.get('id')}")
        return result

    def get_post_insights(self, media_id: str) -> dict:
        """投稿のインサイトを取得"""
        url = f"{self.BASE_URL}/{media_id}/insights"
        params = {
            "metric": "views,likes,replies,reposts,quotes",
            "access_token": self.access_token,
        }
        return self._request_with_retry("GET", url, params=params)
