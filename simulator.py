import pandas as pd
import numpy as np
import random
import os

def generate_session(user_id, condition, duration_sec=60):
    """
    仮想ユーザーのキーストロークデータを生成する
    condition: 'alert' (元気) or 'fatigued' (疲労)
    """
    # 基本設定（秒単位）
    # 疲労時はホールド時間(HT)とフライト時間(FT)が伸び、バラつき(std)も増えると仮定
    if condition == 'alert':
        base_ht, std_ht = 0.10, 0.01
        base_ft, std_ft = 0.15, 0.02
    else: # fatigued
        base_ht, std_ht = 0.14, 0.03 # 少し長くなり、不安定になる
        base_ft, std_ft = 0.25, 0.05 # 反応が鈍くなる

    data = []
    current_time = 1000.0 # 開始時刻
    keys = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']

    while current_time < 1000.0 + duration_sec:
        # ランダムにキーを選ぶ
        key = random.choice(keys)
        
        # タイミングを生成（正規分布）
        ht = abs(np.random.normal(base_ht, std_ht))
        ft = abs(np.random.normal(base_ft, std_ft))

        # PRESS
        press_time = current_time + ft
        data.append([press_time, 'PRESS', key])
        
        # RELEASE
        release_time = press_time + ht
        data.append([release_time, 'RELEASE', key])
        
        current_time = release_time

    df = pd.DataFrame(data, columns=['timestamp', 'event_type', 'key_code'])
    return df

def create_dataset(num_users=20):
    """学習用データセットを作成"""
    os.makedirs("data/simulated", exist_ok=True)
    
    summary = []
    
    print(f"🤖 {num_users}人分の仮想データを作成中...")
    for i in range(num_users):
        # 半分は元気、半分は疲労
        condition = 'alert' if i % 2 == 0 else 'fatigued'
        df = generate_session(i, condition)
        
        filename = f"data/simulated/user_{i}_{condition}.csv"
        df.to_csv(filename, index=False)
        
        summary.append({'filename': filename, 'condition': condition})
        
    print("✅ 作成完了")
    return pd.DataFrame(summary)

if __name__ == "__main__":
    create_dataset(100) # 100ファイル生成

