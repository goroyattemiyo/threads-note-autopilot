"""メイン実行スクリプト - Sheets → Threads 投稿"""
import os
import sys

from threads_api import ThreadsAPI
from sheets import SheetManager


def load_env(key: str) -> str:
    """環境変数を取得（未設定なら終了）"""
    value = os.environ.get(key, "")
    if not value:
        print(f"ERROR: 環境変数 {key} が未設定です")
        sys.exit(1)
    return value


def run_post(time_slot: str):
    """投稿を実行"""
    print(f"=== Threads 自動投稿 ({time_slot}) ===")

    # 環境変数読み込み
    access_token = load_env("KURASHI_ACCESS_TOKEN")
    user_id = load_env("KURASHI_USER_ID")
    sheets_creds = load_env("GOOGLE_SHEETS_CREDENTIALS")
    spreadsheet_id = "1LBzuBpfMBIFPtnsF9Pbhs9LmC0lBgQSOGTQ5uK1Y_7Y"
    queue_sheet = "投稿キュー"
    log_sheet = "投稿ログ"

    # 初期化
    api = ThreadsAPI(access_token, user_id)
    sheets = SheetManager(sheets_creds, spreadsheet_id)

    # 次の投稿を取得
    print("投稿キューを確認中...")
    post_data = sheets.get_next_post(queue_sheet, time_slot)

    if not post_data:
        print("投稿対象がありません。終了します。")
        return

    print(f"投稿対象: row={post_data['row']} 種別={post_data['type']}")
    print(f"投稿文: {post_data['text'][:50]}...")

    # Threads に投稿
    result = api.post_text(post_data["text"])

    if "error" in result:
        error_msg = str(result["error"])[:200]
        print(f"ERROR: {error_msg}")
        sheets.mark_as_error(queue_sheet, post_data["row"], error_msg)
        sheets.log_post(log_sheet, "", post_data["text"],
                        post_data["type"], "error")
        sys.exit(1)

    post_id = result.get("id", "")
    print(f"投稿完了: {post_id}")

    # Sheets 更新
    sheets.mark_as_posted(queue_sheet, post_data["row"], post_id)
    sheets.log_post(log_sheet, post_id, post_data["text"],
                    post_data["type"], "success")
    print("Sheets 更新完了")


def run_status():
    """キューの状態を表示"""
    sheets_creds = load_env("GOOGLE_SHEETS_CREDENTIALS")
    spreadsheet_id = "1LBzuBpfMBIFPtnsF9Pbhs9LmC0lBgQSOGTQ5uK1Y_7Y"
    queue_sheet = "投稿キュー"

    sheets = SheetManager(sheets_creds, spreadsheet_id)
    status = sheets.get_queue_status(queue_sheet)

    print("=== 投稿キュー状態 ===")
    print(f"  合計:   {status['total']}件")
    print(f"  投稿済: {status['posted']}件")
    print(f"  エラー: {status['errors']}件")
    print(f"  未投稿: {status['pending']}件")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python post.py [post-morning|post-evening|status]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "post-morning":
        run_post("morning")
    elif command == "post-evening":
        run_post("evening")
    elif command == "status":
        run_status()
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)
