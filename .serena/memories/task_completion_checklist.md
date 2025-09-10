# タスク完了時のチェックリスト

## コード変更後に必ず実行すること

1. **コードフォーマット（必須）**
   ```bash
   poetry run black .
   poetry run isort .
   ```

2. **リントチェック**
   ```bash
   poetry run flake8
   ```

3. **データベース変更がある場合**
   - モデル変更時は必ずAlembicマイグレーションを作成
   ```bash
   poetry run alembic revision --autogenerate -m "変更内容の説明"
   poetry run alembic upgrade head
   ```

4. **テスト実行**
   - テストがある場合は実行して確認

5. **動作確認**
   - Discord Botを起動して機能が正しく動作することを確認
   ```bash
   poetry run python main.py
   ```

6. **エラーハンドリング確認**
   - Discord APIエラーが適切にキャッチされているか
   - ユーザーフレンドリーなメッセージが返されるか

## 重要な注意事項
- **コミット前には必ず**`black`と`isort`を実行する
- 環境変数の設定は`config/`ディレクトリで管理
- ログ出力は統一されたロガーを使用