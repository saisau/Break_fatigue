"""
機械学習疲労検知モデルのテスト（仕様書）

【ゴール】
- feedback_log.csv を学習データとして使用
- テストデータに対する正解率（Accuracy）が 90% 以上
- 推論速度が 0.01秒 以内

【制約】
- scikit-learn を使用すること
- モデルは ml_model.py の FatigueClassifier クラスとして実装
"""

import pytest
import pandas as pd
import time
import sys
import os

# 親ディレクトリのモジュールを読み込めるようにする
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# これから作るモジュール
from ml_model import FatigueClassifier


class TestFatigueClassifier:
    """疲労検知MLモデルのテストスイート"""
    
    @pytest.fixture
    def sample_data(self):
        """テスト用のサンプルデータを生成"""
        # 実際のfeedback_log.csvが少ない場合に備えて、シミュレーションデータも使う
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
    
    @pytest.fixture
    def trained_model(self, sample_data):
        """学習済みモデルを返す"""
        model = FatigueClassifier()
        X = sample_data[['mean_hold_time', 'mean_flight_time']]
        y = (sample_data['fatigue_score'] >= 4).astype(int)  # 4以上を疲労(1)とする
        model.fit(X, y)
        return model
    
    # ========================================
    # 1. モデルの基本機能テスト
    # ========================================
    
    def test_model_can_be_instantiated(self):
        """モデルがインスタンス化できること"""
        model = FatigueClassifier()
        assert model is not None
    
    def test_model_can_fit(self, sample_data):
        """モデルが学習できること"""
        model = FatigueClassifier()
        X = sample_data[['mean_hold_time', 'mean_flight_time']]
        y = (sample_data['fatigue_score'] >= 4).astype(int)
        
        # fit() がエラーなく完了すること
        model.fit(X, y)
        assert hasattr(model, 'model_')  # 内部モデルが作成されていること
    
    def test_model_can_predict(self, trained_model):
        """モデルが予測できること"""
        X_test = pd.DataFrame({
            'mean_hold_time': [0.10, 0.20],
            'mean_flight_time': [0.15, 0.30]
        })
        
        predictions = trained_model.predict(X_test)
        
        assert len(predictions) == 2
        assert all(p in [0, 1] for p in predictions)  # 0 or 1 のみ
    
    # ========================================
    # 2. 精度要件テスト（Accuracy >= 90%）
    # ========================================
    
    def test_accuracy_above_90_percent(self, sample_data):
        """正解率が90%以上であること"""
        from sklearn.model_selection import train_test_split
        
        X = sample_data[['mean_hold_time', 'mean_flight_time']]
        y = (sample_data['fatigue_score'] >= 4).astype(int)
        
        # 学習・テスト分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        model = FatigueClassifier()
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        
        print(f"\n📊 モデル精度: {accuracy:.2%}")
        assert accuracy >= 0.90, f"精度が90%未満です: {accuracy:.2%}"
    
    # ========================================
    # 3. 推論速度テスト（< 0.01秒）
    # ========================================
    
    def test_inference_speed_under_10ms(self, trained_model):
        """推論速度が0.01秒（10ms）以内であること"""
        X_test = pd.DataFrame({
            'mean_hold_time': [0.15],
            'mean_flight_time': [0.25]
        })
        
        # 推論時間を計測
        start_time = time.perf_counter()
        trained_model.predict(X_test)
        elapsed_time = time.perf_counter() - start_time
        
        print(f"\n⚡ 推論速度: {elapsed_time*1000:.3f} ms")
        assert elapsed_time < 0.01, f"推論速度が遅すぎます: {elapsed_time:.4f}秒"
    
    # ========================================
    # 4. 実用性テスト
    # ========================================
    
    def test_predict_proba_returns_confidence(self, trained_model):
        """確率値（信頼度）を返せること"""
        X_test = pd.DataFrame({
            'mean_hold_time': [0.15],
            'mean_flight_time': [0.25]
        })
        
        probabilities = trained_model.predict_proba(X_test)
        
        assert probabilities.shape == (1, 2)  # [P(元気), P(疲労)]
        assert 0 <= probabilities[0][0] <= 1
        assert 0 <= probabilities[0][1] <= 1
        assert abs(sum(probabilities[0]) - 1.0) < 0.001  # 合計が1
    
    def test_model_can_save_and_load(self, trained_model, tmp_path):
        """モデルを保存・読み込みできること"""
        # 保存
        model_path = tmp_path / "fatigue_model.pkl"
        trained_model.save(str(model_path))
        
        assert model_path.exists()
        
        # 読み込み
        loaded_model = FatigueClassifier.load(str(model_path))
        
        # 同じ予測ができること
        X_test = pd.DataFrame({
            'mean_hold_time': [0.15],
            'mean_flight_time': [0.25]
        })
        
        original_pred = trained_model.predict(X_test)
        loaded_pred = loaded_model.predict(X_test)
        
        assert list(original_pred) == list(loaded_pred)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

