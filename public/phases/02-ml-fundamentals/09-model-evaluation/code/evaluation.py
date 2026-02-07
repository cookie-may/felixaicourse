#!/usr/bin/env python3
"""
Felix Learning Platform - Model Evaluation Module
Comprehensive metrics and validation strategies for ML models
Author: Felix Learning
License: MIT

This module provides tools for evaluating machine learning models
including classification metrics, regression metrics, and cross-validation.
"""

import random
import math
from typing import List, Tuple, Callable, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class SplitStrategy(Enum):
    """Data splitting strategies"""
    STANDARD = "standard"
    STRATIFIED = "stratified"
    K_FOLD = "k_fold"
    STRATIFIED_K_FOLD = "stratified_k_fold"


@dataclass
class EvaluationResult:
    """Container for evaluation metrics"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    metrics: Dict[str, float]


class DataSplitter:
    """Handles train/validation/test splitting"""

    @staticmethod
    def holdout_split(
        features: List[Any],
        targets: List[Any],
        train_ratio: float = 0.6,
        val_ratio: float = 0.2,
        seed: int = 42
    ) -> Tuple[List[Any], List[Any], List[Any], List[Any], List[Any], List[Any]]:
        """Split data into train, validation, and test sets"""
        random.seed(seed)
        n = len(features)
        indices = list(range(n))
        random.shuffle(indices)

        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        train_idx = indices[:train_end]
        val_idx = indices[train_end:val_end]
        test_idx = indices[val_end:]

        X_train = [features[i] for i in train_idx]
        y_train = [targets[i] for i in train_idx]
        X_val = [features[i] for i in val_idx]
        y_val = [targets[i] for i in val_idx]
        X_test = [features[i] for i in test_idx]
        y_test = [targets[i] for i in test_idx]

        return X_train, y_train, X_val, y_val, X_test, y_test

    @staticmethod
    def k_fold_split(n: int, k: int = 5, seed: int = 42) -> List[Tuple[List[int], List[int]]]:
        """Create k folds for cross-validation"""
        random.seed(seed)
        indices = list(range(n))
        random.shuffle(indices)

        fold_size = n // k
        folds = []

        for i in range(k):
            start = i * fold_size
            end = start + fold_size if i < k - 1 else n
            val_idx = indices[start:end]
            train_idx = indices[:start] + indices[end:]
            folds.append((train_idx, val_idx))

        return folds

    @staticmethod
    def stratified_k_fold_split(
        targets: List[int],
        k: int = 5,
        seed: int = 42
    ) -> List[Tuple[List[int], List[int]]]:
        """Create stratified k folds maintaining class distribution"""
        random.seed(seed)

        class_indices = {}
        for i, label in enumerate(targets):
            class_indices.setdefault(label, []).append(i)

        for label in class_indices:
            random.shuffle(class_indices[label])

        folds = [{"train": [], "val": []} for _ in range(k)]

        for label, indices in class_indices.items():
            fold_size = len(indices) // k
            for i in range(k):
                start = i * fold_size
                end = start + fold_size if i < k - 1 else len(indices)
                val_part = indices[start:end]
                train_part = indices[:start] + indices[end:]
                folds[i]["val"].extend(val_part)
                folds[i]["train"].extend(train_part)

        return [(f["train"], f["val"]) for f in folds]


class BinaryClassificationMetrics:
    """Compute binary classification metrics from predictions"""

    def __init__(self, true_labels: List[int], predicted_labels: List[int]):
        self.true_positives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 1)
        self.true_negatives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 0)
        self.false_positives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 1)
        self.false_negatives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 0)

    def compute_accuracy(self) -> float:
        """Overall accuracy"""
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        return (self.true_positives + self.true_negatives) / total if total > 0 else 0.0

    def compute_precision(self) -> float:
        """Positive predictive value"""
        denom = self.true_positives + self.false_positives
        return self.true_positives / denom if denom > 0 else 0.0

    def compute_recall(self) -> float:
        """True positive rate"""
        denom = self.true_positives + self.false_negatives
        return self.true_positives / denom if denom > 0 else 0.0

    def compute_f1(self) -> float:
        """Harmonic mean of precision and recall"""
        p = self.compute_precision()
        r = self.compute_recall()
        return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


class RegressionMetrics:
    """Compute regression evaluation metrics"""

    @staticmethod
    def mean_squared_error(true_values: List[float], predicted: List[float]) -> float:
        """MSE loss"""
        n = len(true_values)
        return sum((yt - yp) ** 2 for yt, yp in zip(true_values, predicted)) / n

    @staticmethod
    def root_mse(true_values: List[float], predicted: List[float]) -> float:
        """RMSE metric"""
        return math.sqrt(RegressionMetrics.mean_squared_error(true_values, predicted))

    @staticmethod
    def mean_absolute_error(true_values: List[float], predicted: List[float]) -> float:
        """MAE metric"""
        n = len(true_values)
        return sum(abs(yt - yp) for yt, yp in zip(true_values, predicted)) / n

    @staticmethod
    def r_squared(true_values: List[float], predicted: List[float]) -> float:
        """Coefficient of determination"""
        mean_y = sum(true_values) / len(true_values)
        ss_residual = sum((yt - yp) ** 2 for yt, yp in zip(true_values, predicted))
        ss_total = sum((yt - mean_y) ** 2 for yt in true_values)

        if ss_total == 0:
            return 0.0
        return 1.0 - ss_residual / ss_total


class ROCCurveCalculator:
    """Compute ROC curve and AUC-ROC metric"""

    @staticmethod
    def compute_curve(
        true_labels: List[int],
        prediction_scores: List[float]
    ) -> Tuple[List[float], List[float], List[float]]:
        """Calculate ROC curve points"""
        thresholds = sorted(set(prediction_scores), reverse=True)
        tpr_values = []
        fpr_values = []

        total_positives = sum(true_labels)
        total_negatives = len(true_labels) - total_positives

        for threshold in thresholds:
            predictions = [1 if s >= threshold else 0 for s in prediction_scores]
            tp = sum(1 for yt, yp in zip(true_labels, predictions) if yt == 1 and yp == 1)
            fp = sum(1 for yt, yp in zip(true_labels, predictions) if yt == 0 and yp == 1)

            tpr = tp / total_positives if total_positives > 0 else 0.0
            fpr = fp / total_negatives if total_negatives > 0 else 0.0

            tpr_values.append(tpr)
            fpr_values.append(fpr)

        return fpr_values, tpr_values, thresholds

    @staticmethod
    def compute_auc(true_labels: List[int], prediction_scores: List[float]) -> float:
        """Calculate area under ROC curve"""
        fpr_list, tpr_list, _ = ROCCurveCalculator.compute_curve(true_labels, prediction_scores)

        pairs = sorted(zip(fpr_list, tpr_list))
        fpr_sorted = [p[0] for p in pairs]
        tpr_sorted = [p[1] for p in pairs]

        area = 0.0
        for i in range(1, len(fpr_sorted)):
            width = fpr_sorted[i] - fpr_sorted[i - 1]
            height = (tpr_sorted[i] + tpr_sorted[i - 1]) / 2
            area += width * height

        return area


class CrossValidator:
    """Perform cross-validation for model evaluation"""

    def __init__(
        self,
        model_factory: Callable[[], Any],
        metric_function: Callable[[List[int], List[int]], float],
        k_folds: int = 5,
        stratified: bool = False
    ):
        self.model_factory = model_factory
        self.metric_fn = metric_function
        self.k = k_folds
        self.stratified = stratified

    def validate(
        self,
        features: List[Any],
        targets: List[int]
    ) -> Tuple[List[float], float, float]:
        """Run cross-validation and return scores"""
        n = len(features)

        if self.stratified:
            folds = DataSplitter.stratified_k_fold_split(targets, self.k)
        else:
            folds = DataSplitter.k_fold_split(n, self.k)

        scores = []
        for fold_idx, (train_idx, val_idx) in enumerate(folds):
            X_train = [features[i] for i in train_idx]
            y_train = [targets[i] for i in train_idx]
            X_val = [features[i] for i in val_idx]
            y_val = [targets[i] for i in val_idx]

            model = self.model_factory()
            model.fit(X_train, y_train)
            predictions = [model.predict(x) for x in X_val]

            score = self.metric_fn(y_val, predictions)
            scores.append(score)

        mean_score = sum(scores) / len(scores)
        variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
        std_score = math.sqrt(variance)

        return scores, mean_score, std_score


class LearningCurveAnalyzer:
    """Analyze learning curves for model behavior"""

    @staticmethod
    def generate_curve(
        features: List[Any],
        targets: List[int],
        model_factory: Callable[[], Any],
        metric_fn: Callable[[List[int], List[int]], float],
        train_ratios: Optional[List[float]] = None,
        val_ratio: float = 0.2,
        seed: int = 42
    ) -> Tuple[List[int], List[float], List[float]]:
        """Generate learning curve data points"""
        random.seed(seed)
        n = len(features)
        indices = list(range(n))
        random.shuffle(indices)

        val_size = int(n * val_ratio)
        val_idx = indices[:val_size]
        pool_idx = indices[val_size:]

        X_val = [features[i] for i in val_idx]
        y_val = [targets[i] for i in val_idx]

        if train_ratios is None:
            pool_size = len(pool_idx)
            train_ratios = [int(pool_size * r) for r in [0.1, 0.2, 0.4, 0.6, 0.8, 1.0]]

        train_scores = []
        val_scores = []

        for size in train_ratios:
            subset = pool_idx[:size]
            X_train = [features[i] for i in subset]
            y_train = [targets[i] for i in subset]

            model = model_factory()
            model.fit(X_train, y_train)

            train_pred = [model.predict(x) for x in X_train]
            val_pred = [model.predict(x) for x in X_val]

            train_scores.append(metric_fn(y_train, train_pred))
            val_scores.append(metric_fn(y_val, val_pred))

        return train_ratios, train_scores, val_scores


class ImbalanceAnalyzer:
    """Analyze behavior on imbalanced datasets"""

    @staticmethod
    def compute_class_distributions(labels: List[int]) -> Dict[int, int]:
        """Count samples per class"""
        counts = {}
        for label in labels:
            counts[label] = counts.get(label, 0) + 1
        return counts

    @staticmethod
    def analyze_baseline_performance(
        true_labels: List[int],
        predictions: List[int]
    ) -> Dict[str, float]:
        """Compare model against trivial baselines"""
        positive_count = sum(true_labels)
        negative_count = len(true_labels) - positive_count

        always_positive = [1] * len(true_labels)
        always_negative = [0] * len(true_labels)

        metrics = {}

        # Model performance
        model_metrics = BinaryClassificationMetrics(true_labels, predictions)
        metrics['model_accuracy'] = model_metrics.compute_accuracy()
        metrics['model_precision'] = model_metrics.compute_precision()
        metrics['model_recall'] = model_metrics.compute_recall()
        metrics['model_f1'] = model_metrics.compute_f1()

        # Trivial baselines
        neg_metrics = BinaryClassificationMetrics(true_labels, always_negative)
        pos_metrics = BinaryClassificationMetrics(true_labels, always_positive)

        metrics['negative_baseline_accuracy'] = neg_metrics.compute_accuracy()
        metrics['positive_baseline_accuracy'] = pos_metrics.compute_accuracy()

        return metrics


# Demo models for cross-validation
class SimpleLogisticModel:
    """Simple logistic regression for demonstration"""

    def __init__(self, lr: float = 0.1, epochs: int = 100):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0

    def fit(self, X: List[List[float]], y: List[int]) -> 'SimpleLogisticModel':
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                z = sum(w * x for w, x in zip(self.weights, xi)) + self.bias
                pred = 1.0 / (1.0 + math.exp(-max(-500, min(500, z))))
                error = yi - pred
                for j in range(n_features):
                    self.weights[j] += self.lr * error * xi[j]
                self.bias += self.lr * error

        return self

    def predict(self, x: List[float]) -> int:
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
        return 1 if z >= 0 else 0


class SimpleLinearModel:
    """Simple linear regression for demonstration"""

    def __init__(self, lr: float = 0.001, epochs: int = 200):
        self.lr = lr
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> 'SimpleLinearModel':
        n_features = len(X[0])
        self.weights = [0.0] * n_features
        self.bias = 0.0
        n = len(X)

        for _ in range(self.epochs):
            for xi, yi in zip(X, y):
                pred = sum(w * x for w, x in zip(self.weights, xi)) + self.bias
                error = yi - pred
                for j in range(n_features):
                    self.weights[j] += self.lr * error * xi[j] / n
                self.bias += self.lr * error / n

        return self

    def predict(self, x: List[float]) -> float:
        return sum(w * xi for w, xi in zip(self.weights, x)) + self.bias


# Data generators
def generate_classification_data(n: int = 300, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate synthetic classification data"""
    random.seed(seed)
    X = []
    y = []

    for _ in range(n):
        x1 = random.gauss(0, 1)
        x2 = random.gauss(0, 1)
        label = 1 if (x1 + x2 + random.gauss(0, 0.5)) > 0 else 0
        X.append([x1, x2])
        y.append(label)

    return X, y


def generate_regression_data(n: int = 200, seed: int = 42) -> Tuple[List[List[float]], List[float]]:
    """Generate synthetic regression data"""
    random.seed(seed)
    X = []
    y = []

    for _ in range(n):
        x1 = random.uniform(0, 10)
        x2 = random.uniform(0, 5)
        target = 3 * x1 + 2 * x2 + random.gauss(0, 2)
        X.append([x1, x2])
        y.append(target)

    return X, y


def generate_imbalanced_data(n: int = 300, minority_ratio: float = 0.05, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate imbalanced classification data"""
    random.seed(seed)
    X = []
    y = []

    for _ in range(n):
        if random.random() < minority_ratio:
            x1 = random.gauss(3, 0.5)
            x2 = random.gauss(3, 0.5)
            label = 1
        else:
            x1 = random.gauss(0, 1)
            x2 = random.gauss(0, 1)
            label = 0
        X.append([x1, x2])
        y.append(label)

    return X, y


def standardize(values: List[float]) -> Tuple[List[float], float, float]:
    """Z-score standardization"""
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    std = math.sqrt(variance) if variance > 0 else 1.0
    return [(v - mean) / std for v in values], mean, std


if __name__ == "__main__":
    print("=" * 60)
    print("  FELIX MODEL EVALUATION DEMONSTRATION")
    print("=" * 60)

    # Classification evaluation
    print("\n[1] Train/Validation/Test Split")
    print("-" * 40)
    X_clf, y_clf = generate_classification_data(300)
    X_train, y_train, X_val, y_val, X_test, y_test = DataSplitter.holdout_split(X_clf, y_clf)

    print(f"  Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    print(f"  Train positive ratio: {sum(y_train)}/{len(y_train)}")
    print(f"  Val positive ratio: {sum(y_val)}/{len(y_val)}")

    model = SimpleLogisticModel(lr=0.1, epochs=200)
    model.fit(X_train, y_train)

    print("\n[2] Binary Classification Metrics")
    print("-" * 40)
    y_pred = [model.predict(x) for x in X_test]
    metrics = BinaryClassificationMetrics(y_test, y_pred)

    print(f"  Confusion: TP={metrics.true_positives}, TN={metrics.true_negatives}, FP={metrics.false_positives}, FN={metrics.false_negatives}")
    print(f"  Accuracy:  {metrics.compute_accuracy():.4f}")
    print(f"  Precision: {metrics.compute_precision():.4f}")
    print(f"  Recall:    {metrics.compute_recall():.4f}")
    print(f"  F1 Score:  {metrics.compute_f1():.4f}")

    print("\n[3] K-Fold Cross-Validation (K=5)")
    print("-" * 40)
    cv = CrossValidator(
        model_factory=lambda: SimpleLogisticModel(lr=0.1, epochs=200),
        metric_function=lambda y_true, y_pred: sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true),
        k_folds=5
    )
    scores, mean_score, std_score = cv.validate(X_clf, y_clf)
    print(f"  Fold scores: {[round(s, 4) for s in scores]}")
    print(f"  Mean: {mean_score:.4f} (+/- {std_score:.4f})")

    print("\n[4] Stratified K-Fold Cross-Validation (K=5)")
    print("-" * 40)
    stratified_cv = CrossValidator(
        model_factory=lambda: SimpleLogisticModel(lr=0.1, epochs=200),
        metric_function=lambda y_true, y_pred: sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true),
        k_folds=5,
        stratified=True
    )
    strat_scores, strat_mean, strat_std = stratified_cv.validate(X_clf, y_clf)
    print(f"  Fold scores: {[round(s, 4) for s in strat_scores]}")
    print(f"  Mean: {strat_mean:.4f} (+/- {strat_std:.4f})")

    print("\n[5] Imbalanced Data Analysis")
    print("-" * 40)
    X_imb, y_imb = generate_imbalanced_data(300, minority_ratio=0.05)
    positive_count = sum(y_imb)
    print(f"  Class distribution: {positive_count} positive, {len(y_imb) - positive_count} negative ({positive_count/len(y_imb)*100:.1f}% positive)")

    always_negative = [0] * len(y_imb)
    neg_metrics = BinaryClassificationMetrics(y_imb, always_negative)
    print(f"  Always-negative baseline accuracy: {neg_metrics.compute_accuracy():.4f}")

    X_tr_i, y_tr_i, X_v_i, y_v_i, X_te_i, y_te_i = DataSplitter.holdout_split(X_imb, y_imb)
    model_imb = SimpleLogisticModel(lr=0.5, epochs=500)
    model_imb.fit(X_tr_i, y_tr_i)
    y_pred_imb = [model_imb.predict(x) for x in X_te_i]

    imb_metrics = BinaryClassificationMetrics(y_te_i, y_pred_imb)
    print(f"  Trained model accuracy: {imb_metrics.compute_accuracy():.4f}")
    print(f"  Trained model precision: {imb_metrics.compute_precision():.4f}")
    print(f"  Trained model recall: {imb_metrics.compute_recall():.4f}")
    print(f"  Trained model F1: {imb_metrics.compute_f1():.4f}")

    print("\n[6] Regression Metrics")
    print("-" * 40)
    X_reg, y_reg = generate_regression_data(200)

    col0 = [x[0] for x in X_reg]
    col1 = [x[1] for x in X_reg]
    col0_s, m0, s0 = standardize(col0)
    col1_s, m1, s1 = standardize(col1)
    X_reg_scaled = [[col0_s[i], col1_s[i]] for i in range(len(X_reg))]

    X_tr_r, y_tr_r, X_v_r, y_v_r, X_te_r, y_te_r = DataSplitter.holdout_split(X_reg_scaled, y_reg)
    reg_model = SimpleLinearModel(lr=0.01, epochs=500)
    reg_model.fit(X_tr_r, y_tr_r)
    y_pred_r = [reg_model.predict(x) for x in X_te_r]

    print(f"  MSE:       {RegressionMetrics.mean_squared_error(y_te_r, y_pred_r):.4f}")
    print(f"  RMSE:      {RegressionMetrics.root_mse(y_te_r, y_pred_r):.4f}")
    print(f"  MAE:       {RegressionMetrics.mean_absolute_error(y_te_r, y_pred_r):.4f}")
    print(f"  R-squared: {RegressionMetrics.r_squared(y_te_r, y_pred_r):.4f}")

    baseline = [sum(y_tr_r) / len(y_tr_r)] * len(y_te_r)
    print(f"\n  Mean baseline R-squared: {RegressionMetrics.r_squared(y_te_r, baseline):.4f}")

    print("\n[7] Learning Curve Analysis")
    print("-" * 40)
    ratios, train_sc, val_sc = LearningCurveAnalyzer.generate_curve(
        X_clf, y_clf,
        model_factory=lambda: SimpleLogisticModel(lr=0.1, epochs=200),
        metric_fn=lambda y_true, y_pred: sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp) / len(y_true)
    )

    print(f"  {'Size':>6} {'Train':>8} {'Val':>8}")
    for s, tr, va in zip(ratios, train_sc, val_sc):
        print(f"  {s:>6} {tr:>8.4f} {va:>8.4f}")

    print("\n" + "=" * 60)
    print("  Model evaluation demonstration complete!")
    print("=" * 60)