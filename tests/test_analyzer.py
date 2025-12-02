import pandas as pd
import pytest
import sys
import os

# 親ディレクトリのモジュールを読み込めるようにする
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# まだ存在しないが、これからAIに作らせるモジュール
from analyzer import calculate_features

def test_calculate_features():
    # ダミーデータを読み込み
    df = pd.read_csv('tests/dummy_log.csv')
    
    # 特徴量計算を実行
    results = calculate_features(df)
    
    # --- 検証 (Assert) ---
    
    # 1. Hold Time (キーを押し続けている時間) の平均
    # a: 0.1s, b: 0.15s -> 平均 0.125s
    assert results['mean_hold_time'] == pytest.approx(0.125)
    
    # 2. Flight Time (前のキーを離してから次を押すまでの時間) の平均
    # a(release) 1000.1 -> b(press) 1000.2 = 0.1s
    assert results['mean_flight_time'] == pytest.approx(0.1)

    print("✅ 全てのテストを通過しました！")