# 教授への自動欠席連絡エージェント

これは、特定の条件（毎週月曜日の13時台に学校外にいる）を満たした場合に、指定された教授へ自動で欠席連絡メールを送信するためのPythonエージェントです。

GoogleのADK (Agent Development Kit) のコンセプトに基づき、条件判断とツールの実行を分離した構造になっています。

## ✨ 主な機能

- **時刻ベースのトリガー**: スクリプトが実行された時刻が「月曜日の13時台」であるかを判定します。
- **条件分岐**: （モックの）位置情報ツールを呼び出し、学校内にいるか否かを判定します。
- **自動メール送信**: 条件に合致した場合のみ、Gmail経由で事前に設定された内容の欠席メールを送信します。

## 🔧 セットアップと実行方法

### 1. 前提条件

- Python 3.8以上
- Gmailアカウント

### 2. インストール

1.  このプロジェクトをローカルに準備します。

2.  （推奨）Pythonの仮想環境を作成し、有効化します。
    ```bash
    python -m venv venv
    # Windowsの場合
    .\venv\Scripts\activate
    # Mac/Linuxの場合
    source venv/bin/activate
    ```

3.  必要なライブラリをインストールします。
    ```bash
    pip install -r requirements.txt
    ```

### 3. 環境変数の設定

1.  プロジェクトのルートにある `.env` ファイルを開きます。（なければ作成してください）
2.  あなたのGmailアドレスと、Googleアカウントで生成した**アプリパスワード**を記述します。
    ```env
    GMAIL_ADDRESS="your_email_address@gmail.com"
    GMAIL_APP_PASSWORD="your_16_digit_app_password"
    ```

### 4. 実行

ターミナルから以下のコマンドでスクリプトを実行します。
```zsh
adk web