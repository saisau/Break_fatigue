import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

LOG_FILE = "feedback_log.csv"

def analyze_data():
    if not os.path.exists(LOG_FILE):
        print("❌ データファイルが見つかりません。")
        return

    # データを読み込む
    df = pd.read_csv(LOG_FILE)
    print(f"📊 データ件数: {len(df)} 件")
    
    # データが少なすぎる場合の警告
    if len(df) < 5:
        print("⚠️ データが少なすぎます。グラフが正しく描画されない可能性があります。")

    # グラフの設定
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 1. Hold Time (キーを押している時間) vs 疲労度
    sns.regplot(x="mean_hold_time", y="fatigue_score", data=df, ax=axes[0],
                scatter_kws={'s':100, 'alpha':0.6, 'color':'blue'}, line_kws={'color':'red'})
    axes[0].set_title("Hold Time vs. Fatigue Score")
    axes[0].set_xlabel("Mean Hold Time (sec)")
    axes[0].set_ylabel("Fatigue Score (1:Active - 5:Exhausted)")

    # 2. Flight Time (キー移動時間) vs 疲労度
    sns.regplot(x="mean_flight_time", y="fatigue_score", data=df, ax=axes[1],
                scatter_kws={'s':100, 'alpha':0.6, 'color':'green'}, line_kws={'color':'red'})
    axes[1].set_title("Flight Time vs. Fatigue Score")
    axes[1].set_xlabel("Mean Flight Time (sec)")
    axes[1].set_ylabel("Fatigue Score")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyze_data()

