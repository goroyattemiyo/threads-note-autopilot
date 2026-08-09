# ことばの距離 - Threads 運用基盤

**goro｜ことばの距離**（@goro_kotobanokyori）の Threads 投稿・検証システムです。

## 目的

日常の小さなイライラ、不安、言い訳、他責、攻撃的な言葉に対して、
無理にポジティブへ飛ばず、まず言葉と視点の距離を取り直す発信を続けます。

基本方針は次の順番です。

**ネガティブ → フラット → できれば少しポジティブ**

フラットで止めてもよいことを前提にします。

このリポジトリは単なる自動投稿機ではなく、
「どんな言葉の変換が人に届いたか」を蓄積・検証するための運用基盤です。

## 現在のフェーズ

Phase 1: Threads 投稿基盤の転生・最小運用

- 朝 7:00 JST / 夜 20:00 JST の投稿枠を維持
- Google Sheets の投稿キューから投稿
- 投稿結果とインサイトを記録
- 投稿文は人間が確認してからキューへ入れる
- note の自動生成・販売導線は当面停止

## アーキテクチャ

手動:

ネタ・原体験・本や研究からの気づき
→ Google Sheets「ネタストック」
→ 投稿文を生成・人間レビュー
→ Google Sheets「投稿キュー」

自動:

GitHub Actions
→ `src/post.py`
→ Threads API
→ Google Sheets「投稿ログ」

週次:

GitHub Actions
→ `src/insights.py`
→ Google Sheets「インサイト」
→ 次週の投稿仮説へ反映

## 投稿時間

- 朝: 7:00 JST
  - 今日を少し楽に始める
  - 前を向けるところまで戻す
- 夜: 20:00 JST
  - 今日抱えたものを少し下ろす
  - 明日まで持ち越さなくてよい余白をつくる

GitHub Actions の cron は UTC で設定しています。
投稿対象日の判定と投稿ログは `Asia/Tokyo` を基準にします。

## Google Sheets

### 投稿キュー

`投稿日 / 時間帯 / 投稿文 / 種別 / ネタID / 投稿済 / 投稿ID / エラー`

### ネタストック

`ID / 日付 / 場面 / 最初の言葉 / カテゴリ / フラットな言葉 / 少し前向きな言葉 / 視点変更 / 根拠/出典 / 使用済`

主なカテゴリ例:

- `reassurance`
- `neutral_reframe`
- `temporal_distance`
- `other_blame`
- `attack_reframe`
- `excuse_to_action`
- `self_reflection`

## 主要ファイル

- `src/post.py` - 投稿メインスクリプト
- `src/threads_api.py` - Threads API ラッパー
- `src/sheets.py` - Google Sheets 操作
- `src/setup_sheets.py` - Sheets 初期セットアップ
- `src/insights.py` - 週次インサイト収集
- `src/token_check.py` - 月次トークン確認
- `prompts/kotoba_no_kyori/threads_post.md` - 投稿生成方針
- `config/_template.yml` - プロジェクト設定テンプレート

## GitHub Actions

- `post-morning.yml` - 毎日 7:00 JST
- `post-evening.yml` - 毎日 20:00 JST
- `weekly-insights.yml` - 毎週月曜 9:00 JST
- `monthly-token-check.yml` - 毎月1日 9:00 JST

## 必要な GitHub Secrets

- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`
- `SPREADSHEET_ID`
- `GOOGLE_SHEETS_CREDENTIALS`

旧 `KURASHI_ACCESS_TOKEN` / `KURASHI_USER_ID` は使用しません。

## セットアップ方針

1. 「ことばの距離」用 Threads の User ID / Access Token を取得
2. 「ことばの距離」用 Google Spreadsheet を用意
3. サービスアカウントを Spreadsheet の編集者として共有
4. 上記4つの GitHub Secrets を設定
5. `src/setup_sheets.py` でシート構成を作成
6. `workflow_dispatch` で手動テスト
7. 問題がなければ朝・夜の定期実行を有効化

既存のおつまみごろー用Spreadsheetを再利用する場合は、
`setup_sheets.py` がヘッダーを新スキーマへ更新するため、必要な旧データを先に退避してください。

## note について

note の収益化機能・記事量産は現在のフェーズでは使用しません。
Threads で思想・反応・自分の言葉を十分に育ててから再検討します。

既存の `src/note_html.py` 等は将来利用できるため残しています。

## 旧おつまみごろー

旧プロンプトは `archive/otsumamigoro/` に退避しています。
過去の設計や記事は Git 履歴からも参照できます。

## 開発

作業は feature branch で行い、差分確認・テスト後に main へ反映します。
