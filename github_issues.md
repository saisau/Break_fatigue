# GitHub Issues for Background Agents

以下の5つの Issue を GitHub で作成してください。
https://github.com/saisau/Break_fatigue/issues/new

---

## Issue 1: [Agent A] ロジスティック回帰で ml_model.py を実装

```
@cursor

`ml_model.py` を新規作成し、`tests/test_ml_model.py` のテストが全て通るように実装してください。

**ブランチ**: `feature/ml-fatigue-model`
**アルゴリズム**: ロジスティック回帰 (LogisticRegression)
**ライブラリ**: scikit-learn

**要件**:
- FatigueClassifier クラスを実装
- fit(), predict(), predict_proba(), score(), save(), load() メソッド
- 精度90%以上、推論速度10ms以内

テスト実行: `python -m pytest tests/test_ml_model.py -v`
```

---

## Issue 2: [Agent B] SVM (RBF) で ml_model.py を実装

```
@cursor

`ml_model.py` を新規作成し、`tests/test_ml_model.py` のテストが全て通るように実装してください。

**ブランチ**: `feature/ml-fatigue-model`
**アルゴリズム**: SVM with RBF kernel (SVC)
**ライブラリ**: scikit-learn

**要件**:
- FatigueClassifier クラスを実装
- fit(), predict(), predict_proba(), score(), save(), load() メソッド
- 精度90%以上、推論速度10ms以内
- SVCには probability=True を設定すること

テスト実行: `python -m pytest tests/test_ml_model.py -v`
```

---

## Issue 3: [Agent C] ランダムフォレストで ml_model.py を実装

```
@cursor

`ml_model.py` を新規作成し、`tests/test_ml_model.py` のテストが全て通るように実装してください。

**ブランチ**: `feature/ml-fatigue-model`
**アルゴリズム**: ランダムフォレスト (RandomForestClassifier)
**ライブラリ**: scikit-learn

**要件**:
- FatigueClassifier クラスを実装
- fit(), predict(), predict_proba(), score(), save(), load() メソッド
- 精度90%以上、推論速度10ms以内
- n_estimators=100 程度で

テスト実行: `python -m pytest tests/test_ml_model.py -v`
```

---

## Issue 4: [Agent D] 勾配ブースティングで ml_model.py を実装

```
@cursor

`ml_model.py` を新規作成し、`tests/test_ml_model.py` のテストが全て通るように実装してください。

**ブランチ**: `feature/ml-fatigue-model`
**アルゴリズム**: 勾配ブースティング (GradientBoostingClassifier)
**ライブラリ**: scikit-learn

**要件**:
- FatigueClassifier クラスを実装
- fit(), predict(), predict_proba(), score(), save(), load() メソッド
- 精度90%以上、推論速度10ms以内

テスト実行: `python -m pytest tests/test_ml_model.py -v`
```

---

## Issue 5: [Agent E] k-近傍法で ml_model.py を実装

```
@cursor

`ml_model.py` を新規作成し、`tests/test_ml_model.py` のテストが全て通るように実装してください。

**ブランチ**: `feature/ml-fatigue-model`
**アルゴリズム**: k-近傍法 (KNeighborsClassifier)
**ライブラリ**: scikit-learn

**要件**:
- FatigueClassifier クラスを実装
- fit(), predict(), predict_proba(), score(), save(), load() メソッド
- 精度90%以上、推論速度10ms以内
- n_neighbors=5 程度で

テスト実行: `python -m pytest tests/test_ml_model.py -v`
```

---

## 手順

1. https://github.com/saisau/Break_fatigue/issues/new にアクセス
2. 上記の各 Issue のタイトルと本文（```で囲まれた部分）をコピー&ペースト
3. 「Submit new issue」をクリック
4. 5つ全て作成後、Background Agents が自動的に実装を開始します

