#!/usr/bin/env python3
"""
Felix Learning Platform - Imbalanced Data Handling Module
Techniques for handling class imbalance in machine learning
Author: Felix Learning
License: MIT

This module demonstrates various strategies for handling imbalanced
datasets including resampling techniques and weighted loss functions.
"""

import random
import math
from typing import List, Tuple, Dict, Callable, Optional
from dataclasses import dataclass


@dataclass
class ImbalanceMetrics:
    """Metrics for imbalanced classification evaluation"""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    mcc: float


class DataSampler:
    """Handles sampling strategies for imbalanced data"""

    @staticmethod
    def create_synthetic_dataset(
        majority_count: int = 950,
        minority_count: int = 50,
        seed: int = 42
    ) -> Tuple[List[List[float]], List[int]]:
        """Generate synthetic imbalanced classification data"""
        random.seed(seed)

        # Majority class centered at origin
        majority = [
            [random.gauss(0.0, 1.0), random.gauss(0.0, 1.0)]
            for _ in range(majority_count)
        ]

        # Minority class offset from majority
        minority = [
            [random.gauss(2.5, 0.8), random.gauss(2.5, 0.8)]
            for _ in range(minority_count)
        ]

        X = majority + minority
        y = [0] * majority_count + [1] * minority_count

        # Shuffle
        indices = list(range(len(y)))
        random.shuffle(indices)
        X = [X[i] for i in indices]
        y = [y[i] for i in indices]

        return X, y

    @staticmethod
    def random_oversample(
        X: List[List[float]],
        y: List[int],
        seed: int = 42
    ) -> Tuple[List[List[float]], List[int]]:
        """Oversample minority class by duplicating samples"""
        random.seed(seed)

        classes = list(set(y))
        counts = {cls: y.count(cls) for cls in classes}
        max_count = max(counts.values())

        X_resampled = [row[:] for row in X]
        y_resampled = y[:]

        for cls, count in counts.items():
            if count < max_count:
                cls_indices = [i for i, label in enumerate(y) if label == cls]
                needed = max_count - count
                choices = random.choices(cls_indices, k=needed)
                X_resampled.extend([X[i][:] for i in choices])
                y_resampled.extend([y[i] for i in choices])

        # Shuffle result
        combined = list(zip(X_resampled, y_resampled))
        random.shuffle(combined)
        X_out, y_out = zip(*combined)

        return list(X_out), list(y_out)

    @staticmethod
    def random_undersample(
        X: List[List[float]],
        y: List[int],
        seed: int = 42
    ) -> Tuple[List[List[float]], List[int]]:
        """Undersample majority class by removing samples"""
        random.seed(seed)

        classes = list(set(y))
        counts = {cls: y.count(cls) for cls in classes}
        min_count = min(counts.values())

        X_resampled = []
        y_resampled = []

        for cls in classes:
            cls_indices = [i for i, label in enumerate(y) if label == cls]
            chosen = random.sample(cls_indices, min_count)
            X_resampled.extend([X[i][:] for i in chosen])
            y_resampled.extend([y[i] for i in chosen])

        combined = list(zip(X_resampled, y_resampled))
        random.shuffle(combined)
        X_out, y_out = zip(*combined)

        return list(X_out), list(y_out)


class SMOTEGenerator:
    """Synthetic Minority Over-sampling Technique (SMOTE)"""

    def __init__(self, k_neighbors: int = 5, random_seed: int = 42):
        self.k = k_neighbors
        self.rng = random.Random(random_seed)

    def compute_distance(self, a: List[float], b: List[float]) -> float:
        """Euclidean distance between two points"""
        return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

    def find_k_nearest(
        self,
        X: List[List[float]],
        index: int,
        k: int
    ) -> List[int]:
        """Find k nearest neighbors for a sample"""
        distances = []
        for i in range(len(X)):
            if i == index:
                continue
            dist = self.compute_distance(X[index], X[i])
            distances.append((i, dist))

        distances.sort(key=lambda x: x[1])
        return [d[0] for d in distances[:k]]

    def generate_synthetic_samples(
        self,
        minority_X: List[List[float]],
        n_synthetic: int
    ) -> List[List[float]]:
        """Generate synthetic minority samples using interpolation"""
        n_minority = len(minority_X)
        effective_k = min(self.k, n_minority - 1)

        if effective_k < 1:
            raise ValueError("SMOTE requires at least 2 minority samples")

        synthetic = []

        for _ in range(n_synthetic):
            idx = self.rng.randint(0, n_minority - 1)
            neighbors = self.find_k_nearest(minority_X, idx, effective_k)
            neighbor_idx = neighbors[self.rng.randint(0, len(neighbors) - 1)]

            # Random interpolation factor
            interpolation = self.rng.random()
            new_point = [
                minority_X[idx][dim] + interpolation * (minority_X[neighbor_idx][dim] - minority_X[idx][dim])
                for dim in range(len(minority_X[0]))
            ]
            synthetic.append(new_point)

        return synthetic

    def resample(
        self,
        X: List[List[float]],
        y: List[int]
    ) -> Tuple[List[List[float]], List[int]]:
        """Apply SMOTE to balance classes"""
        minority_mask = [label == 1 for label in y]
        minority_X = [X[i] for i in range(len(y)) if minority_mask[i]]
        majority_count = sum(1 - m for m in minority_mask)

        n_synthetic_needed = majority_count - len(minority_X)
        synthetic = self.generate_synthetic_samples(minority_X, n_synthetic_needed)

        X_balanced = X + synthetic
        y_balanced = y + [1] * len(synthetic)

        return X_balanced, y_balanced


class WeightedLogisticRegression:
    """Logistic regression with sample weighting support"""

    def __init__(self, learning_rate: float = 0.01, epochs: int = 200):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = 0.0

    def sigmoid(self, z: float) -> float:
        """Numerically stable sigmoid"""
        clamped = max(-500, min(500, z))
        return 1.0 / (1.0 + math.exp(-clamped))

    def fit(
        self,
        X: List[List[float]],
        y: List[int],
        sample_weights: Optional[List[float]] = None
    ) -> 'WeightedLogisticRegression':
        """Train with optional sample weights"""
        n_samples, n_features = len(X), len(X[0])

        if sample_weights is None:
            sample_weights = [1.0] * n_samples

        self.weights = [0.0] * n_features
        self.bias = 0.0

        for _ in range(self.epochs):
            z = [sum(w * x for w, x in zip(self.weights, xi)) + self.bias for xi in X]
            predictions = [self.sigmoid(zi) for zi in z]
            errors = [p - t for p, t in zip(predictions, y)]

            weighted_errors = [e * w for e, w in zip(errors, sample_weights)]

            weight_grad = [
                sum(weighted_errors[i] * X[i][j] for i in range(n_samples)) / n_samples
                for j in range(n_features)
            ]
            bias_grad = sum(weighted_errors) / n_samples

            for j in range(n_features):
                self.weights[j] -= self.lr * weight_grad[j]
            self.bias -= self.lr * bias_grad

        return self

    def predict_proba(self, x: List[float]) -> float:
        """Compute probability for positive class"""
        z = sum(w * xi for w, xi in zip(self.weights, x)) + self.bias
        return self.sigmoid(z)

    def predict(self, x: List[float], threshold: float = 0.5) -> int:
        """Predict class label"""
        return 1 if self.predict_proba(x) >= threshold else 0


class ClassWeightCalculator:
    """Compute class weights for imbalanced datasets"""

    @staticmethod
    def compute_inverse_weights(y: List[int]) -> List[float]:
        """Compute sample weights based on inverse class frequency"""
        classes = list(set(y))
        counts = {cls: y.count(cls) for cls in classes}
        n_samples = len(y)
        n_classes = len(classes)

        weight_map = {cls: n_samples / (n_classes * count) for cls, count in counts.items()}
        return [weight_map[yi] for yi in y]

    @staticmethod
    def compute_balanced_weights(y: List[int]) -> List[float]:
        """Compute balanced sample weights"""
        classes = list(set(y))
        counts = {cls: y.count(cls) for cls in classes}
        n_samples = len(y)

        # Effective number of samples for balanced weight
        beta = 0.9999
        effective_n = {cls: 1.0 - beta ** counts[cls] for cls in classes}

        weight_map = {cls: (1.0 / effective_n[cls]) * (n_samples / len(classes)) for cls in classes}
        return [weight_map[yi] for yi in y]


class WeightedLossFunction:
    """Binary cross-entropy with optional weighting"""

    @staticmethod
    def compute_loss(
        y_true: List[int],
        y_probs: List[float],
        weights: Optional[List[float]] = None
    ) -> float:
        """Compute weighted binary cross-entropy"""
        n = len(y_true)

        if weights is None:
            weights = [1.0] * n

        # Clip probabilities for numerical stability
        clipped = [max(1e-15, min(1 - 1e-15, p)) for p in y_probs]

        total = 0.0
        for i in range(n):
            sample_loss = -(y_true[i] * math.log(clipped[i]) + (1 - y_true[i]) * math.log(1 - clipped[i]))
            total += sample_loss * weights[i]

        return total / n


class ThresholdTuner:
    """Optimize classification threshold for imbalanced data"""

    @staticmethod
    def find_optimal(
        y_true: List[int],
        y_probs: List[float],
        target_metric: str = "f1"
    ) -> Tuple[float, float]:
        """Find threshold that maximizes specified metric"""
        best_threshold = 0.5
        best_score = -1.0

        for threshold in [t / 100.0 for t in range(5, 96)]:
            predictions = [1 if p >= threshold else 0 for p in y_probs]

            tp = sum(1 for yt, yp in zip(y_true, predictions) if yt == 1 and yp == 1)
            fp = sum(1 for yt, yp in zip(y_true, predictions) if yt == 0 and yp == 1)
            fn = sum(1 for yt, yp in zip(y_true, predictions) if yt == 1 and yp == 0)

            if target_metric == "f1":
                prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
                rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
                score = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
            elif target_metric == "recall":
                score = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            elif target_metric == "precision":
                score = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            else:
                score = 0.0

            if score > best_score:
                best_score = score
                best_threshold = threshold

        return best_threshold, best_score


class ConfusionMatrix:
    """Confusion matrix computation and display"""

    def __init__(self, y_true: List[int], y_pred: List[int]):
        self.tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
        self.tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
        self.fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
        self.fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)

    def to_metrics(self) -> ImbalanceMetrics:
        """Convert to metrics dataclass"""
        total = self.tp + self.tn + self.fp + self.fn
        acc = (self.tp + self.tn) / total if total > 0 else 0.0
        prec = self.tp / (self.tp + self.fp) if (self.tp + self.fp) > 0 else 0.0
        rec = self.tp / (self.tp + self.fn) if (self.tp + self.fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

        denom = math.sqrt(float((self.tp + self.fp) * (self.tp + self.fn) * (self.tn + self.fp) * (self.tn + self.fn)))
        mcc = (self.tp * self.tn - self.fp * self.fn) / denom if denom > 0 else 0.0

        return ImbalanceMetrics(accuracy=acc, precision=prec, recall=rec, f1_score=f1, mcc=mcc)

    def display(self, label: str = "") -> None:
        """Print confusion matrix"""
        if label:
            print(f"  {label}")
        print(f"                  Predicted +  Predicted -")
        print(f"    Actual +       {self.tp:>5}        {self.fn:>5}")
        print(f"    Actual -       {self.fp:>5}        {self.tn:>5}")


def display_metrics(metrics: ImbalanceMetrics, label: str = "") -> None:
    """Print metrics with optional label"""
    if label:
        print(f"  {label}")
    print(f"    Accuracy:  {metrics.accuracy:.4f}")
    print(f"    Precision: {metrics.precision:.4f}")
    print(f"    Recall:    {metrics.recall:.4f}")
    print(f"    F1:        {metrics.f1_score:.4f}")
    print(f"    MCC:       {metrics.mcc:.4f}")


def demonstrate_imbalance_handling():
    """Main demonstration of imbalanced data techniques"""
    print("=" * 60)
    print("  FELIX IMBALANCED DATA HANDLING DEMONSTRATION")
    print("=" * 60)

    # Generate imbalanced dataset
    X, y = DataSampler.create_synthetic_dataset(950, 50, seed=42)
    n_pos = sum(y)
    n_neg = len(y) - n_pos

    print(f"\nOriginal dataset: {len(y)} samples")
    print(f"  Positive: {n_pos} ({n_pos/len(y)*100:.1f}%)")
    print(f"  Negative: {n_neg} ({n_neg/len(y)*100:.1f}%)")

    # Train/test split
    split = int(0.8 * len(y))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    print(f"\nTrain: {len(y_train)} samples, Test: {len(y_test)} samples")
    print(f"Train positives: {sum(y_train)}, Test positives: {sum(y_test)}")

    # Method 1: Always predict majority (baseline)
    print("\n" + "-" * 60)
    print("[1] ALWAYS PREDICT MAJORITY (BASELINE)")
    print("-" * 60)
    baseline_preds = [0] * len(y_test)
    baseline_cm = ConfusionMatrix(y_test, baseline_preds)
    baseline_cm.display("Always negative predictions:")
    display_metrics(baseline_cm.to_metrics(), "Baseline metrics:")

    # Method 2: No treatment
    print("\n" + "-" * 60)
    print("[2] NO TREATMENT (PLAIN LOGISTIC REGRESSION)")
    print("-" * 60)
    model_plain = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_plain.fit(X_train, y_train, sample_weights=[1.0] * len(y_train))

    plain_probs = [model_plain.predict_proba(x) for x in X_test]
    plain_preds = [model_plain.predict(x, threshold=0.5) for x in X_test]
    plain_cm = ConfusionMatrix(y_test, plain_preds)
    plain_cm.display("Default threshold (0.5):")
    display_metrics(plain_cm.to_metrics(), "Plain model metrics:")

    # Method 3: Random Oversampling
    print("\n" + "-" * 60)
    print("[3] RANDOM OVERSAMPLING")
    print("-" * 60)
    X_over, y_over = DataSampler.random_oversample(X_train, y_train)
    print(f"  Resampled: {len(y_over)} samples (was {len(y_train)})")
    print(f"  Positive: {sum(y_over)}, Negative: {len(y_over) - sum(y_over)}")

    model_over = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_over.fit(X_over, y_over)

    over_preds = [model_over.predict(x, threshold=0.5) for x in X_test]
    over_cm = ConfusionMatrix(y_test, over_preds)
    over_cm.display("Oversampled model:")
    display_metrics(over_cm.to_metrics(), "Oversampled metrics:")

    # Method 4: Random Undersampling
    print("\n" + "-" * 60)
    print("[4] RANDOM UNDERSAMPLING")
    print("-" * 60)
    X_under, y_under = DataSampler.random_undersample(X_train, y_train)
    print(f"  Resampled: {len(y_under)} samples (was {len(y_train)})")
    print(f"  Positive: {sum(y_under)}, Negative: {len(y_under) - sum(y_under)}")

    model_under = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_under.fit(X_under, y_under)

    under_preds = [model_under.predict(x, threshold=0.5) for x in X_test]
    under_cm = ConfusionMatrix(y_test, under_preds)
    under_cm.display("Undersampled model:")
    display_metrics(under_cm.to_metrics(), "Undersampled metrics:")

    # Method 5: SMOTE
    print("\n" + "-" * 60)
    print("[5] SMOTE (SYNTHETIC MINORITY OVERSAMPLING)")
    print("-" * 60)
    minority_mask_train = [label == 1 for label in y_train]
    minority_X_train = [X_train[i] for i in range(len(y_train)) if minority_mask_train[i]]

    smote = SMOTEGenerator(k_neighbors=5, random_seed=42)
    n_synthetic_needed = len(y_train) - sum(minority_mask_train)
    synthetic_samples = smote.generate_synthetic_samples(minority_X_train, n_synthetic_needed)

    X_smote = X_train + synthetic_samples
    y_smote = y_train + [1] * len(synthetic_samples)

    print(f"  Generated {len(synthetic_samples)} synthetic samples")
    print(f"  Resampled: {len(y_smote)} samples")
    print(f"  Positive: {sum(y_smote)}, Negative: {len(y_smote) - sum(y_smote)}")

    model_smote = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_smote.fit(X_smote, y_smote)

    smote_preds = [model_smote.predict(x, threshold=0.5) for x in X_test]
    smote_cm = ConfusionMatrix(y_test, smote_preds)
    smote_cm.display("SMOTE model:")
    display_metrics(smote_cm.to_metrics(), "SMOTE metrics:")

    # Method 6: Class Weights
    print("\n" + "-" * 60)
    print("[6] CLASS WEIGHTS")
    print("-" * 60)
    sample_weights = ClassWeightCalculator.compute_inverse_weights(y_train)
    unique_weights = list(set(sample_weights))

    print(f"  Negative class weight: {unique_weights[0]:.4f}")
    print(f"  Positive class weight: {unique_weights[-1]:.4f}")

    model_weights = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_weights.fit(X_train, y_train, sample_weights=sample_weights)

    weighted_probs = [model_weights.predict_proba(x) for x in X_test]
    weighted_preds = [model_weights.predict(x, threshold=0.5) for x in X_test]
    weighted_cm = ConfusionMatrix(y_test, weighted_preds)
    weighted_cm.display("Class-weighted model:")
    display_metrics(weighted_cm.to_metrics(), "Class-weighted metrics:")

    # Method 7: Threshold Tuning
    print("\n" + "-" * 60)
    print("[7] THRESHOLD TUNING ON CLASS-WEIGHTED MODEL")
    print("-" * 60)

    # Use validation split for threshold tuning
    val_split = int(0.75 * len(y_train))
    X_tr, X_val = X_train[:val_split], X_train[val_split:]
    y_tr, y_val = y_train[:val_split], y_train[val_split:]

    val_weights = ClassWeightCalculator.compute_inverse_weights(y_tr)
    model_val = WeightedLogisticRegression(learning_rate=0.1, epochs=300)
    model_val.fit(X_tr, y_tr, sample_weights=val_weights)

    val_probs = [model_val.predict_proba(x) for x in X_val]
    best_thresh, best_f1 = ThresholdTuner.find_optimal(y_val, val_probs, target_metric="f1")

    print(f"  Optimal threshold: {best_thresh:.2f} (F1 on validation: {best_f1:.4f})")

    tuned_preds = [1 if p >= best_thresh else 0 for p in weighted_probs]
    tuned_cm = ConfusionMatrix(y_test, tuned_preds)
    tuned_cm.display(f"Threshold = {best_thresh:.2f}:")
    display_metrics(tuned_cm.to_metrics(), "Tuned metrics:")

    # Weighted Loss Comparison
    print("\n" + "-" * 60)
    print("[8] WEIGHTED LOSS FUNCTION ANALYSIS")
    print("-" * 60)
    plain_train_probs = [model_plain.predict_proba(x) for x in X_train]
    weighted_train_probs = [model_weights.predict_proba(x) for x in X_train]

    uniform_w = [1.0] * len(y_train)

    loss_plain_uniform = WeightedLossFunction.compute_loss(y_train, plain_train_probs, uniform_w)
    loss_plain_weighted = WeightedLossFunction.compute_loss(y_train, plain_train_probs, sample_weights)
    loss_weighted_uniform = WeightedLossFunction.compute_loss(y_train, weighted_train_probs, uniform_w)
    loss_weighted_weighted = WeightedLossFunction.compute_loss(y_train, weighted_train_probs, sample_weights)

    print(f"  Plain model, uniform loss:   {loss_plain_uniform:.4f}")
    print(f"  Plain model, weighted loss:  {loss_plain_weighted:.4f}")
    print(f"  Weighted model, uniform:     {loss_weighted_uniform:.4f}")
    print(f"  Weighted model, weighted:    {loss_weighted_weighted:.4f}")

    # Summary Comparison
    print("\n" + "=" * 60)
    print("SUMMARY COMPARISON")
    print("=" * 60)

    approaches = [
        ("Always majority", baseline_cm.to_metrics()),
        ("No treatment", plain_cm.to_metrics()),
        ("Oversampling", over_cm.to_metrics()),
        ("Undersampling", under_cm.to_metrics()),
        ("SMOTE", smote_cm.to_metrics()),
        ("Class weights", weighted_cm.to_metrics()),
        ("CW + threshold", tuned_cm.to_metrics()),
    ]

    print(f"\n  {'Approach':<18} {'Acc':>6} {'Prec':>6} {'Rec':>6} {'F1':>6} {'MCC':>6}")
    print(f"  {'-'*18} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")

    for name, metrics in approaches:
        print(f"  {name:<18} {metrics.accuracy:>6.3f} {metrics.precision:>6.3f} {metrics.recall:>6.3f} {metrics.f1_score:>6.3f} {metrics.mcc:>6.3f}")

    print("\n" + "=" * 60)
    print("  Imbalanced data handling demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_imbalance_handling()