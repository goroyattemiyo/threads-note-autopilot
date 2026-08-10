import os
import gspread
from google.auth import default as google_auth_default

SPREADSHEET_ID = "1vmzjImuoZfm81JQClAMAmsqsaDPx7YuUAhZofrXQRWE"
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
TARGET_DATES = {"2026/08/11","2026/08/12","2026/08/13","2026/08/14","2026/08/15","2026/08/16","2026/08/17"}

POSTS = [
{"id":"KTK-20260811-AM","date":"2026/08/11","slot":"morning","type":"life","scene":"朝、コーヒーを飲みながらその日のことを考える","first":"今日は何しようかな","flat":"今日もいつも通り始める","positive":"気になったことがあればまた試してみる","view":"朝は考え方を教えず、生活の温度をそのまま出す","source":"goroの日常投稿","text":"""おはようございます☺️\n\n朝ごはん食べて、\nコーヒー飲んで、\n今日もいつも通りスタート。\n\n仕事しながら、\nまた何か気になること見つけたら\nたぶん寄り道しますw\n\n今日もよろしくお願いします☕"""},
{"id":"KTK-20260811-PM","date":"2026/08/11","slot":"evening","type":"life_reframe","scene":"気になることを次々始めて趣味が増える","first":"自分って飽きっぽいな","flat":"興味を持つものが多いんだな","positive":"前向きに考えるようにした","view":"同じ自分でも、自分に使う言葉で見え方が変わる","source":"goroの生活実感／ことばの距離プロジェクト独自の実践","text":"""また趣味が増えました😂\n\n気になると、\nとりあえずやってみたくなる。\n\nAI、料理、音楽、DIY……\n\n時間が足りないのは、\nたぶん自分のせいですw\n\n昔は\n「自分って飽きっぽいな」\nって思うこともあったけど、\n\n最近は、\n\n「興味を持つものが多いんだな」\n\nって前向きに考えるようにしましたw\n\nやってることは同じでも、\n自分に使う言葉で\n見え方って変わりますね。"""},
{"id":"KTK-20260812-AM","date":"2026/08/12","slot":"morning","type":"life","scene":"朝から夜ごはんを考える","first":"今日の夜なに作ろう","flat":"冷蔵庫の中を思い浮かべる","positive":"帰ってから作るのを楽しみにする","view":"料理好きの生活感をそのまま出す","source":"goroの日常投稿","text":"""おはようございます☺️\n\n朝なのに、\nもう夜ごはん何作ろうかなって考えてますw\n\n冷蔵庫に何あったっけ。\n\nこういうこと考えてる時間、\nけっこう好きです🍳"""},
{"id":"KTK-20260812-PM","date":"2026/08/12","slot":"evening","type":"life_reframe","scene":"料理の味付けが濃くなった","first":"失敗した","flat":"今日はちょっと味が濃くなった","positive":"次は少し控えめにしよう","view":"小さな失敗を全部に広げず、その出来事まで戻す","source":"ことばの距離プロジェクト独自の実践","text":"""料理してて、\n「あ、味濃くなった」って日がある。\n\nそんなときまで\n「失敗した〜」って大きく言わなくても、\n\n「今日はちょっと濃かった」\n\nくらいでいいんですよね。\n\n次は少し控えめにしよう。\nそれで終わりw"""},
{"id":"KTK-20260813-AM","date":"2026/08/13","slot":"morning","type":"life","scene":"朝から同じ曲を繰り返し聴く","first":"また同じ曲聴いてる","flat":"今これが気に入ってる","positive":"飽きるまで聴く","view":"音楽のある日常を軽く出す","source":"goroの日常投稿","text":"""おはようございます☺️\n\n気に入った曲があると、\nしばらく同じ曲ばっかり聴くタイプですw\n\n朝からもう何回目だろう。\n\n飽きるまで聴きます🎧"""},
{"id":"KTK-20260813-PM","date":"2026/08/13","slot":"evening","type":"attack_reframe","scene":"駅の列に割り込まれる場面を思い出す","first":"なんだこいつ。常識ないな","flat":"割り込まれた、その行動が嫌だった","positive":"人全部まで嫌いにしなくていい","view":"人と、その人の行動を分ける","source":"goroの実例／ことばの距離プロジェクト独自の実践","text":"""駅で並んでる列に\nスッと入られたら、\n自分は普通にイラッとします。\n\n「なんだこいつ」\nくらいは思うw\n\nでも少し経ったら、\n\n「あの人が嫌い」じゃなくて\n「割り込まれたのが嫌だった」\n\nくらいまで戻すようにしてます。\n\n嫌な行動と、\nその人全部は分けておきたい。"""},
{"id":"KTK-20260814-AM","date":"2026/08/14","slot":"morning","type":"life","scene":"金曜の朝、帰宅後の楽しみを考える","first":"今日も仕事","flat":"帰ったら何作ろう","positive":"夜の楽しみをひとつ持つ","view":"朝からネガティブを持ち込まず生活の楽しみを置く","source":"goroの日常投稿","text":"""おはようございます☺️\n\n今日は帰ったら何作ろうかな。\n\n仕事中に思いついたら\n忘れないようにメモしときますw\n\n金曜日、いってきます☕"""},
{"id":"KTK-20260814-PM","date":"2026/08/14","slot":"evening","type":"life_distance","scene":"仕事のあと料理をして気分が切り替わる","first":"まだ仕事のことが頭に残ってる","flat":"いまは玉ねぎ切ってる","positive":"生活に戻ると少し離れることがある","view":"嫌なことを全部整理しなくても、自分の生活へ戻ることで距離ができる","source":"goroの生活実感／ことばの距離プロジェクト独自の実践","text":"""仕事でちょっと引っかかることがあっても、\n\n帰って料理して、\n玉ねぎ切って、\n肉焼いて、\n味見してるうちに、\n\n気づいたら別のこと考えてたりする。\n\n嫌なことって、\n全部きれいに整理しなくても\n自分の生活に戻ると\n少し離れることもありますね。"""},
{"id":"KTK-20260815-AM","date":"2026/08/15","slot":"morning","type":"life","scene":"休日の朝にやりたいことがいくつも浮かぶ","first":"あれもこれもやりたい","flat":"やりたいことが多い","positive":"できたものから楽しむ","view":"休日のわくわくをそのまま出す","source":"goroの日常投稿","text":"""おはようございます☺️\n\n休みの日ほど、\nやりたいことが増える。\n\nAIも触りたい。\n料理もしたい。\n音楽もやりたい。\n\nたぶん全部は終わりませんw\n\nできたものから楽しみます😂"""},
{"id":"KTK-20260815-PM","date":"2026/08/15","slot":"evening","type":"life","scene":"片付け中に別のことへ脱線する","first":"片付けしよう","flat":"途中で別のものが気になった","positive":"まあこういう日もある","view":"学びにせず、自分ツッコミだけで終える生活投稿","source":"goroの日常投稿","text":"""片付けしようと思って始めたのに、\n\n途中で昔のもの見つけて、\nそこから完全に別のことしてましたw\n\nこういう脱線、よくあります😂\n\n片付けは……また続きやります。"""},
{"id":"KTK-20260816-AM","date":"2026/08/16","slot":"morning","type":"life","scene":"休日の朝をゆっくり始める","first":"今日は何しよう","flat":"まずコーヒー","positive":"決めすぎず始める","view":"余白のある朝投稿","source":"goroの日常投稿","text":"""おはようございます☺️\n\n日曜日。\n\n今日は何しようかな。\n\nとりあえずコーヒー飲みながら考えます☕\n\n予定を決める前の時間も好きです。"""},
{"id":"KTK-20260816-PM","date":"2026/08/16","slot":"evening","type":"temporal_distance","scene":"目の前のことを大きく感じたとき、遠い時間から見る","first":"このことばかり気になる","flat":"10万年後から見たら、今日のこれはどのくらいだろう","positive":"じゃあ今の時間を何に使いたいかへ戻る","view":"遠くを見ることで今の大切なものへ戻る","source":"goroの考え／Temporal distancingと隣接するが10万年という尺度自体は独自","text":"""たまに、\nものすごく遠くから今を見ることがあります。\n\n10万年後。\n\nそこから見たら、\n今日気にしてることって\nどのくらいの大きさなんだろう。\n\nだから「どうでもいい」じゃなくて、\n\nじゃあ今の時間を\n何に使いたいかなって戻ってくる。\n\n遠くを見ると、\n今が大切になる。"""},
{"id":"KTK-20260817-AM","date":"2026/08/17","slot":"morning","type":"life","scene":"新しい週の朝、気になることをメモする","first":"今週もいろいろやりたい","flat":"思いついたらメモする","positive":"ひとつずつ楽しむ","view":"月曜でもマイナスから始めず、好奇心を出す","source":"goroの日常投稿","text":"""おはようございます☺️\n\n今週も、\n気になること思いついたら\nとりあえずメモしていきますw\n\n仕事も、遊びも、\n気になったことも。\n\n今週もよろしくお願いします☕"""},
{"id":"KTK-20260817-PM","date":"2026/08/17","slot":"evening","type":"self_reflection","scene":"一日の終わりにできなかったことより、できたことをひとつ思い出す","first":"あれもできなかった","flat":"今日はこれをやった","positive":"一日全部を未完了のことで決めない","view":"できなかった一つを一日全体へ広げない","source":"ことばの距離プロジェクト独自の実践","text":"""一日の終わりって、\nできなかったことの方を\n思い出すことがあります。\n\nあれもやってない。\nこれも途中。\n\nでも今日は、\nできたこともちゃんとある。\n\n全部できなかった日じゃなくて、\n途中のものもあった日。\n\n自分はそれくらいにして、\n今日は終わりにします🌙"""}
]


def norm_date(value):
    return str(value or "").strip().replace("-", "/")


def main():
    creds, _ = google_auth_default(scopes=SCOPES)
    gc = gspread.authorize(creds)
    ss = gc.open_by_key(SPREADSHEET_ID)
    queue = ss.worksheet("投稿キュー")
    stock = ss.worksheet("ネタストック")

    q_values = queue.get_all_values()
    if q_values:
        header = q_values[0]
        date_i = header.index("投稿日")
        posted_i = header.index("投稿済")
        for rownum in range(len(q_values), 1, -1):
            row = q_values[rownum - 1]
            date = norm_date(row[date_i] if date_i < len(row) else "")
            posted = str(row[posted_i] if posted_i < len(row) else "").strip().upper()
            if date in TARGET_DATES and posted != "TRUE":
                queue.delete_rows(rownum)

    s_values = stock.get_all_values()
    if s_values:
        header = s_values[0]
        id_i = header.index("ID")
        ids = {p["id"] for p in POSTS}
        for rownum in range(len(s_values), 1, -1):
            row = s_values[rownum - 1]
            rid = str(row[id_i] if id_i < len(row) else "").strip()
            if rid in ids:
                stock.delete_rows(rownum)

    queue_rows = []
    stock_rows = []
    for p in POSTS:
        queue_rows.append([p["date"], p["slot"], p["text"], p["type"], p["id"], "FALSE", "", ""])
        stock_rows.append([p["id"], p["date"], p["scene"], p["first"], p["type"], p["flat"], p["positive"], p["view"], p["source"], "FALSE"])

    queue.append_rows(queue_rows, value_input_option="USER_ENTERED")
    stock.append_rows(stock_rows, value_input_option="USER_ENTERED")
    print(f"success queue={len(queue_rows)} stock={len(stock_rows)} spreadsheet={SPREADSHEET_ID}")

if __name__ == "__main__":
    main()
