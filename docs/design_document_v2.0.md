# ことばの距離 Threads 運用基盤 設計書 v2.0

> 作成日: 2026-08-09
> 対象: goroyattemiyo/threads-note-autopilot
> ステータス: Phase 1

## 1. ミッション

日常の小さな悩み・イライラ・他責・攻撃的な言葉を、無理にポジティブへ飛ばさず、ことばと視点を少し遠ざけて扱いやすくする。

発信の基本変換は **ネガティブ → フラット → できれば少しポジティブ**。フラットで止めることを許容する。

## 2. アカウント

- 表示名: goro｜ことばの距離
- Threads: @goro_kotobanokyori
- Instagram: 同一ブランドで運用
- note: 専用アカウントは保持するが、Phase 1では収益化・量産を行わない

## 3. 投稿ポリシー

### 朝 7:00 JST

- 今日を少し楽に始める
- 前を向けるところまで戻す
- フラット〜軽いポジティブを中心にする

### 夜 20:00 JST

- 今日抱えたものを少し下ろす
- 嫌な出来事を人生全体へ広げない
- 明日まで持ち越さなくてよい余白をつくる

### 投稿カテゴリ

- reassurance
- neutral_reframe
- temporal_distance
- other_blame
- attack_reframe
- excuse_to_action
- self_reflection

## 4. 言葉の安全設計

- ネガティブ感情そのものを否定しない
- 「考え方次第」「気にしなければいい」で片付けない
- ポジティブを強制しない
- 他責な人・ネガティブな人を断罪しない
- 相手の責任と自分の行動選択を分ける
- 心理・医学の専門家を装わない
- 研究は出典確認し、万能効果として断定しない
- 安心を届ける投稿では絵文字を1〜2個まで使用可
- CTAを毎投稿必須にしない

## 5. システム構成

### 手動

原体験 / 日常の気づき / 本 / 研究
→ Sheets「ネタストック」
→ 投稿文生成
→ 人間レビュー
→ Sheets「投稿キュー」

### 自動

GitHub Actions
→ GitHub OIDC
→ Google Cloud Workload Identity Federation
→ サービスアカウント権限借用
→ Application Default Credentials
→ `src/post.py`
→ Threads API / Google Sheets

### 週次

GitHub Actions
→ WIF認証
→ `src/insights.py`
→ Sheets「インサイト」
→ 投稿カテゴリ別に反応を振り返る

## 6. Google Sheets スキーマ

### 投稿キュー

投稿日 / 時間帯 / 投稿文 / 種別 / ネタID / 投稿済 / 投稿ID / エラー

### ネタストック

ID / 日付 / 場面 / 最初の言葉 / カテゴリ / フラットな言葉 / 少し前向きな言葉 / 視点変更 / 根拠/出典 / 使用済

### 投稿ログ

投稿日時 / 投稿ID / 投稿文 / 種別 / ステータス

### インサイト

取得日 / 投稿ID / views / likes / replies / reposts / quotes

## 7. タイムゾーン

日時判定は `Asia/Tokyo` / JST を基準にする。

- 朝7:00 JST = 前日22:00 UTC
- 夜20:00 JST = 11:00 UTC

Sheets上の「投稿日」の判定はActionsホストのローカル時刻ではなくJSTで行う。

## 8. 認証・Secrets

Threads:

- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`

Google Sheets:

- `SPREADSHEET_ID`
- GitHub Actions OIDC + Google Cloud WIF
- `google-github-actions/auth@v3`
- Python側は `google.auth.default()` を使用

サービスアカウントJSONキーおよび `GOOGLE_SHEETS_CREDENTIALS` は使用しない。

WIFのGoogle Cloud側では、GitHubリポジトリのmainブランチから来るOIDC subjectだけにサービスアカウント権限借用を許可する。

## 9. note

Phase 1では停止。

実施しないこと:
- 月次記事ノルマ
- 有料記事の先行作成
- Threads投稿ごとのnote CTA
- 価格A/Bテスト

再開条件:
- Threads上で発信テーマが十分に育っている
- 読者が深掘りを求めるテーマが見えている
- goro自身が繰り返し書きたいテーマが明確になっている

## 10. KPI

初期は売上ではなく以下を見る。

- views
- replies
- reposts / quotes
- フォローにつながった投稿テーマ
- 投稿カテゴリ別の反応
- 自分が無理なく継続できたか

「いいね」単独で投稿の良し悪しを判断しない。

## 11. Phase 1 完了条件

1. JSTで朝夜の投稿対象日が正しく判定される
2. WIF/ADCでGoogle Sheetsへ接続できる
3. ことばの距離用Sheetsスキーマが用意される
4. 投稿生成プロンプトがことばの距離の思想に一致する
5. 手動 `workflow_dispatch` でテスト投稿できる
6. 1週間の試験運用で致命的なエラーがない

## 12. 後続バックログ

- Threads API `topic_tag` 対応
- Insights追加メトリクス対応
- Access Token refreshの正式実装
- 投稿カテゴリ別の週次自動集計
- note再開設計
