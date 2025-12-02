"""
5つのアルゴリズムを比較するスクリプト
"""

import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


def get_sample_data():
    """テスト用のサンプルデータを生成"""
    data = {
        'mean_hold_time': [0.10, 0.11, 0.12, 0.09, 0.08,  # 元気
                           0.18, 0.20, 0.22, 0.19, 0.21,  # 疲労
                           0.10, 0.12, 0.11, 0.09, 0.10,  # 元気
                           0.17, 0.19, 0.20, 0.18, 0.22], # 疲労
        'mean_flight_time': [0.15, 0.14, 0.16, 0.13, 0.12,  # 元気
                             0.30, 0.32, 0.35, 0.28, 0.33,  # 疲労
                             0.14, 0.15, 0.13, 0.12, 0.14,  # 元気
                             0.29, 0.31, 0.34, 0.30, 0.32], # 疲労
        'fatigue_score': [1, 1, 2, 1, 1,  # 元気 (1-3)
                          4, 5, 5, 4, 5,  # 疲労 (4-5)
                          1, 2, 1, 1, 2,  # 元気
                          4, 4, 5, 4, 5]  # 疲労
    }
    return pd.DataFrame(data)


def compare_algorithms():
    print("=" * 60)
    print("5つのアルゴリズム比較")
    print("=" * 60)
    
    df = get_sample_data()
    X = df[['mean_hold_time', 'mean_flight_time']]
    y = (df['fatigue_score'] >= 4).astype(int)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    algorithms = {
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'SVM (RBF)': SVC(kernel='rbf', probability=True, random_state=42),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'GradientBoosting': GradientBoostingClassifier(random_state=42),
        'k-NN': KNeighborsClassifier(n_neighbors=3)
    }
    
    results = []
    
    for name, model in algorithms.items():
        # 学習
        model.fit(X_train_scaled, y_train)
        
        # 精度
        accuracy = model.score(X_test_scaled, y_test)
        
        # 推論速度
        X_single = X_test_scaled[:1]
        start = time.perf_counter()
        for _ in range(100):
            model.predict(X_single)
        elapsed = (time.perf_counter() - start) / 100 * 1000  # ms
        
        results.append({
            'Algorithm': name,
            'Accuracy': accuracy,
            'Inference (ms)': elapsed
        })
        
        status = "✅" if accuracy >= 0.90 and elapsed < 10 else "❌"
        print(f"{status} {name:20} | 精度: {accuracy:.2%} | 速度: {elapsed:.3f} ms")
    
    print("=" * 60)
    
    # ベストを選択
    passed = [r for r in results if r['Accuracy'] >= 0.90 and r['Inference (ms)'] < 10]
    if passed:
        best = max(passed, key=lambda x: x['Accuracy'])
        print(f"\n🏆 ベスト: {best['Algorithm']}")
        print(f"   精度: {best['Accuracy']:.2%}")
        print(f"   速度: {best['Inference (ms)']:.3f} ms")
    
    return results


if __name__ == "__main__":
    compare_algorithms()

