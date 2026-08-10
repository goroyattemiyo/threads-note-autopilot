import gspread
from google.auth import default as google_auth_default

SPREADSHEET_ID = "1vmzjImuoZfm81JQClAMAmsqsaDPx7YuUAhZofrXQRWE"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]

POSTS = [
{"id":"KTK-20260811-AM","date":"2026/08/11","slot":"morning","type":"life","scene":"朝のコーヒーと仕事前","first":"おはようございます","flat":"いつもの朝をそのまま出す","positive":"今日もよろしくお願いします","view":"コーヒー好き・会社員が入りやすい朝の生活投稿","text":"""おはようございます☺️\n\n朝はコーヒー派です☕\n\n飲みながら、\n今日やることをぼんやり考える時間が好き。\n\nみなさんは朝、\nコーヒー派ですか？お茶派ですか？"""},
{"id":"KTK-20260811-PM","date":"2026/08/11","slot":"evening","type":"life_reframe","scene":"趣味が次々増える","first":"また趣味が増えました😂","flat":"興味を持つものが多いんだな","positive":"前向きに考えるようにしたw","view":"趣味・AI・料理・音楽好きが自分事で入れる","text":"""また趣味が増えました😂\n\n気になると、\nとりあえずやってみたくなる。\n\nAI、料理、音楽、DIY……\n\n時間が足りないw\n\n昔は\n「自分って飽きっぽいな」\nって思うこともあったけど、\n\n最近は\n「興味を持つものが多いんだな」\nって前向きに考えるようにしましたw"""},
{"id":"KTK-20260812-AM","date":"2026/08/12","slot":"morning","type":"life","scene":"朝から夜ごはんを考える","first":"朝なのにもう夜ごはん考えてるw","flat":"料理好きの日常","positive":"献立を考えるのが楽しい","view":"料理・自炊好きが入りやすい","text":"""おはようございます☺️\n\n朝なのに、\nもう夜ごはん何作ろうかなって考えてますw\n\n冷蔵庫に何あったっけ。\n\nみなさん今日の晩ごはん、\nもう決まってます？🍳"""},
{"id":"KTK-20260812-PM","date":"2026/08/12","slot":"evening","type":"life_reframe","scene":"料理の味付けが濃くなった","first":"味、濃くなったw","flat":"今日はちょっと濃かった","positive":"次は少し控えめにしよう","view":"料理の失敗あるあるから言葉の範囲を狭める","text":"""料理してて\n「あ、今日ちょっと味濃いな」って日があるw\n\n前なら普通に\n「失敗した〜」って言ってたけど、\n\n別に料理全部を失敗したわけじゃない。\n\n今日はちょっと濃かった。\n次は少し控えめにしよう。\n\n最近はそのくらいで終わるようにしてます。"""},
{"id":"KTK-20260813-AM","date":"2026/08/13","slot":"morning","type":"life","scene":"同じ曲を何度も聴く","first":"気に入った曲、何回も聴く派です","flat":"今これが好き","positive":"飽きるまで聴く","view":"音楽好きが参加しやすい","text":"""おはようございます☺️\n\n気に入った曲があると、\n同じ曲ばっかり聴くタイプですw\n\n朝からもう何回目だろう。\n\nみなさんもリピートする派です？🎧"""},
{"id":"KTK-20260813-PM","date":"2026/08/13","slot":"evening","type":"attack_reframe","scene":"駅の列に割り込まれた","first":"こういうの、自分は普通にイラッとします","flat":"割り込まれた行動が嫌だった","positive":"人全部まで嫌いにしない","view":"電車・通勤あるあるから人と行動を分ける","text":"""駅で並んでる列に\nスッと入られたら、\n自分は普通にイラッとします。\n\n「なんだこいつ」くらいは思うw\n\nでも少し経ったら、\n\n「あの人が嫌い」じゃなくて\n「割り込まれたのが嫌だった」\n\nくらいまで戻すようにしてます。\n\n嫌だった行動と、\nその人全部は分けておきたい。"""},
{"id":"KTK-20260814-AM","date":"2026/08/14","slot":"morning","type":"life","scene":"金曜朝に夜の料理を考える","first":"今日は帰ったら何作ろうかな","flat":"夜の楽しみを考える","positive":"仕事のあとに楽しみがある","view":"金曜・仕事・料理の共通関心","text":"""おはようございます☺️\n\n金曜日。\n\n今日は帰ったら何作ろうかな。\n\n仕事中に思いついたら\n忘れないようにメモしますw\n\nおすすめの簡単ごはんあったら教えてください🍳"""},
{"id":"KTK-20260814-PM","date":"2026/08/14","slot":"evening","type":"life_distance","scene":"仕事後の料理で頭が切り替わる","first":"仕事のあと、何すると切り替わります？","flat":"料理しているうちに別のことを考える","positive":"自分の生活に戻る","view":"会社員・家事・料理好きが入りやすい","text":"""仕事のあと、\n何すると頭が切り替わります？\n\n自分は料理してるときが多いです。\n\n玉ねぎ切って、\n肉焼いて、\n味見してるうちに、\n\n気づいたら仕事と別のこと考えてるw\n\n全部整理しなくても、\n生活に戻るだけで少し離れることってありますね。"""},
{"id":"KTK-20260815-AM","date":"2026/08/15","slot":"morning","type":"life","scene":"休日にやりたいことが増える","first":"休みの日ほどやりたいことが増えるw","flat":"やりたいことが多い","positive":"できたものから楽しむ","view":"休日・趣味好きのあるある","text":"""おはようございます☺️\n\n休みの日ほど、\nやりたいことが増えるw\n\nAIも触りたい。\n料理もしたい。\n音楽もやりたい。\n\nたぶん全部は終わりません😂\n\nみなさん今日は何します？"""},
{"id":"KTK-20260815-PM","date":"2026/08/15","slot":"evening","type":"life","scene":"片付け中に脱線する","first":"片付けあるあるだと思いたいw","flat":"途中で別のものが気になった","positive":"続きはまたやる","view":"片付け・家事の共感で入れる純生活投稿","text":"""片付けしようと思って始めたのに、\n\n昔のもの見つけて、\nそこから完全に別のことしてましたw\n\nこういう脱線、\n自分だけじゃないと思いたい😂\n\n片付けは……また続きやります。"""},
{"id":"KTK-20260816-AM","date":"2026/08/16","slot":"morning","type":"life","scene":"日曜朝に予定を決める前の時間","first":"日曜の朝って何してます？","flat":"まずコーヒーを飲む","positive":"予定を決める前の時間を楽しむ","view":"休日の過ごし方という広い入口","text":"""おはようございます☺️\n\n日曜日の朝って、\nみなさん何してます？\n\n自分はとりあえずコーヒー☕\n\n今日は何しようかなって\n考えてる時間もけっこう好きです。"""},
{"id":"KTK-20260816-PM","date":"2026/08/16","slot":"evening","type":"temporal_distance","scene":"目の前のことを大きく感じたとき遠い時間から見る","first":"たまに10万年後から今を見ます","flat":"今日のこれはどのくらいの大きさだろう","positive":"今の時間を何に使いたいかへ戻る","view":"一見変わった10万年という入口から時間との距離へ","text":"""たまに、\n10万年後から今を見ます。\n\n自分でも変な考え方だと思うw\n\nでも、そこから見たら\n今日気にしてることって\nどのくらいの大きさなんだろうって。\n\n「どうでもいい」じゃなくて、\n\nじゃあ今の時間を\n何に使いたいかなって戻ってくる。\n\n遠くを見ると、\n今が大切になる。"""},
{"id":"KTK-20260817-AM","date":"2026/08/17","slot":"morning","type":"life","scene":"思いついたことをすぐメモする","first":"思いついたらすぐメモする派です","flat":"忘れる前に残す","positive":"あとで見返すのも楽しい","view":"メモ・アイデア・仕事術好きの入口","text":"""おはようございます☺️\n\n思いついたこと、\nすぐメモする派です。\n\n仕事のことも、\n料理も、\nやってみたいことも。\n\nあとで見ると\n「これ何考えてたんだろうw」\nってメモもあります😂"""},
{"id":"KTK-20260817-PM","date":"2026/08/17","slot":"evening","type":"self_reflection","scene":"一日の終わりに未完了ばかり思い出す","first":"今日やろうと思ってたこと、全部終わりました？","flat":"途中のものもあった日","positive":"できたこともある","view":"仕事・家事の未完了あるあるから一日全体へ広げない","text":"""今日やろうと思ってたこと、\n全部終わりました？\n\n自分はだいたい何か残りますw\n\n前は\n「あれもできなかった」\nって考えがちだったけど、\n\n今日はこれをやった。\nこれは途中だった。\n\n最近はそのくらいで\n一日を終えるようにしてます🌙"""}
]


def main():
    creds, _ = google_auth_default(scopes=SCOPES)
    ss = gspread.authorize(creds).open_by_key(SPREADSHEET_ID)
    queue = ss.worksheet("投稿キュー")
    stock = ss.worksheet("ネタストック")
    by_id = {p["id"]: p for p in POSTS}

    qrecords = queue.get_all_records()
    qcount = 0
    for idx, row in enumerate(qrecords, start=2):
        pid = str(row.get("ネタID", "")).strip()
        if pid in by_id and str(row.get("投稿済", "")).strip().upper() not in ("TRUE", "ERROR"):
            p = by_id[pid]
            queue.update(f"A{idx}:H{idx}", [[p["date"], p["slot"], p["text"], p["type"], p["id"], "", "", ""]])
            qcount += 1

    srecords = stock.get_all_records()
    scount = 0
    for idx, row in enumerate(srecords, start=2):
        pid = str(row.get("ID", "")).strip()
        if pid in by_id:
            p = by_id[pid]
            stock.update(f"A{idx}:J{idx}", [[p["id"], p["date"], p["scene"], p["first"], p["type"], p["flat"], p["positive"], p["view"], "goroの生活実感／ことばの距離プロジェクト独自の実践", "FALSE"]])
            scount += 1

    print(f"queue_updated={qcount}")
    print(f"stock_updated={scount}")

if __name__ == "__main__":
    main()
