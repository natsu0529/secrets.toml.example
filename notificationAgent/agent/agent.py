# run_agent_local.py

# 必要なライブラリをインポート
from google.adk.agents import Agent
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 環境変数を読み込むライブラリ
from dotenv import load_dotenv
load_dotenv()


# --- 1. カスタムツールの定義 ---

def get_current_datetime() -> str:
    """
    現在の曜日と時刻を文字列で取得する。
    """
    now = datetime.datetime.now()
    print(f"DEBUG: [ツール実行] get_current_datetime() -> {now.strftime('%A %H:%M')}")
    # weekday()は月曜=0, 火曜=1, ...
    return f"Today is {now.weekday()}, current time is {now.hour}:{now.minute}"

def get_location_status() -> dict:
    """
    現在の位置情報を取得し、学校にいるか判定。
    """
    print("DEBUG: [ツール実行] get_location_status()")
    # テスト用に常に「学校外」を返す
    return {"status": "success", "at_school": False, "location_description": "自宅（学校外）"}

def send_professor_email(professor_email_address: str, subject: str, body: str) -> str:
    """
    Gmail経由で指定された教授へメールを送信する。
    """
    print(f"DEBUG: [ツール実行] send_professor_email(to='{professor_email_address}')")

    # 環境変数からGmailの認証情報を取得
    from_address = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not from_address or not app_password:
        error_message = "エラー: 環境変数 GMAIL_ADDRESS または GMAIL_APP_PASSWORD が設定されていません。"
        print(error_message)
        return error_message

    # メールメッセージを作成
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = from_address
    msg['To'] = professor_email_address

    # GmailのSMTPサーバーに接続してメールを送信
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(from_address, app_password)
            smtp.send_message(msg)
        
        success_message = f"送信成功: {professor_email_address} 宛にメールを送信しました。"
        print(success_message)
        return success_message
    except Exception as e:
        error_message = f"メール送信中にエラーが発生しました: {e}"
        print(error_message)
        return error_message


# --- 2. ルートエージェントの定義 ---
# ▼▼▼▼▼ ここが修正点です ▼▼▼▼▼
# 変数名を 'agent' から 'root_agent' に戻します
root_agent = Agent(
    name="professor_notification_agent",
    model="gemini-1.5-flash",
    description="特定の条件（月曜13時＆学校外）の時だけ、教授へ欠席連絡メールを自動送信するエージェント。",
    instruction="""
    あなたは、指示を受けるとタスクを実行する、非常に忠実なアシスタントです。

    # 行動フロー
    1.  まず `get_current_datetime` ツールを呼び出し、現在の曜日と時刻を確認します。曜日は数値（月曜=0）で返されます。
    2.  もし、現在が「月曜日の13時台」である場合のみ、次のステップに進みます。それ以外の曜日・時刻の場合は、「実行条件を満たしませんでした」と報告して処理を終了してください。
    3.  次に `get_location_status` ツールで、現在地が学校内か学校外かを確認します。
    4.  もし、学校外（`at_school`が`False`）の場合のみ、`send_professor_email` ツールを使って、以下の内容でメールを送信してください。
        - 宛先: `kubo@logopt.com`
        - 件名: `本日の授業について`
        - 本文: `久保先生、2323025の鈴木夏大です。本日の授業は体調不良のため欠席させていただきます。`
    5.  学校内にいる場合は、メールは送信せずに「学校にいるためメールは送信しませんでした」と報告してください。
    6.  最終的な実行結果をまとめて、簡潔にユーザーに報告してください。
    """,
    tools=[
        get_current_datetime,
        get_location_status,
        send_professor_email,
    ],
)


# --- 3. ターミナルから直接実行するためのメイン処理 ---
def main():
    """
    このスクリプトを直接実行した際のメイン処理。
    """
    print("--- 教授への自動通知エージェント（ターミナル実行版） ---")
    print("エージェントにタスクの実行を指示します...")
    
    # エージェントに固定の指示を与えて実行
    # instructionに全てのロジックが書かれているため、指示はシンプルでOK
    # ▼▼▼▼▼ ここも修正点です ▼▼▼▼▼
    # 'agent.run' ではなく 'root_agent.run' を呼び出します
    result = root_agent.run("指示に従い、タスクを実行してください。")
    
    print("\n--- 実行結果 ---")
    print(result)
    print("--------------------")

# このファイルが直接実行された場合にのみ、main()関数を呼び出す
if __name__ == "__main__":
    main()