import pandas as pd
from analyzer import calculate_features

# ログファイル名（recorder.pyと同じ設定にする）
LOG_FILE = "keystroke_log.csv"

def analyze_my_log():
    try:
        print(f"📂 {LOG_FILE} を読み込んでいます...")
        df = pd.read_csv(LOG_FILE)
        
        if df.empty:
            print("⚠️ データが空です。recorder.py を実行してキーを叩いてください。")
            return

        print(f"📊 {len(df)} 行のデータを分析中...")
        features = calculate_features(df)
        
        print("\n" + "="*30)
        print("   あなたのキーストローク分析結果")
        print("="*30)
        print(f"🔹 平均ホールド時間 (Hold Time) : {features['mean_hold_time']:.4f} 秒")
        print(f"🔹 平均フライト時間 (Flight Time): {features['mean_flight_time']:.4f} 秒")
        print(f"🔹 有効サンプル数              : {features['hold_time_count']} キー")
        print("="*30)
        
        # 簡易診断（研究の仮説に基づく）
        ht = features['mean_hold_time']
        if ht > 0.15: # 仮の閾値
            print("💡 少し指の動きがゆっくりかもしれません（疲労の可能性？）")
        else:
            print("🚀 軽快にタイプできています！")

    except FileNotFoundError:
        print(f"❌ {LOG_FILE} が見つかりません。まずは python recorder.py を実行してください。")

if __name__ == "__main__":
    analyze_my_log()

