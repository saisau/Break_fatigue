import time
import pandas as pd
import os
from analyzer import calculate_features
from jitai import JITAIEngine
from notifier import show_interactive_popup

# MLモデルを使用するかどうか
USE_ML_MODEL = True

LOG_FILE = "keystroke_log.csv"
MODEL_FILE = "fatigue_model.pkl"
CHECK_INTERVAL = 10  # 10秒ごとにチェック

# 閾値ベースのパラメータ（MLモデルが使えない場合のフォールバック）
BEST_HT = 0.175
BEST_FT = 0.270


def load_ml_model():
    """MLモデルを読み込む（なければNone）"""
    if not os.path.exists(MODEL_FILE):
        return None
    try:
        from ml_model import FatigueClassifier
        return FatigueClassifier.load(MODEL_FILE)
    except Exception as e:
        print(f"⚠️ モデル読み込みエラー: {e}")
        return None


def get_recent_data(filepath, seconds=60):
    """直近n秒のデータだけをCSVから読み込む"""
    if not os.path.exists(filepath):
        return pd.DataFrame()
        
    try:
        df = pd.read_csv(filepath)
        if df.empty:
            return df
        
        current_timestamp = time.time()
        recent_df = df[df['timestamp'] > (current_timestamp - seconds)]
        return recent_df
    except Exception as e:
        print(f"Read Error: {e}")
        return pd.DataFrame()


def predict_fatigue_ml(model, feats):
    """MLモデルで疲労を予測"""
    X = pd.DataFrame([{
        'mean_hold_time': feats['mean_hold_time'],
        'mean_flight_time': feats['mean_flight_time']
    }])
    
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    
    return prediction == 1, proba[1]  # is_fatigued, confidence


def predict_fatigue_threshold(feats, ht_thresh, ft_thresh):
    """閾値ベースで疲労を予測"""
    is_fatigued = (
        feats['mean_hold_time'] > ht_thresh or 
        feats['mean_flight_time'] > ft_thresh
    )
    return is_fatigued, None


def main():
    print("👀 疲労監視モニターを起動しました...")
    
    # MLモデルを読み込み
    ml_model = None
    if USE_ML_MODEL:
        ml_model = load_ml_model()
        if ml_model:
            print("🧠 MLモデルを使用します")
        else:
            print(f"⚠️ MLモデルが見つかりません。閾値ベースで動作します。")
            print(f"   モデルを作成するには: python train_model.py")
    
    if not ml_model:
        print(f"   パラメータ: HT>{BEST_HT}, FT>{BEST_FT}")
    
    jitai = JITAIEngine()
    jitai.min_interval_sec = 60  # 1分間隔
    
    while True:
        # 1. データ取得
        df = get_recent_data(LOG_FILE, seconds=60)
        
        if len(df) < 10:
            print(f"⏳ データ収集中... ({len(df)} keys / min)")
        else:
            # 2. 特徴量計算
            feats = calculate_features(df)
            ht = feats['mean_hold_time']
            ft = feats['mean_flight_time']
            
            # 3. 疲労判定
            if ml_model:
                is_fatigued, confidence = predict_fatigue_ml(ml_model, feats)
                status = f"疲労 {confidence:.0%} 😫" if is_fatigued else f"元気 {1-confidence:.0%} 😃"
            else:
                is_fatigued, _ = predict_fatigue_threshold(feats, BEST_HT, BEST_FT)
                status = "疲労傾向 😫" if is_fatigued else "元気 😃"
            
            print(f"[{time.strftime('%H:%M:%S')}] HT:{ht:.3f} FT:{ft:.3f} -> {status}")

            # 4. 介入判定
            should_intervene, reason = jitai.decide_intervention(is_fatigued)
            
            if should_intervene:
                print(f"🚀 介入実行: {reason}")
                # 5. 通知（5段階評価UIを表示）
                show_interactive_popup("少し指の動きが硬いです。", feats)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
