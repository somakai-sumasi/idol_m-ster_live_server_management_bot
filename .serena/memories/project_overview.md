# プロジェクト概要

## プロジェクトの目的
アイドルマスターのライブイベントを管理するDiscord Botプロジェクト

主な機能:
- Discordのスケジュールイベントの作成・管理
- ユーザーの好きなアイドル情報の登録・検索

## 技術スタック
- **言語**: Python 3.11+
- **Botフレームワーク**: discord.py 2.4.0
- **データベース**: SQLite3 + SQLAlchemy 2.0.35
- **マイグレーション**: Alembic 1.15.2
- **パッケージ管理**: Poetry
- **コード品質**: Black, Flake8, isort

## 主な依存関係
- discord-py ^2.4.0
- sqlalchemy ^2.0.35
- alembic ^1.15.2
- black ^24.8.0
- flake8 ^7.1.1
- isort ^5.13.2
- requests ^2.32.4
- beautifulsoup4 ^4.13.4

## プロジェクト名
idol-m@ster-live-server-management-bot