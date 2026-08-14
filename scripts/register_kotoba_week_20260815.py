import os

import gspread
from google.auth import default as google_auth_default

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

POSTS = [
    {
        "id": "KTK-20260815-AM",
        "date": "2026/08/15",
        "slot": "morning",
        "type": "life",
        "scene": "休日なのにいつもの時間に目が覚める朝",
        "first": "休みなのに目が覚めたw",
        "flat": "予定がない朝をそのまま過ごす",
        "positive": "ゆっくり始められる朝を楽しむ",
        "view": "質問ではなく小さな日常の一場面を置く",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

休みなのに、
いつもの時間に目が覚めたw

「せっかくの休みだし
もう一回寝るか」
と思ったけど、
結局コーヒー淹れてます☕

予定がない朝って、
それだけでちょっとゆっくり感じる。""",
    },
    {
        "id": "KTK-20260815-PM",
        "date": "2026/08/15",
        "slot": "evening",
        "type": "life",
        "scene": "片付け中に昔のものを見つけて脱線する",
        "first": "片付けするはずだったのに",
        "flat": "途中で別のものが気になった",
        "positive": "続きはまたやればいい",
        "view": "学びにしすぎず生活の失敗をそのまま出す",
        "source": "goroの日常投稿",
        "text": """片付けしようと思って始めたのに、

昔のもの見つけて、
そこから完全に別のことしてましたw

こういう脱線、
自分だけじゃないと思いたい😂

片付けは……
また続きやります。""",
    },
    {
        "id": "KTK-20260816-AM",
        "date": "2026/08/16",
        "slot": "morning",
        "type": "life",
        "scene": "休日の朝ごはんをまだ決めていない",
        "first": "朝ごはん何にしよう",
        "flat": "のんびり朝ごはんを考える",
        "positive": "休日の朝を急がず始める",
        "view": "自分の朝を先に出してから一つだけ開いた質問を置く",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

休日の朝。

コーヒー飲みながら、
「朝ごはん何にしよう」
ってまだ決めてませんw

平日より時間あるのに、
こういう日はなぜかのんびりする。

今日の朝ごはん、
何にしました？☕""",
    },
    {
        "id": "KTK-20260816-PM",
        "date": "2026/08/16",
        "slot": "evening",
        "type": "temporal_distance",
        "scene": "今日の気になることを、ものすごく遠い時間から見る",
        "first": "今日のことばかり気になる",
        "flat": "10万年後から見たら、これはどのくらいの大きさだろう",
        "positive": "今夜の時間を何に使いたいか考える",
        "view": "遠い時間を見ることで、今の大切なものへ意識を向ける",
        "source": "goroの考え／時間との距離",
        "text": """たまに、
ものすごく遠くから今を見ることがあります。

10万年後。

そこから見たら、
今日気にしてることって
どのくらいの大きさなんだろう。

だから「どうでもいい」
ではなくて、

じゃあ今夜の時間を
何に使いたいかなって考える。

遠くを見ると、
今が大切になる。""",
    },
    {
        "id": "KTK-20260817-AM",
        "date": "2026/08/17",
        "slot": "morning",
        "type": "life",
        "scene": "月曜朝に今週の予定を開く",
        "first": "今週もいろいろあるな",
        "flat": "まず今日の予定だけ見る",
        "positive": "一日ずつ始める",
        "view": "質問せず、仕事前の小さな習慣と人柄を出す",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

月曜日。

予定表を開いた瞬間、
「あ、今週もいろいろあるな」
ってなるw

でも朝から一週間分を
全部考えても疲れるので、
まず今日の分だけ見る。

そのあとコーヒー☕
一週間、ぼちぼち始めます。""",
    },
    {
        "id": "KTK-20260817-PM",
        "date": "2026/08/17",
        "slot": "evening",
        "type": "self_reflection",
        "scene": "一日の終わりに未完了のことばかり思い出す",
        "first": "今日も全然できなかった",
        "flat": "終わったものも、途中のものもある",
        "positive": "一日全部を未完了だけで決めない",
        "view": "問いかけず、自分の一日の見方として範囲を狭める",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """一日終わるころ、
終わらなかったことばっかり
思い出す日があります。

「あれもできなかった」
「これも残った」

でも見直すと、
終わったものもある。
途中のものもある。

今日は
「全部できなかった」じゃなく、
そのまま数えて終わります🌙""",
    },
    {
        "id": "KTK-20260818-AM",
        "date": "2026/08/18",
        "slot": "morning",
        "type": "life",
        "scene": "朝から昼ごはんを楽しみにする",
        "first": "今日のお昼何にしよう",
        "flat": "昼の楽しみを一つ持つ",
        "positive": "小さな楽しみを朝から考える",
        "view": "二択をやめ、食べ物の話から自由回答で会話を作る",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

朝からもう、
お昼何食べようって考えてますw

仕事の予定より先に
思い浮かぶ日もある。

小さいことだけど、
昼に楽しみがひとつあると
ちょっと嬉しい🍙

今日のお昼、何にします？""",
    },
    {
        "id": "KTK-20260818-PM",
        "date": "2026/08/18",
        "slot": "evening",
        "type": "neutral_reframe",
        "scene": "送ったメッセージに返信が来ず、理由を考え始める",
        "first": "何か変なこと言ったかな",
        "flat": "今わかっているのは、まだ返事が来ていないことだけ",
        "positive": "理由が分かる前に答えを作らない",
        "view": "事実と推測を分け、説明を長くしすぎず止める",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """メッセージの返信が来ないと、

「何か変なこと言ったかな」
まで一気に考えることがあります。

でも今わかってるのは、

「まだ返事が来てない」

それだけ。

理由はまだわからない。

今夜はそこまでにしておきます。""",
    },
    {
        "id": "KTK-20260819-AM",
        "date": "2026/08/19",
        "slot": "morning",
        "type": "life",
        "scene": "仕事中に一度席を立って切り替える",
        "first": "ちょっと席を離れよう",
        "flat": "数分だけ別の景色を見る",
        "positive": "自分なりの小さな切り替えを持つ",
        "view": "質問ではなく、仕事中の小さな習慣を一つ見せる",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

仕事中、頭が詰まってきたら
一回席を立ちます。

コンビニまで行くとか、
飲み物取りに行くとか。

数分だけ別の景色を見る。

自分にはそのくらいが
ちょうどいいです🌿""",
    },
    {
        "id": "KTK-20260819-PM",
        "date": "2026/08/19",
        "slot": "evening",
        "type": "neutral_reframe",
        "scene": "仕事で確認を一つ抜かしてミスした",
        "first": "今日ダメだったな",
        "flat": "確認を一つ抜かした",
        "positive": "次に確認する場所を一つ決める",
        "view": "ミスを否定せず、一日全体の評価とは分ける",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """ミスした直後って、
「今日ダメだったな」まで
広がることがあります。

今日あったのは、
確認をひとつ抜かしたこと。

ミスはミス。
へこむのもそのまま。

でも自分は、
一日全部の評価まではしない。

次はそこだけ確認する。
帰ったらごはんですw""",
    },
    {
        "id": "KTK-20260820-AM",
        "date": "2026/08/20",
        "slot": "morning",
        "type": "life",
        "scene": "帰宅すると冷蔵庫を開けて夜ごはんを考える",
        "first": "今日なに作れるかな",
        "flat": "冷蔵庫を見て夜ごはんを考える",
        "positive": "料理を考える時間を楽しむ",
        "view": "問いかけず、料理好きという人柄が見える短い日常を置く",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

家に帰ると、
手洗いしてそのまま
冷蔵庫を開けることが多いですw

お腹が空いてるというより、
「今日なに作れるかな」の確認。

冷蔵庫の前で考える時間、
けっこう好きです🍳""",
    },
    {
        "id": "KTK-20260820-PM",
        "date": "2026/08/20",
        "slot": "evening",
        "type": "attack_reframe",
        "scene": "仕事で言い方のきつい一言を受けた",
        "first": "あの人ほんと嫌だ",
        "flat": "自分は、その言い方が嫌だった",
        "positive": "責任を消さず、人全部の評価とは分ける",
        "view": "人物全体ではなく嫌だった言動まで対象を具体化する",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """きつい言い方をされると、
「あの人ほんと嫌だ」まで
思うことがあります。

時間が少し経っても、
嫌なものは嫌。

ただ、自分が嫌だったのは
「あの言い方」だった。

そこまでは分けて考える。

相手が悪くないことにする必要はないし、
人全部の話にもしなくていい。

今日はそこまで。""",
    },
    {
        "id": "KTK-20260821-AM",
        "date": "2026/08/21",
        "slot": "morning",
        "type": "life",
        "scene": "金曜朝から週末を少し楽しみにする",
        "first": "もう週末のこと考えてるw",
        "flat": "明日少しゆっくりできるのを楽しみにする",
        "positive": "小さな楽しみを持って金曜を始める",
        "view": "週の最後だけ開いた質問を置き、選択肢は並べない",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️

金曜日。

朝からもう
週末のこと考えてますw

何か特別な予定がなくても、
「明日は少しゆっくりできる」
それだけでちょっと嬉しい。

週末、何か楽しみにしてることあります？🌿""",
    },
    {
        "id": "KTK-20260821-PM",
        "date": "2026/08/21",
        "slot": "evening",
        "type": "life_distance",
        "scene": "金曜夜まで仕事の引っかかりを考え続けそうになる",
        "first": "まだ仕事のことが気になる",
        "flat": "必要なことだけメモして月曜に渡す",
        "positive": "今夜の時間は今夜に使う",
        "view": "考える時間を区切り、自分の生活へ意識を向ける",
        "source": "goroの生活実感／ことばの距離プロジェクト独自の実践",
        "text": """金曜の夜なのに、
仕事のことが頭に残ってる。

「あれ大丈夫かな」
「月曜どうしよう」

今すぐできることがないなら、
必要なことだけメモして終わり。

月曜の自分に渡して、
今夜は今夜。

冷蔵庫開けて、
何作るか考えますw🍳""",
    },
]


def is_locked(value):
    return str(value or "").strip().upper() in ("TRUE", "ERROR")


def main():
    spreadsheet_id = os.environ["SPREADSHEET_ID"]
    creds, _ = google_auth_default(scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(spreadsheet_id)
    queue = ss.worksheet("投稿キュー")
    stock = ss.worksheet("ネタストック")

    queue_records = queue.get_all_records()
    queue_by_id = {
        str(row.get("ネタID", "")).strip(): (idx, row)
        for idx, row in enumerate(queue_records, start=2)
        if str(row.get("ネタID", "")).strip()
    }

    queue_updated = 0
    queue_added = 0
    queue_skipped = 0

    for post in POSTS:
        existing = queue_by_id.get(post["id"])
        values = [[
            post["date"],
            post["slot"],
            post["text"],
            post["type"],
            post["id"],
            "",
            "",
            "",
        ]]

        if existing:
            row_index, row = existing
            if is_locked(row.get("投稿済", "")):
                queue_skipped += 1
                continue
            queue.update(range_name=f"A{row_index}:H{row_index}", values=values)
            queue_updated += 1
        else:
            queue.append_row(values[0], value_input_option="USER_ENTERED")
            queue_added += 1

    stock_records = stock.get_all_records()
    stock_by_id = {
        str(row.get("ID", "")).strip(): idx
        for idx, row in enumerate(stock_records, start=2)
        if str(row.get("ID", "")).strip()
    }

    stock_updated = 0
    stock_added = 0

    for post in POSTS:
        values = [[
            post["id"],
            post["date"],
            post["scene"],
            post["first"],
            post["type"],
            post["flat"],
            post["positive"],
            post["view"],
            post["source"],
            "FALSE",
        ]]

        row_index = stock_by_id.get(post["id"])
        if row_index:
            stock.update(range_name=f"A{row_index}:J{row_index}", values=values)
            stock_updated += 1
        else:
            stock.append_row(values[0], value_input_option="USER_ENTERED")
            stock_added += 1

    print(f"queue_updated={queue_updated}")
    print(f"queue_added={queue_added}")
    print(f"queue_skipped={queue_skipped}")
    print(f"stock_updated={stock_updated}")
    print(f"stock_added={stock_added}")
    print(f"posts_total={len(POSTS)}")


if __name__ == "__main__":
    main()
