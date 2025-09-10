# コーディング規約とスタイル

## コードフォーマッター
- **Black**: Python標準のコードフォーマッター
- **isort**: importの自動ソート
- **Flake8**: リンター

## コーディングスタイル
- Python 3.11+の機能を使用
- 型ヒントを使用（例: `self.bot: commands.Bot`）
- クラスベースの実装（discord.pyのCogシステム）
- async/awaitパターンを使用

## 命名規則
- クラス名: PascalCase（例: `BaseUserCog`, `EventModel`）
- 関数/メソッド名: snake_case（例: `on_ready`, `get_event`）
- ファイル名: snake_case（例: `base_cog.py`, `event_service.py`）
- モデルクラス: `*Model`の命名規則（例: `EventModel`, `PreferenceModel`）

## プロジェクト構造の規約
- Cogシステム: 全てのCogは`BaseUserCog`を継承
- レイヤードアーキテクチャ:
  - cogs: Discord機能モジュール
  - service: ビジネスロジック
  - repository: データアクセス層
  - model: SQLAlchemyモデル
  - entity: ドメインエンティティ
  - common: 共通ユーティリティ

## 開発時の注意点
- コミット前に必ず`black`と`isort`を実行
- モデル変更時は必ずAlembicマイグレーションを作成
- Discord APIエラーは適切にキャッチしてユーザーフレンドリーなメッセージを返す
- ログは`app/common/logging_config.py`で設定されたロガーを使用