import gspread
from google.auth import default as google_auth_default

SPREADSHEET_ID = "1vmzjImuoZfm81JQClAMAmsqsaDPx7YuUAhZofrXQRWE"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

POSTS = [
    {
        "id": "KTK-20260810-AM",
        "date": "2026/08/10",
        "slot": "morning",
        "type": "neutral_reframe",
        "scene": "朝から嫌なことが一つ起きた",
        "first": "今日は最悪な日だ",
        "flat": "朝から嫌なことがあった",
        "positive": "まだ今日全部が決まったわけじゃない",
        "view": "一つの嫌な出来事を一日全部へ広げない",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """朝から嫌なことがあると、\n「今日は最悪な日だ」\nって思うことがある。\n\n自分も普通に思う。\n\nでも、少しだけ言葉を戻してみる。\n\n「今日は最悪」\nじゃなくて、\n「朝から嫌なことがあった」\n\n嫌だったことは消えない。\nでも、まだ今日全部が\n決まったわけじゃない。""",
    },
    {
        "id": "KTK-20260810-PM",
        "date": "2026/08/10",
        "slot": "evening",
        "type": "neutral_reframe",
        "scene": "一日を振り返って嫌な出来事ばかり思い出す",
        "first": "今日は全部ダメだった",
        "flat": "今日は嫌なことがあった",
        "positive": "一日全部を嫌な出来事ひとつに渡さない",
        "view": "嫌な一日と、嫌なことがあった一日を分ける",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """「今日は最悪だった」\n\nそんな夜もある。\n\nでも少し落ち着いたら、\n\n「今日は嫌なことがあった」\n\nくらいまで言葉を戻してみる。\n\n同じ一日でも、\n少しだけ意味が変わる。\n\n嫌なことがあった一日と、\n全部が嫌だった一日は、\nたぶん同じじゃない。""",
    },
    {
        "id": "KTK-20260811-AM",
        "date": "2026/08/11",
        "slot": "morning",
        "type": "reassurance",
        "scene": "理由は分からないが、なんとなくイライラしている",
        "first": "なんか最悪。ムカつく",
        "flat": "腹が立った／悔しかった／不安だった",
        "positive": "何に反応しているか少し見えれば十分",
        "view": "感情を消さず、中身を少し具体化してみる",
        "source": "Affect labeling / Emotion differentiationとの接点あり。効果の断定はしない",
        "text": """「なんかムカつく」\n「もう最悪」\n\nそんなとき、\n無理に前向きにしなくてもいい。\n\n自分は少しだけ、\n中身を分けてみる。\n\n腹が立ったのか。\n悔しかったのか。\n不安だったのか。\nがっかりしたのか。\n\nまだ分からないなら、\nそれでもいい。\n\n気持ちを消すより、\nまず何に反応しているか\n少し見えれば十分。""",
    },
    {
        "id": "KTK-20260811-PM",
        "date": "2026/08/11",
        "slot": "evening",
        "type": "reassurance",
        "scene": "嫌なことがあったが、自分でも感情が整理できない",
        "first": "自分でも何が嫌なのか分からない",
        "flat": "まだよく分からない",
        "positive": "今日はそこまででもいい",
        "view": "感情の言語化を急がない",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """怒りなのか、\n悔しいのか、\n寂しいのか。\n\n自分でもよく分からない夜がある。\n\nそんなときまで、\nちゃんと言葉にしなきゃ\nと思わなくていい。\n\n「まだよく分からない」\n\nそれも今の自分に近い言葉だと思う。\n\n無理に答えを作らず、\n今日はそこまででもいい🌙""",
    },
    {
        "id": "KTK-20260812-AM",
        "date": "2026/08/12",
        "slot": "morning",
        "type": "attack_reframe",
        "scene": "電車待ちの列に割り込まれた",
        "first": "なんだこいつ。常識ないな",
        "flat": "割り込まれたことが嫌だった",
        "positive": "その人全部まで嫌いだと決めなくてもいい",
        "view": "人そのものと、その人の行動を分ける",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """電車を待っていて、\n並んでいる列に割り込まれたら、\n普通に腹が立つ。\n\n「なんだこいつ」\n「常識ないな」\n\n自分もそう思う。\n\nでも少し経ったら、\n\n「あの人が嫌い」\nではなく、\n「割り込まれたことが嫌だった」\n\nくらいまで言葉を戻してみる。\n\n割り込みは嫌い。\nでも、その人全部まで\n嫌いだと決めなくてもいい。\n\n自分はそう考えるようにしている。""",
    },
    {
        "id": "KTK-20260812-PM",
        "date": "2026/08/12",
        "slot": "evening",
        "type": "attack_reframe",
        "scene": "愛想のない態度や思いやりのない言い方をされた",
        "first": "この人ほんと嫌い",
        "flat": "その言い方／その態度が嫌だった",
        "positive": "人と、その人の行動は少し分けて考えたい",
        "view": "人物全体ではなく、自分が嫌だった言動まで対象を具体化する",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """人を嫌いになることって、\n自分は意外と少ない。\n\nでも、\n\nその言い方は嫌だな。\nその態度は苦手だな。\nそれは自分勝手じゃないかな。\n\nと思うことは普通にある。\n\n「あの人が嫌い」まで広げず、\n\n「自分は、この言動が嫌だった」\n\nくらいで止めておく。\n\n人と、その人の行動は、\n少し分けて考えたい。""",
    },
    {
        "id": "KTK-20260813-AM",
        "date": "2026/08/13",
        "slot": "morning",
        "type": "temporal_distance",
        "scene": "今すごく気になる小さなトラブルがある",
        "first": "ずっと気になる。最悪だ",
        "flat": "来週も同じ大きさで気にしているかな",
        "positive": "今の感情がこの大きさのままずっと続くとは限らない",
        "view": "近い未来から現在を見る",
        "source": "Temporal distancingとの接点あり。未来予測としては扱わない",
        "text": """今はすごく気になる。\n\nでも、\n\n「これ、来週も\n同じ大きさで気にしてるかな」\n\nと考えることがある。\n\n来週には絶対どうでもよくなる、\nという意味じゃない。\n\nただ、今の気持ちが\nこの大きさのままずっと続くとは\n限らない。\n\nそれだけでも少し、\n目の前から距離ができることがある。""",
    },
    {
        "id": "KTK-20260813-PM",
        "date": "2026/08/13",
        "slot": "evening",
        "type": "temporal_distance",
        "scene": "今日あった嫌な出来事を寝る前まで引きずっている",
        "first": "まだ腹が立つ。忘れられない",
        "flat": "1年後の自分なら、今の自分になんて言うだろう",
        "positive": "今とは少し違う場所から自分を見る",
        "view": "未来の自分から現在を見る",
        "source": "Temporal distancing / Future-self writingとの接点あり",
        "text": """今日あった嫌なこと。\n\nまだ頭に残っているなら、\n\n「1年後の自分なら、\n今の自分になんて言うだろう」\n\nと考えてみる。\n\n「気にするな」\nじゃなくてもいい。\n\n「それは腹立つよな」\nかもしれない。\n\nでも、今とは少し違う場所から\n自分を見られるかもしれない。""",
    },
    {
        "id": "KTK-20260814-AM",
        "date": "2026/08/14",
        "slot": "morning",
        "type": "other_blame",
        "scene": "相手のミスや身勝手な行動で自分が困った",
        "first": "あいつのせいで全部ダメになった",
        "flat": "相手に問題はあった。では自分は次に何をするか",
        "positive": "自分の人生のハンドルまで相手に渡さない",
        "view": "責任の所在と、これから自分が選ぶ行動を分ける",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """相手が悪かったなら、\n「自分にも原因があるかも」\nと無理に考えなくていいと思う。\n\n相手の責任は相手の責任。\n\nでも、\n\n「じゃあ自分は次にどうするか」\n\nは別の話。\n\n責任の所在と、\nこれから自分が選ぶ行動は\n分けて考えたい。\n\n自分の人生のハンドルまで\n相手に渡さないために。""",
    },
    {
        "id": "KTK-20260814-PM",
        "date": "2026/08/14",
        "slot": "evening",
        "type": "self_reflection",
        "scene": "嫌な相手のことを何時間も考え続けている",
        "first": "あいつ本当にムカつく",
        "flat": "嫌だった。それはそれでいい",
        "positive": "残りの時間を少しずつ自分の方へ戻したい",
        "view": "嫌な出来事に使う時間を区切り、自分の時間へ戻る",
        "source": "ことばの距離プロジェクト独自の実践",
        "text": """嫌なことをされたら、\nその瞬間は普通に傷つくし、\n腹も立つ。\n\nでも、その人のことを\n何時間も考え続けていたら、\n\n嫌な出来事より長い時間を\nその人に使うことになる。\n\nだから自分は、\n\n「嫌だった。それはそれでいい」\n\nまで言葉を戻して、\n\n残りの時間を\n少しずつ自分の方へ戻したい。""",
    },
    {
        "id": "KTK-20260815-AM",
        "date": "2026/08/15",
        "slot": "morning",
        "type": "self_reflection",
        "scene": "確認不足で仕事や作業をミスした",
        "first": "自分ってほんとダメだな",
        "flat": "今回は確認不足でミスをした",
        "positive": "失敗を自分全部に広げなくてもいい",
        "view": "人格評価から具体的な事実へ戻す",
        "source": "Decentering / Cognitive defusionと接点はあるが、この言い換え自体はプロジェクト独自",
        "text": """ミスをすると、\n\n「自分ってほんとダメだな」\n\nと思うことがある。\n\nでも、\n反省することと\n自分を攻撃することは別。\n\n「自分はダメ」\nじゃなくて、\n\n「今回は確認不足でミスをした」\n\nまで戻す。\n\n失敗を小さくする必要はない。\n\nでも、失敗を\n自分全部に広げなくてもいい。""",
    },
    {
        "id": "KTK-20260815-PM",
        "date": "2026/08/15",
        "slot": "evening",
        "type": "reassurance",
        "scene": "嫌な出来事を何度も思い出して強い言葉を重ねている",
        "first": "最悪。ほんと最低。ずっとムカつく",
        "flat": "嫌だった。傷ついた",
        "positive": "一度傷ついたあと、自分でもう何度も傷つけ続けなくていい",
        "view": "強い言葉を重ねるのをやめ、感情に近い言葉まで戻る",
        "source": "ことばの距離プロジェクト独自の中核思想",
        "text": """傷つかないように生きるのは、\nたぶん無理だと思う。\n\n嫌なこともあるし、\n腹が立つこともある。\n\nでも、\n\n一度傷ついたあとに\n\n「最悪」\n「全部ダメ」\n「絶対許せない」\n\nと強い言葉を重ねて、\n\n自分でもう何度も\n傷つけ続けなくていい。\n\n「嫌だった」\n「傷ついた」\n\nまずはそこまで戻れたら、\n自分は十分だと思っている。""",
    },
    {
        "id": "KTK-20260816-AM",
        "date": "2026/08/16",
        "slot": "morning",
        "type": "temporal_distance",
        "scene": "目の前の小さなトラブルに頭を持っていかれている",
        "first": "こんなこと許せない。ずっと腹が立つ",
        "flat": "この出来事に、今日の残り時間まで使いたいだろうか",
        "positive": "この後の時間を何に使いたい？",
        "view": "10万年後という極端に遠い時間から見て、現在の大切なものへ戻る",
        "source": "長い時間軸はgoro自身の経験・思想。Temporal distancing研究と同一視しない",
        "text": """目の前の嫌なことが\nすごく大きく感じるとき、\n\n自分は、ときどき\nものすごく遠くまで時間を伸ばして考える。\n\n10万年後。\n\nそこから見たら、\n今日のこの出来事は\nものすごく小さい。\n\nだから「どうでもいい」\nではなくて、\n\n「じゃあ、この後の時間を\n何に使いたい？」\n\nと今に戻ってくる。\n\n遠くを見るのは、\n今を捨てるためじゃない。""",
    },
    {
        "id": "KTK-20260816-PM",
        "date": "2026/08/16",
        "slot": "evening",
        "type": "temporal_distance",
        "scene": "一週間を振り返り、嫌なことも良いこともあった",
        "first": "今週いろいろあったな",
        "flat": "嫌なことはあった。でも、自分の時間はまだ残っている",
        "positive": "遠くを見ると、今が大切になる",
        "view": "遠くから見たあと、家族・友人・好きなこと・自分の時間へ戻る",
        "source": "ことばの距離プロジェクトのキーフレーズ／goro自身の経験・思想",
        "text": """遠くを見ると、\n今の悩みが少し小さく見えることがある。\n\nでも、\n「どうせ全部なくなる」\nと思いたいわけじゃない。\n\nむしろ逆。\n\n時間が限られているなら、\n\nどうでもいいことを少し手放して、\n家族や友人、\n好きなこと、\n自分の時間へ戻りたい。\n\n遠くを見ると、\n今が大切になる。\n\n自分はそんなふうに\n考えるようにしています🌿""",
    },
]


def main():
    credentials, _ = google_auth_default(scopes=SCOPES)
    gc = gspread.authorize(credentials)
    ss = gc.open_by_key(SPREADSHEET_ID)

    queue = ss.worksheet("投稿キュー")
    stock = ss.worksheet("ネタストック")

    queue_records = queue.get_all_records()
    queue_ids = {str(r.get("ネタID", "")).strip() for r in queue_records}
    stock_records = stock.get_all_records()
    stock_ids = {str(r.get("ID", "")).strip() for r in stock_records}

    queue_rows = []
    stock_rows = []

    for p in POSTS:
        if p["id"] not in queue_ids:
            queue_rows.append([
                p["date"], p["slot"], p["text"], p["type"], p["id"], "", "", ""
            ])
        if p["id"] not in stock_ids:
            stock_rows.append([
                p["id"], p["date"], p["scene"], p["first"], p["type"], p["flat"],
                p["positive"], p["view"], p["source"], "FALSE"
            ])

    if queue_rows:
        queue.append_rows(queue_rows, value_input_option="USER_ENTERED")
    if stock_rows:
        stock.append_rows(stock_rows, value_input_option="USER_ENTERED")

    print(f"投稿キュー追加: {len(queue_rows)}件")
    print(f"ネタストック追加: {len(stock_rows)}件")


if __name__ == "__main__":
    main()
