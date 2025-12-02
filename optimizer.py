import pandas as pd
import numpy as np
import multiprocessing
from itertools import product

LOG_FILE = "feedback_log.csv"

# 疲労とみなすスコアの境界線（4以上を「疲労」とする）
FATIGUE_THRESHOLD_SCORE = 4

def evaluate_parameters(args):
    """
    1つのパラメータセット(ht_threshold, ft_threshold)を評価する関数
    並列処理のために独立した関数として定義
    """
    ht_thresh, ft_thresh, data_records = args
    
    correct_count = 0
    total_count = len(data_records)
    
    for record in data_records:
        # 正解ラベル: スコアが4以上なら True (疲れてる)
        actual_is_fatigued = record['fatigue_score'] >= FATIGUE_THRESHOLD_SCORE
        
        # モデルの予測: 特徴量が閾値を超えていれば True
        # (簡単のため OR 条件で判定してみる)
        predicted_is_fatigued = (
            record['mean_hold_time'] > ht_thresh or 
            record['mean_flight_time'] > ft_thresh
        )
        
        if actual_is_fatigued == predicted_is_fatigued:
            correct_count += 1
            
    accuracy = correct_count / total_count if total_count > 0 else 0
    return (accuracy, ht_thresh, ft_thresh)

def run_optimization():
    print("🚀 パラメータ最適化を開始します（ローカル並列実行）...")
    
    # データを読み込み、辞書のリストに変換（高速化のため）
    df = pd.read_csv(LOG_FILE)
    records = df.to_dict('records')
    
    print(f"📚 学習データ数: {len(records)} 件")
    
    # 探索範囲の設定（グリッドサーチ）
    # あなたのグラフを見て、範囲を調整してください
    ht_range = np.arange(0.05, 0.20, 0.005) # 0.05秒〜0.20秒 を 0.005刻みで
    ft_range = np.arange(0.10, 0.30, 0.010) # 0.10秒〜0.30秒 を 0.010刻みで
    
    # 全組み合わせを作成
    param_combinations = list(product(ht_range, ft_range))
    total_params = len(param_combinations)
    
    print(f"🧪 テストするパラメータの組み合わせ: {total_params} 通り")
    print(f"💻 CPUコア数: {multiprocessing.cpu_count()} をフル稼働させます")

    # 並列処理用の引数リスト作成
    tasks = [(ht, ft, records) for ht, ft in param_combinations]
    
    # 並列実行 (Map)
    with multiprocessing.Pool() as pool:
        results = pool.map(evaluate_parameters, tasks)
        
    # 結果の中からベストを探す (Reduce)
    best_result = max(results, key=lambda x: x[0])
    best_accuracy, best_ht, best_ft = best_result
    
    print("\n" + "="*40)
    print("🏆 最適化完了！最強のパラメータが見つかりました")
    print("="*40)
    print(f"✅ 最高正解率 (Accuracy): {best_accuracy:.2%}")
    print(f"🔹 最適 Hold Time 閾値 : > {best_ht:.3f} 秒")
    print(f"🔹 最適 Flight Time 閾値: > {best_ft:.3f} 秒")
    print("="*40)
    print("👉 monitor.py の定数をこれに書き換えてください！")

if __name__ == "__main__":
    run_optimization()
