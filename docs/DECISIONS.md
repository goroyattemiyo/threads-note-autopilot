# threads-note-autopilot - 設計判断ログ

## D-001: アーキテクチャ選定
- 日付: 2026-03-17
- 決定: GitHub Actions + Python + Google Sheets + Threads API
- 理由: 低コスト、Git管理しやすい、投稿とログを分離できる

## D-002: Meta Developer 構成
- 日付: 2026-03-17
- 決定: 1アプリ + 複数テストユーザーを基本とする
- 理由: 管理コストを抑えつつ複数アカウントに対応できる

## D-003: 旧アカウント設計（履歴）
- 日付: 2026-03-17
- 決定: 「おつまみごろー」で料理×暮らしを運用
- 状態: 2026-08-09 に終了。現行設計では使用しない

## D-004: コア3ファイル分離
- 日付: 2026-03-17
- 決定: `threads_api.py` / `sheets.py` / `post.py` を分離
- 理由: API通信、データ操作、オーケストレーションの責務を分ける

## D-005: Insights / token check / テンプレート追加
- 日付: 2026-03-17
- 決定: 週次Insights、月次token check、設定・プロンプトテンプレートを追加
- 状態: 基盤として継続利用。コンテンツ固有部分はD-006で置換

## D-006: 「ことばの距離」への全面転生 Phase 1
- 日付: 2026-08-09
- 背景: 旧「おつまみごろー」アカウントを `goro｜ことばの距離` として再利用する
- 承認: 変更方針を提示後、ユーザーから実装承認あり

### 決定
1. 投稿基盤 `post.py` / `threads_api.py` / `sheets.py` / Actions / Insights は再利用する
2. Sheetsの日付判定とログ日時は `Asia/Tokyo` に統一する
3. Secret名を `THREADS_ACCESS_TOKEN` / `THREADS_USER_ID` / `SPREADSHEET_ID` に統一する
4. ネタストックを「場面・最初の言葉・フラット・少し前向き・視点変更・根拠/出典」へ変更する
5. 投稿思想を「ネガティブ → フラット → できれば少しポジティブ」とする
6. noteの自動量産・CTA・収益化はPhase 1では停止する
7. 旧おつまみ用プロンプトは `archive/otsumamigoro/` へ退避する
8. mainへ直接変更せず `feat/kotoba-no-kyori-phase1` で実装し、テスト後にPRとする

## D-007: Google Sheets認証をWIFへ移行
- 日付: 2026-08-09
- 背景: Google Cloudの組織ポリシーによりサービスアカウントJSONキー作成が無効化されていた
- 選択肢: A) 組織ポリシーを解除してJSONキーを発行 B) Workload Identity Federationを利用
- 決定: B) GitHub Actions OIDC + Google Cloud Workload Identity Federation
- 理由: 長期秘密鍵を保持せず、組織ポリシーを弱めずに運用できる
- 実装:
  - GitHub Actionsに `id-token: write` を付与
  - `google-github-actions/auth@v3` でADCを生成
  - Pythonは `google.auth.default()` で認証
  - `GOOGLE_SHEETS_CREDENTIALS` を廃止
  - Sheets初期構築用の手動workflowを追加
- セキュリティ: Google Cloud側の権限借用対象は対象リポジトリのmainブランチに限定

### WIF移行後の必要Secrets
- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`
- `SPREADSHEET_ID`

### ロールバック
WIF関連コミットを戻せば旧JSON方式へ復帰可能。ただし組織ポリシー上JSONキーは発行不可のため、実運用上はWIFを標準とする。

## 未実装として残すもの
- Threads API `topic_tag`
- Insights追加メトリクス
- Long-Lived Token refresh正式実装
- note再設計
