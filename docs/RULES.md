# threads-note-autopilot - 開発ルール

最終更新: 2026-08-09

## 1. 基本原則

1. 目的・要件・制約・影響範囲を確認してから実装する
2. 既存の動作するコードを理由なく壊さない
3. シンプルで保守しやすい実装を優先する
4. 外部API・認証情報・ファイルパスは実在確認してから使う
5. 変更後は構文・ユニットテスト・差分レビューを行う
6. 現フェーズ外の改善は `BACKLOG.md` に送る
7. 重要な設計判断は `DECISIONS.md` に残す
8. 不明な仕様は推測で実装しない

## 2. 実装プロセス

Plan → Execute → Test/Check → Review → Improve の順で進める。

### Plan

- 変更対象
- 影響範囲
- 外部依存
- ロールバック方法

を短く整理する。

5ファイル以上に影響する変更は、人間の承認後に実施する。

### Execute

- feature branch で変更する
- 1コミット1目的を目安にする
- Secretや認証情報をコミットしない

### Test/Check

最低限:

- Python構文チェック
- 追加・変更した純粋ロジックのユニットテスト
- YAML構文確認
- mainとの差分確認

外部APIを実際に叩くE2Eは、認証情報と投稿先を確認してから手動実行する。

### Review

- 旧アカウント固有語が残っていないか
- 時刻がJST基準か
- Secret名が統一されているか
- 自動投稿が意図せず有効化されていないか
- ことばの距離の発信方針から外れていないか

### Improve

テスト・レビューで見つかった問題だけ直す。
フェーズ外の改善を混ぜない。

## 3. Single Source of Truth

新しい作業を始めるときは次を読む。

1. `docs/RULES.md`
2. `docs/design_document_v2.0.md`
3. `docs/DECISIONS.md`
4. `docs/BACKLOG.md`

AIや会話履歴より、リポジトリ上の最新版を優先する。

## 4. Gitルール

- mainへ直接実装しない
- `feat/*` / `fix/*` 等のfeature branchを使う
- テストと差分確認後にPRでmainへ反映する
- コミットメッセージは `feat:` `fix:` `docs:` `test:` `refactor:` `ci:` `chore:` を使う
- 問題があればbranchを破棄してmainへ戻せる状態を保つ

## 5. セキュリティ

以下は絶対にコミットしない。

- Threads Access Token
- Threads User IDを含むローカル設定ファイル
- Google Service Account JSON
- Spreadsheet IDを含む `config/active.yml`
- `.env*`

GitHub ActionsではGitHub Secretsを使用する。

現行Secret名:

- `THREADS_ACCESS_TOKEN`
- `THREADS_USER_ID`
- `SPREADSHEET_ID`
- `GOOGLE_SHEETS_CREDENTIALS`

## 6. タイムゾーン

日時が関係する処理は `Asia/Tokyo` / JST を正とする。

GitHub Actions cronはUTCだが、
Sheets上の日付判定・ログ日時はJSTで処理する。

## 7. コンテンツ安全ルール

ことばの距離の生成・運用では以下を守る。

- ネガティブ感情を否定しない
- ポジティブを強制しない
- 他人を断罪・嘲笑しない
- 他責を自責へ極端に反転させない
- 相手の責任と、自分が次に選べる行動を分ける
- 心理学・医学の専門家を装わない
- 研究結果を万能な事実として断定しない
- 出典が必要な内容は確認してから投稿する

## 8. テスト方針

### 純粋ロジック

標準ライブラリ `unittest` でテストする。

### 外部依存

Threads API / Google Sheets APIはモックを優先する。
実アカウントへの投稿テストは `workflow_dispatch` で明示的に行う。

### 回帰確認

投稿処理を変更した場合は最低限:

- morning / evening のキュー選択
- JST日付判定
- 投稿済みフラグ
- エラー時のERROR記録

を確認する。

## 9. ファイルサイズ

| 種別 | 分割検討 | 上限目安 |
|---|---:|---:|
| Python | 200行 | 250行 |
| YAML | 120行 | 150行 |
| Markdown | 250行 | 300行 |

必要性がない分割・抽象化はしない。

## 10. 現在の技術的負債

詳細は `docs/BACKLOG.md` を正とする。

主な未対応:

- Threads API `topic_tag` 対応
- Insights追加メトリクス
- Long-Lived Token refreshの正式実装
- note関連機能の再設計

## 11. 変更履歴

- 2026-03-17: 初版
- 2026-08-09: ことばの距離 Phase 1 に合わせて簡素化・更新
