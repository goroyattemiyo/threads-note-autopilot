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

### 検討視点
- アーキテクチャ: 投稿基盤は十分再利用可能。ジャンル汎用化より専用化を優先
- QA: GitHub Actions朝投稿でUTC日付を使うとJST日付とずれる可能性がある
- コンテンツ: 商品紹介向けプロンプト・Sheetsスキーマは新テーマと不整合
- セキュリティ/運用: 旧 `KURASHI_*` Secret名とSpreadsheet IDのハードコードを除去すべき

### 決定
1. 投稿基盤 `post.py` / `threads_api.py` / `sheets.py` / Actions / Insights は再利用する
2. Sheetsの日付判定とログ日時は `Asia/Tokyo` に統一する
3. Secret名を `THREADS_ACCESS_TOKEN` / `THREADS_USER_ID` / `SPREADSHEET_ID` に汎用化する
4. ネタストックを「場面・最初の言葉・フラット・少し前向き・視点変更・根拠/出典」へ変更する
5. 投稿思想を「ネガティブ → フラット → できれば少しポジティブ」とする
6. noteの自動量産・CTA・収益化はPhase 1では停止する
7. 旧おつまみ用プロンプトは `archive/otsumamigoro/` へ退避する
8. mainへ直接変更せず `feat/kotoba-no-kyori-phase1` で実装し、テスト後にPRとする

### 影響範囲
- `src/post.py`
- `src/sheets.py`
- `src/setup_sheets.py`
- `src/utils.py`
- GitHub Actions 4本
- `config/_template.yml`
- `prompts/`
- README / docs

### ロールバック
`feat/kotoba-no-kyori-phase1` を破棄すればmainは旧状態のまま維持される。

### 未実装として残すもの
- Threads API `topic_tag`
- Insights追加メトリクス
- Long-Lived Token refresh正式実装
- note再設計
