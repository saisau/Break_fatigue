"""
精神的疲労推定のための特徴量計算モジュール
"""
import pandas as pd


def calculate_features(df: pd.DataFrame) -> dict:
    """
    キーストロークログから疲労推定用の特徴量を計算する。
    
    Parameters
    ----------
    df : pd.DataFrame
        timestamp, event_type, key_code カラムを持つDataFrame
        
    Returns
    -------
    dict
        mean_hold_time: キーを押し続けている時間の平均
        mean_flight_time: 前のキーを離してから次のキーを押すまでの時間の平均
    """
    hold_times = []
    
    # PRESSイベントとRELEASEイベントを分離
    press_events = df[df['event_type'] == 'PRESS'].reset_index(drop=True)
    release_events = df[df['event_type'] == 'RELEASE'].reset_index(drop=True)
    
    # Hold Time計算: 同じkey_codeのPRESSとRELEASEをマッチング
    for _, press_row in press_events.iterrows():
        key = press_row['key_code']
        press_time = press_row['timestamp']
        
        # 対応するRELEASEを探す（同じkey_codeで、PRESSより後のもの）
        matching_release = release_events[
            (release_events['key_code'] == key) & 
            (release_events['timestamp'] > press_time)
        ]
        
        if not matching_release.empty:
            release_time = matching_release.iloc[0]['timestamp']
            hold_times.append(release_time - press_time)
    
    # Flight Time計算: RELEASEから次のPRESSまでの時間
    flight_times = []
    
    # 時系列順にイベントを処理
    for i in range(len(df) - 1):
        current = df.iloc[i]
        next_event = df.iloc[i + 1]
        
        # 現在がRELEASEで、次がPRESSの場合
        if current['event_type'] == 'RELEASE' and next_event['event_type'] == 'PRESS':
            flight_time = next_event['timestamp'] - current['timestamp']
            flight_times.append(flight_time)
    
    # 平均を計算
    mean_hold_time = sum(hold_times) / len(hold_times) if hold_times else 0.0
    mean_flight_time = sum(flight_times) / len(flight_times) if flight_times else 0.0
    
    return {
        'mean_hold_time': mean_hold_time,
        'mean_flight_time': mean_flight_time,
        'hold_time_count': len(hold_times)
    }


def detect_fatigue(df, threshold_ht, threshold_ft):
    """
    与えられた閾値に基づいて、疲労状態かどうかを判定する
    True: 疲労 (Fatigued)
    False: 元気 (Alert)
    """
    features = calculate_features(df)
    
    # ロジック: HTかFTのどちらかが閾値を超えていたら「疲労」とみなす（AND/ORは実験対象）
    is_fatigued = (
        features['mean_hold_time'] > threshold_ht or 
        features['mean_flight_time'] > threshold_ft
    )
    
    return is_fatigued, features
