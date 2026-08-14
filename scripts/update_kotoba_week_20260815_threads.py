"""8/15-8/21 投稿の文面調整と、時々入れるツリー2投稿目を登録する。"""
import os

import gspread
from google.auth import default as google_auth_default

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

QUEUE_HEADERS = [
    "投稿日",
    "時間帯",
    "投稿文",
    "種別",
    "ネタID",
    "投稿済",
    "投稿ID",
    "エラー",
    "ツリー2投稿目",
    "ツリー投稿ID",
    "ツリーエラー",
]

TEXT_UPDATES = {
    "KTK-20260818-PM": """メッセージの返信が来ないと、

「何か変なこと言ったかな」
って考え始めることがあります。

自分も普通にある。

でも今わかってるのは、

「まだ返事が来てない」

それだけ。

忙しいのかもしれないし、
あとで返すつもりかもしれない。

理由が分かる前に、
答えまで作らないようにしたい。""",
    "KTK-20260819-PM": """仕事でひとつミスすると、

「今日ダメだったな」
って思うことがあります。

自分も普通にへこむ。

でも、今日全部がダメだったわけじゃなくて、

「確認をひとつ抜かした」

という話。

それなら直す場所もひとつ。

今日はそこだけ覚えて、
あとは家でごはん食べますw""",
}

THREAD_REPLIES = {
    "KTK-20260816-PM": """こういうことを考えるのは、
悩みを「どうでもいい」で終わらせたいからじゃないです。

自分も普通にイライラするし、
気になることを引きずります。

ただ、遠くから見てみると、
「じゃあ今の時間を何に使いたい？」
と考えやすくなることがある。

このアカウントでは、
言葉や視点を変えて、
嫌なことを引きずる時間を少し短くする。

そんな自分なりのやり方を書いています。""",
    "KTK-20260820-PM": """こういう投稿をしてますが、
自分も普通にイラッとするし、
ネガティブにもなりますw

誰かのせいにしたくなる日もある。

それを無理に前向きにするんじゃなくて、
何が嫌だったのかを少し具体的に考える。

それだけで、出来事と少し距離ができることがあります。

ここでは、
自分が実際に使っているそんな考え方を書いています。

前向きになれなくても、
少しフラットになれたら十分。""",
}

TARGET_IDS = {
    f"KTK-202608{day:02d}-{slot}"
    for day in range(15, 22)
    for slot in ("AM", "PM")
}


def main():
    spreadsheet_id = os.environ["SPREADSHEET_ID"]
    credentials, _ = google_auth_default(scopes=SCOPES)
    spreadsheet = gspread.authorize(credentials).open_by_key(spreadsheet_id)
    queue = spreadsheet.worksheet("投稿キュー")

    if queue.col_count < len(QUEUE_HEADERS):
        queue.resize(cols=len(QUEUE_HEADERS))
    queue.update(values=[QUEUE_HEADERS], range_name="A1:K1")

    records = queue.get_all_records()
    text_updated = 0
    thread_registered = 0
    cleared = 0
    skipped_posted = 0

    for row_index, row in enumerate(records, start=2):
        neta_id = str(row.get("ネタID", "")).strip()
        if neta_id not in TARGET_IDS:
            continue

        posted = str(row.get("投稿済", "")).strip().upper() in ("TRUE", "ERROR")
        if posted:
            skipped_posted += 1
            continue

        if neta_id in TEXT_UPDATES:
            queue.update_cell(row_index, 3, TEXT_UPDATES[neta_id])
            text_updated += 1

        if neta_id in THREAD_REPLIES:
            queue.update_cell(row_index, 9, THREAD_REPLIES[neta_id])
            queue.update_cell(row_index, 10, "")
            queue.update_cell(row_index, 11, "")
            thread_registered += 1
        else:
            # 今週は2件だけツリーを付ける。未投稿行だけ明示的に空欄へ。
            queue.update_cell(row_index, 9, "")
            queue.update_cell(row_index, 10, "")
            queue.update_cell(row_index, 11, "")
            cleared += 1

    print(f"text_updated={text_updated}")
    print(f"thread_registered={thread_registered}")
    print(f"thread_cleared={cleared}")
    print(f"skipped_posted={skipped_posted}")


if __name__ == "__main__":
    main()
