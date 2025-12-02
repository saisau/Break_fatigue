"""
機械学習による疲労検知モデル
scikit-learn を使用した FatigueClassifier クラス
"""

import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class FatigueClassifier:
    """
    キーストロークの特徴量から疲労状態を予測する分類器
    
    アルゴリズム: ロジスティック回帰
    - 高速な推論（<10ms）
    - 確率値の出力が可能
    - シンプルで解釈しやすい
    """
    
    def __init__(self):
        self.model_ = None
        self.scaler_ = StandardScaler()
        
    def fit(self, X, y):
        """
        モデルを学習する
        
        Parameters
        ----------
        X : DataFrame or array-like
            特徴量（mean_hold_time, mean_flight_time など）
        y : array-like
            ラベル（0: 元気, 1: 疲労）
        """
        # 特徴量をスケーリング
        X_scaled = self.scaler_.fit_transform(X)
        
        # ロジスティック回帰モデルを学習
        self.model_ = LogisticRegression(
            C=1.0,
            max_iter=1000,
            random_state=42
        )
        self.model_.fit(X_scaled, y)
        
        return self
    
    def predict(self, X):
        """
        疲労状態を予測する
        
        Parameters
        ----------
        X : DataFrame or array-like
            特徴量
            
        Returns
        -------
        array
            予測ラベル（0: 元気, 1: 疲労）
        """
        X_scaled = self.scaler_.transform(X)
        return self.model_.predict(X_scaled)
    
    def predict_proba(self, X):
        """
        疲労状態の確率を予測する
        
        Parameters
        ----------
        X : DataFrame or array-like
            特徴量
            
        Returns
        -------
        array
            確率値 [[P(元気), P(疲労)], ...]
        """
        X_scaled = self.scaler_.transform(X)
        return self.model_.predict_proba(X_scaled)
    
    def score(self, X, y):
        """
        正解率を計算する
        
        Parameters
        ----------
        X : DataFrame or array-like
            特徴量
        y : array-like
            正解ラベル
            
        Returns
        -------
        float
            正解率（0.0 〜 1.0）
        """
        X_scaled = self.scaler_.transform(X)
        return self.model_.score(X_scaled, y)
    
    def save(self, filepath):
        """
        モデルをファイルに保存する
        
        Parameters
        ----------
        filepath : str
            保存先のパス
        """
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model_,
                'scaler': self.scaler_
            }, f)
    
    @classmethod
    def load(cls, filepath):
        """
        ファイルからモデルを読み込む
        
        Parameters
        ----------
        filepath : str
            読み込むファイルのパス
            
        Returns
        -------
        FatigueClassifier
            読み込んだモデル
        """
        instance = cls()
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            instance.model_ = data['model']
            instance.scaler_ = data['scaler']
        return instance
