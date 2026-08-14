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
        "scene": "土曜の朝、目覚ましをかけるかどうか",
        "first": "休みの日くらい目覚ましなしで寝たい",
        "flat": "予定がなければ自然に起きたい",
        "positive": "休日の朝をゆっくり始める",
        "view": "答えやすい休日あるあるで会話を作る",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n休みの日の朝って、\n目覚ましかけます？\n\n自分は予定がなければ\nできればかけたくないw\n\nでも結局、\nいつもの時間に目が覚めることも多い。\n\nみなさんは寝る派？\nいつも通り派？☕""",
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
        "text": """片付けしようと思って始めたのに、\n\n昔のもの見つけて、\nそこから完全に別のことしてましたw\n\nこういう脱線、\n自分だけじゃないと思いたい😂\n\n片付けは……\nまた続きやります。""",
    },
    {
        "id": "KTK-20260816-AM",
        "date": "2026/08/16",
        "slot": "morning",
        "type": "life",
        "scene": "日曜朝の朝ごはん",
        "first": "朝ごはん何にしよう",
        "flat": "休日の朝の食べ方を聞く",
        "positive": "のんびり朝を始める",
        "view": "食べ物の低コストな質問で参加しやすくする",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n休日の朝ごはん、\nみなさん何食べます？\n\nパン派。\nごはん派。\nそれともコーヒーだけ派。\n\n自分はとりあえず\nコーヒーから始まります☕""",
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
        "text": """たまに、\nものすごく遠くから今を見ることがあります。\n\n10万年後。\n\nそこから見たら、\n今日気にしてることって\nどのくらいの大きさなんだろう。\n\nだから「どうでもいい」\nではなくて、\n\nじゃあ今夜の時間を\n何に使いたいかなって考える。\n\n遠くを見ると、\n今が大切になる。""",
    },
    {
        "id": "KTK-20260817-AM",
        "date": "2026/08/17",
        "slot": "morning",
        "type": "life",
        "scene": "月曜、仕事を始める前に最初にすること",
        "first": "まず何から始めよう",
        "flat": "朝のルーティンを聞く",
        "positive": "いつものやり方で一週間を始める",
        "view": "仕事の共通体験から会話に入りやすくする",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n仕事始めるとき、\n最初に何します？\n\nメール見る。\n今日の予定見る。\nとりあえずコーヒー飲む。\n\n自分はまず予定を見てから、\nだいたいコーヒーですw☕""",
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
        "view": "できなかったことを一日全体へ広げない",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """今日やろうと思ってたこと、\n全部終わりました？\n\n自分はだいたい何か残りますw\n\nそういう日に\n「今日も全然できなかった」\nって思うことがあるけど、\n\nよく見ると、\n終わったものもある。\n途中のものもある。\n\n今日はそのくらいで\n終わりにします🌙""",
    },
    {
        "id": "KTK-20260818-AM",
        "date": "2026/08/18",
        "slot": "morning",
        "type": "life",
        "scene": "平日のお昼ごはんをどうするか",
        "first": "今日のお昼どうしよう",
        "flat": "昼食スタイルを聞く",
        "positive": "日常の小さな楽しみを共有する",
        "view": "食べ物の答えやすい質問で会話を作る",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n平日のお昼ごはんって、\nみなさんどうしてます？\n\n持っていく派。\n買う派。\n外で食べる派。\n\n自分は朝から\n今日のお昼どうしようって考えてますw🍙""",
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
        "view": "事実と推測を分けて、考えを広げすぎない",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """メッセージの返信が来ないと、\n\n「何か変なこと言ったかな」\nって考え始めることがあります。\n\n自分も普通にある。\n\nでも今わかってるのは、\n\n「まだ返事が来てない」\n\nそこまでなんですよね。\n\n忙しいのかもしれないし、\nあとで返すつもりかもしれない。\n\n理由が分かる前に、\n答えまで作らないようにしたい。""",
    },
    {
        "id": "KTK-20260819-AM",
        "date": "2026/08/19",
        "slot": "morning",
        "type": "life",
        "scene": "仕事の合間の短い休憩",
        "first": "ちょっと外に出たい",
        "flat": "休憩の過ごし方を聞く",
        "positive": "数分でも自分なりに切り替える",
        "view": "仕事中の小さな習慣を共有してもらう",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n仕事の合間の休憩、\nみなさん何してます？\n\n自分は少し外に出るのが好きです。\n\nコンビニ行くだけでも、\n席を離れるとちょっと気分が変わるw\n\n外に出る派？\n席で休む派？""",
    },
    {
        "id": "KTK-20260819-PM",
        "date": "2026/08/19",
        "slot": "evening",
        "type": "neutral_reframe",
        "scene": "仕事で確認を一つ抜かしてミスした",
        "first": "今日ダメだったな",
        "flat": "確認を一つ抜かした",
        "positive": "直す場所が一つ分かれば次に使える",
        "view": "一つのミスを一日全体の評価に広げない",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """仕事でひとつミスすると、\n\n「今日ダメだったな」\nって思うことがあります。\n\n自分も普通にへこむ。\n\nでも今日ダメだったというより、\n\n「確認をひとつ抜かした」\n\nなんですよね。\n\nそれなら直す場所もひとつ。\n\n今日はそこだけ覚えて、\nあとは家でごはん食べますw""",
    },
    {
        "id": "KTK-20260820-AM",
        "date": "2026/08/20",
        "slot": "morning",
        "type": "life",
        "scene": "家に帰って最初にすること",
        "first": "帰ったらまず何しよう",
        "flat": "帰宅後のルーティンを聞く",
        "positive": "自分の生活のリズムを共有する",
        "view": "誰でも答えやすい帰宅後あるあるで会話を作る",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n家に帰ったら、\n最初に何します？\n\n手洗う。\n着替える。\n冷蔵庫開ける。\nソファに座る。\n\n自分は手洗って、\nだいたい冷蔵庫見ますw\n\n夜ごはんの確認です🍳""",
    },
    {
        "id": "KTK-20260820-PM",
        "date": "2026/08/20",
        "slot": "evening",
        "type": "attack_reframe",
        "scene": "仕事で言い方のきつい一言を受けた",
        "first": "あの人ほんと嫌だ",
        "flat": "自分は、その言い方が嫌だった",
        "positive": "人全部の評価まで今日決めなくていい",
        "view": "人物全体ではなく嫌だった言動まで対象を具体化する",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """仕事で言い方がきつい一言をもらうと、\n普通にイラッとします。\n\n「あの人ほんと嫌だ」\nくらいまで思うこともあるw\n\nでも少し時間が経つと、\n\n嫌だったのは\nその人全部というより、\nあの言い方だったなと思う。\n\n人全部の評価まで\n今日決めなくていい。\n\n自分はそのくらいにして、\n夕飯つくります。""",
    },
    {
        "id": "KTK-20260821-AM",
        "date": "2026/08/21",
        "slot": "morning",
        "type": "life",
        "scene": "金曜の朝、週末にやりたいことを考える",
        "first": "週末何しよう",
        "flat": "週末の予定を聞く",
        "positive": "小さな楽しみを一つ持つ",
        "view": "金曜の共通感覚から気軽な会話を作る",
        "source": "goroの日常投稿",
        "text": """おはようございます☺️\n\n金曜日。\n\n週末、何するか決まってます？\n\n自分は料理もしたいし、\nAIも触りたいし、\n音楽もやりたい。\n\nたぶんまた予定だけ増えますw\n\nみなさん何します？""",
    },
    {
        "id": "KTK-20260821-PM",
        "date": "2026/08/21",
        "slot": "evening",
        "type": "life_distance",
        "scene": "金曜夜まで仕事の引っかかりを考え続けそうになる",
        "first": "まだ仕事のことが気になる",
        "flat": "月曜に必要なら、そのとき考える",
        "positive": "今夜の時間は今夜に使う",
        "view": "考える時間を区切って、自分の生活へ意識を向ける",
        "source": "goroの生活実感／ことばの距離プロジェクト独自の実践",
        "text": """金曜の夜まで、\n仕事のことが頭に残る日もあります。\n\n「あれ大丈夫かな」\n「月曜どうしよう」\nって。\n\nでも今すぐできることがないなら、\n月曜に必要な分だけ考えればいい。\n\n今夜は今夜。\n\n自分は冷蔵庫開けて、\n何作るか考えますw🍳""",
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
            queue.update(f"A{row_index}:H{row_index}", values)
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
            stock.update(f"A{row_index}:J{row_index}", values)
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
