"""
feedback_log.csv からモデルを学習して保存するスクリプト
"""

import pandas as pd
import os
from ml_model import FatigueClassifier

FEEDBACK_FILE = "feedback_log.csv"
MODEL_FILE = "fatigue_model.pkl"
FATIGUE_THRESHOLD = 4  # スコア4以上を「疲労」とみなす


def train_and_save():
    print("🧠 モデル学習スクリプト")
    print("=" * 40)
    
    # データ読み込み
    if not os.path.exists(FEEDBACK_FILE):
        print(f"❌ {FEEDBACK_FILE} が見つかりません。")
        print("   システムを使ってデータを収集してください。")
        return False
    
    df = pd.read_csv(FEEDBACK_FILE)
    print(f"📊 データ件数: {len(df)} 件")
    
    if len(df) < 5:
        print("⚠️ データが少なすぎます（最低5件必要）")
        return False
    
    # 特徴量とラベルを準備
    X = df[['mean_hold_time', 'mean_flight_time']]
    y = (df['fatigue_score'] >= FATIGUE_THRESHOLD).astype(int)
    
    print(f"   疲労サンプル: {y.sum()} 件")
    print(f"   元気サンプル: {len(y) - y.sum()} 件")
    
    # モデル学習
    model = FatigueClassifier()
    model.fit(X, y)
    
    # 学習データでの精度を確認
    accuracy = model.score(X, y)
    print(f"\n📈 学習データでの精度: {accuracy:.2%}")
    
    # モデルを保存
    model.save(MODEL_FILE)
    print(f"\n✅ モデルを保存しました: {MODEL_FILE}")
    
    return True


if __name__ == "__main__":
    train_and_save()

