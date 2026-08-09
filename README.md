# ことばの距離 - Threads 運用基盤

**goro｜ことばの距離**（@goro_kotobanokyori）の Threads 投稿・検証システムです。

## 目的

日常の小さなイライラ、不安、言い訳、他責、攻撃的な言葉に対して、無理にポジティブへ飛ばず、まず言葉と視点の距離を取り直す発信を続けます。

基本方針は **ネガティブ → フラット → できれば少しポジティブ**。フラットで止めてもよいことを前提にします。

## 現在のフェーズ

Phase 1: Threads 投稿基盤の転生・最小運用

- 朝 7:00 JST / 夜 20:00 JST の投稿枠
- Google Sheets の投稿キューから投稿
- 投稿結果とインサイトを記録
- 投稿文は人間が確認してからキューへ入れる
- note の自動生成・販売導線は当面停止

## 認証

Threads API は GitHub Secrets の長期アクセストークンを使用します。

Google Sheets はサービスアカウントJSONキーを使わず、GitHub Actions の OIDC と Google Cloud Workload Identity Federation を利用します。`google-github-actions/auth@v3` が Application Default Credentials (ADC) を生成し、Python側は `google.auth.default()` から認証情報を取得します。

## Google Sheets

### 投稿キュー

`投稿日 / 時間帯 / 投稿文 / 種別 / ネタID / 投稿済 / 投稿ID / エラー`

### ネタストック

`ID / 日付 / 場面 / 最初の言葉 / カテゴリ / フラットな言葉 / 少し前向きな言葉 / 視点変更 / 根拠/出典 / 使用済`

主なカテゴリ:

- `reassurance`
- `neutral_reframe`
- `temporal_distance`
- `other_blame`
- `attack_reframe`
- `excuse_to_action`
- `self_reflection`

## GitHub Actions

- `setup-sheets.yml` - Sheets初期構築（手動）
- `post-morning.yml` - 毎日 7:00 JST
- `post-evening.yml` - 毎日 20:00 JST
- `weekly-insights.yml` - 毎週月曜 9:00 JST
- `monthly-token-check.yml` - 毎月1日 9:00 JST
- `test.yml` - ユニットテスト

WIFを使うジョブには `id-token: write` を付与します。

## 必要な GitHub Secrets

- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`
- `SPREADSHEET_ID`

`GOOGLE_SHEETS_CREDENTIALS` は使用しません。

## 初回セットアップ

1. 上記3つのGitHub Secretsを設定
2. SpreadsheetをWIFで使用するサービスアカウントへ編集者共有
3. PRをmainへ反映
4. `Setup Google Sheets` を手動実行
5. 作成されたタブとヘッダーを確認
6. 投稿キューへテスト投稿を1件だけ登録
7. 朝または夜のworkflowを手動実行
8. Threads投稿・投稿ログ・投稿済フラグを確認

## 投稿時間

- 朝: 今日を少し楽に始め、前を向けるところまで戻す
- 夜: 今日抱えたものを少し下ろし、明日まで持ち越さない余白をつくる

日時判定とログは `Asia/Tokyo` / JST を使用します。

## note

Phase 1ではnoteの収益化機能・記事量産は使用しません。Threadsで思想と反応を育ててから再検討します。

## 旧おつまみごろー

旧プロンプトは `archive/otsumamigoro/` に退避しています。過去の設計や記事はGit履歴から参照できます。
