# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

このプロジェクトは、アイドルマスターのライブイベントを管理するDiscord Botです。主な機能：
- Discordのスケジュールイベントの作成・管理
- ユーザーの好きなアイドル情報の登録・検索

## 技術スタック

- **言語**: Python 3.11+
- **Botフレームワーク**: discord.py 2.4.0
- **データベース**: SQLite3 + SQLAlchemy 2.0.35
- **マイグレーション**: Alembic 1.15.2
- **パッケージ管理**: Poetry
- **コード品質**: Black, Flake8, isort

## 開発コマンド

```bash
# 依存関係のインストール
poetry install

# Botの起動
poetry run python main.py

# コードフォーマット（実行前に必須）
poetry run black .
poetry run isort .

# コードチェック
poetry run flake8

# データベースマイグレーション適用
poetry run alembic upgrade head

# 新しいマイグレーション作成
poetry run alembic revision --autogenerate -m "変更内容の説明"

# マイグレーションのダウングレード
poetry run alembic downgrade -1
```

## アーキテクチャ

### レイヤー構成
```
app/
├── cogs/          # Discord.pyのCog（機能モジュール）
├── model/         # SQLAlchemyモデル（DBスキーマ定義）
├── repository/    # データアクセス層（CRUD操作）
├── service/       # ビジネスロジック層
├── entity/        # ドメインエンティティ
└── common/        # 共通ユーティリティ
```

### 主要コンポーネント

1. **Cogシステム**: discord.pyのCogを使用して機能を分離
   - `base_cog.py`: 全Cogの基底クラス
   - `event.py`: イベント管理コマンド群
   - `preferences.py`: アイドル好み設定コマンド群

2. **データベース設計**:
   - `EventModel`: Discordイベント情報を管理
   - `EventJoinModel`: イベント参加者情報を管理
   - `PreferenceModel`: ユーザーの好きなアイドル情報を管理

3. **サービス層**: ビジネスロジックを実装
   - `event_service.py`: イベント関連のロジック
   - `preferences_service.py`: アイドル好み関連のロジック

## 開発時の注意点

1. **コード品質**: コミット前に必ず`black`と`isort`を実行
2. **データベース変更**: モデル変更時は必ずAlembicマイグレーションを作成
3. **エラーハンドリング**: Discord APIエラーは適切にキャッチして、ユーザーフレンドリーなメッセージを返す
4. **ログ**: `app/common/logging_config.py`で設定されたロガーを使用

## 環境設定

必要な環境変数（config/ディレクトリで管理）:
- Discord Botトークン: `config/discord.py`で設定
- データベース名: `config/db.py`で設定（デフォルト: idol_mster.db）