# Threads x note 自動運用システム

**おつまみごろー**（@otsumamigoro）の Threads 自動投稿 x note 収益化システム

## 概要

キッチン便利グッズ x パパッと一品をテーマに、Threads への自動投稿と note 記事による収益化を行うシステムです。GitHub Actions + Google Sheets + Threads API で運用し、月間作業時間90分以内を目指します。

## アーキテクチャ

手動（週1回）: リサーチ → Claude → Google Sheets 投稿キュー
自動（毎日2回）: GitHub Actions (cron) → src/post.py → Threads API → Sheets 投稿ログ更新

## ディレクトリ構成

.github/workflows/ - GitHub Actions ワークフロー
config/ - ジャンル設定（active.yml）
docs/ - 設計書・開発ルール・決定ログ
prompts/ - プロンプトテンプレート
src/ - Python スクリプト
data/ - バックアップデータ（git-ignored）

## 主要ファイル

src/post.py - 投稿メインスクリプト
src/threads_api.py - Threads API ラッパー
src/sheets.py - Google Sheets 操作
src/insights.py - 週次インサイト収集
src/token_check.py - 月次トークン有効性チェック
src/utils.py - 共通ユーティリティ

## ワークフロー

post-morning.yml - 毎日 7:00 JST 朝の投稿
post-evening.yml - 毎日 20:00 JST 夜の投稿
weekly-insights.yml - 毎週月曜 9:00 JST インサイト収集
monthly-token-check.yml - 毎月1日 9:00 JST トークンチェック

## セットアップ

1. GitHub Secrets に登録: KURASHI_ACCESS_TOKEN, KURASHI_USER_ID, GOOGLE_SHEETS_CREDENTIALS
2. Google Sheets にサービスアカウントを編集者として共有
3. config/active.yml を環境に合わせて編集

## ドキュメント

docs/design_document_v1.0.md - 設計書 v1.0
docs/RULES.md - 開発ルール
docs/DECISIONS.md - 決定ログ
docs/BACKLOG.md - バックログ

## ライセンス

Private repository - Not for redistribution.
