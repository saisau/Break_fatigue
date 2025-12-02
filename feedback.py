import csv
import time
import os

FEEDBACK_FILE = "feedback_log.csv"

def log_feedback(score, features):
    """
    ユーザーの5段階評価と、その時の特徴量を保存する
    score: 1 (全く疲れてない) 〜 5 (非常に疲れている)
    features: その時の特徴量
    """
    file_exists = os.path.exists(FEEDBACK_FILE)
    
    with open(FEEDBACK_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # ヘッダー（初回のみ）
        if not file_exists:
            writer.writerow([
                "timestamp", "fatigue_score", 
                "mean_hold_time", "mean_flight_time",
                "is_fatigued_pred"
            ])
            
        writer.writerow([
            time.time(),
            score,  # ここに1~5の数字が入る
            features.get('mean_hold_time', 0),
            features.get('mean_flight_time', 0),
            True
        ])
    
    print(f"📝 疲労度記録: レベル {score}")

if __name__ == "__main__":
    # テスト
    log_feedback(3, {'mean_hold_time': 0.1})

