import time
import pandas as pd
import os
from analyzer import detect_fatigue
from jitai import JITAIEngine
from notifier import show_interactive_popup

LOG_FILE = "keystroke_log.csv"
CHECK_INTERVAL = 10  # 10秒ごとにチェック（実際は60秒などが良い）

# optimizer.py で見つけた最適パラメータ（実データから学習）
BEST_HT = 0.175
BEST_FT = 0.270


def get_recent_data(filepath, seconds=60):
    """
    直近n秒のデータだけをCSVから読み込む
    """
    if not os.path.exists(filepath):
        return pd.DataFrame()
        
    # 全読み込みは遅いので、運用では工夫が必要だが、一旦Pandasで読む
    try:
        df = pd.read_csv(filepath)
        if df.empty: return df
        
        current_timestamp = time.time()
        # timestamp列でフィルタリング
        recent_df = df[df['timestamp'] > (current_timestamp - seconds)]
        return recent_df
    except Exception as e:
        print(f"Read Error: {e}")
        return pd.DataFrame()


def main():
    print("👀 疲労監視モニターを起動しました...")
    print(f"   パラメータ: HT>{BEST_HT}, FT>{BEST_FT}")
    
    jitai = JITAIEngine()
    jitai.min_interval_sec = 60 # デモ用に1分間隔に短縮中
    
    while True:
        # 1. データ取得
        df = get_recent_data(LOG_FILE, seconds=60)
        
        if len(df) < 10:
            print(f"⏳ データ収集中... ({len(df)} keys / min)")
        else:
            # 2. 疲労判定
            is_fatigued, feats = detect_fatigue(df, BEST_HT, BEST_FT)
            
            ht = feats['mean_hold_time']
            ft = feats['mean_flight_time']
            status = "疲労傾向 😫" if is_fatigued else "元気 😃"
            print(f"[{time.strftime('%H:%M:%S')}] HT:{ht:.3f} FT:{ft:.3f} -> {status}")

            # 3. 介入判定
            should_intervene, reason = jitai.decide_intervention(is_fatigued)
            
            if should_intervene:
                print(f"🚀 介入実行: {reason}")
                # 4. 通知（5段階評価UIを表示）
                show_interactive_popup("少し指の動きが硬いです。", feats)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

