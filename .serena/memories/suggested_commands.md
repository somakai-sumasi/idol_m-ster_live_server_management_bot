# 開発コマンド一覧

## 依存関係管理
```bash
poetry install          # 依存関係のインストール
```

## アプリケーション実行
```bash
poetry run python main.py  # Discord Botの起動
```

## コードフォーマット（実行前に必須）
```bash
poetry run black .      # Blackでコードフォーマット
poetry run isort .      # isortでimportソート
```

## コード品質チェック
```bash
poetry run flake8       # Flake8でリントチェック
```

## データベース操作
```bash
poetry run alembic upgrade head                         # マイグレーション適用
poetry run alembic revision --autogenerate -m "説明"    # 新しいマイグレーション作成
poetry run alembic downgrade -1                         # マイグレーションをロールバック
```

## システムコマンド (Darwin/macOS)
```bash
ls                      # ファイル一覧表示
cd <directory>          # ディレクトリ移動
git status              # Gitステータス確認
git diff                # 変更内容確認
git add .               # 変更をステージング
git commit -m "message" # コミット
git log                 # コミット履歴確認
```