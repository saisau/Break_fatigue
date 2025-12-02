import csv
import time
from pynput import keyboard
from datetime import datetime

# ログファイルの保存先
LOG_FILE = "keystroke_log.csv"

def on_press(key):
    """キーが押されたときの処理"""
    log_key(key, "PRESS")

def on_release(key):
    """キーが離されたときの処理"""
    log_key(key, "RELEASE")
    # ESCキーで終了
    if key == keyboard.Key.esc:
        print("\n🛑 記録を終了しました。")
        return False

def log_key(key, event_type):
    """キー情報をCSVに書き込む"""
    try:
        # 特殊キーと文字キーの区別
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    # 現在時刻（UNIXタイムスタンプ）
    timestamp = time.time()
    
    # 画面に軽く表示（動作確認用）
    print(f"{event_type}: {key_char}")

    # CSVに追記モード('a')で書き込み
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event_type, key_char])

def main():
    print(f"🚀 キーストローク記録を開始します: {LOG_FILE}")
    print("終了するには 'ESC' キーを押してください...")
    
    # CSVのヘッダーを作成（ファイルがなければ）
    try:
        with open(LOG_FILE, 'x', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event_type", "key_code"])
    except FileExistsError:
        pass # ファイルが既にあれば何もしない

    # リスナーの起動
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()