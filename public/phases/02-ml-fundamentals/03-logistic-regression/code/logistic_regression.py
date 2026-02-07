#!/usr/bin/env python3
"""
Felix Learning Platform - Logistic Regression Module
Implementation of binary and multi-class classification
Author: Felix Learning
License: MIT

This module provides logistic regression for classification tasks,
including binary classification, softmax for multi-class, and evaluation metrics.
"""

import random
import math
from typing import List, Tuple, Dict, Optional, Callable
from enum import Enum


class ActivationFunction:
    """Sigmoid activation with numerical protection"""

    @staticmethod
    def sigmoid(z: float) -> float:
        """Numerically stable sigmoid"""
        clamped = max(-500, min(500, z))
        return 1.0 / (1.0 + math.exp(-clamped))

    @staticmethod
    def softmax_scores(logits: List[float]) -> List[float]:
        """Stable softmax computation"""
        max_logit = max(logits)
        exp_values = [math.exp(l - max_logit) for l in logits]
        total = sum(exp_values)
        return [e / total for e in exp_values]


class BinaryClassifier:
    """Binary logistic regression classifier"""

    def __init__(self, num_features: int, learning_rate: float = 0.01):
        self.feature_dim = num_features
        self.learning_rate = learning_rate
        self.weights = [0.0] * num_features
        self.bias = 0.0
        self.loss_trajectory: List[float] = []

    def score(self, features: List[float]) -> float:
        """Compute raw model output"""
        return sum(w * x for w, x in zip(self.weights, features)) + self.bias

    def probability(self, features: List[float]) -> float:
        """Compute probability of positive class"""
        return ActivationFunction.sigmoid(self.score(features))

    def predict_class(self, features: List[float], threshold: float = 0.5) -> int:
        """Predict binary label"""
        return 1 if self.probability(features) >= threshold else 0

    def compute_binary_crossentropy(
        self,
        data: List[List[float]],
        labels: List[int]
    ) -> float:
        """Calculate binary cross-entropy loss"""
        n = len(labels)
        total_loss = 0.0

        for i in range(n):
            prob = self.probability(data[i])
            prob = max(1e-15, min(1 - 1e-15, prob))
            total_loss += labels[i] * math.log(prob) + (1 - labels[i]) * math.log(1 - prob)

        return -total_loss / n

    def fit(
        self,
        features: List[List[float]],
        labels: List[int],
        epochs: int = 1000,
        verbose: bool = True,
        log_interval: int = 200
    ) -> 'BinaryClassifier':
        """Train using gradient descent"""
        n_samples = len(labels)
        n_features = len(features[0])

        for epoch in range(epochs):
            weight_gradients = [0.0] * n_features
            bias_gradient = 0.0

            for i in range(n_samples):
                prob = self.probability(features[i])
                error = prob - labels[i]

                for j in range(n_features):
                    weight_gradients[j] += error * features[i][j]
                bias_gradient += error

            for j in range(n_features):
                self.weights[j] -= self.learning_rate * (weight_gradients[j] / n_samples)
            self.bias -= self.learning_rate * (bias_gradient / n_samples)

            loss = self.compute_binary_crossentropy(features, labels)
            self.loss_trajectory.append(loss)

            if verbose and epoch % log_interval == 0:
                weight_str = ", ".join([f"{self.weights[k]:.3f}" for k in range(min(2, n_features))])
                print(f"  Epoch {epoch:4d} | Loss: {loss:.4f} | w: [{weight_str}] | b: {self.bias:.3f}")

        return self

    def accuracy_score(self, data: List[List[float]], labels: List[int]) -> float:
        """Compute classification accuracy"""
        correct = sum(1 for i in range(len(labels)) if self.predict_class(data[i]) == labels[i])
        return correct / len(labels)


class ConfusionMatrixAnalyzer:
    """Analyzes classification confusion matrix"""

    def __init__(self, true_labels: List[int], predicted_labels: List[int]):
        self.true_positives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 1)
        self.true_negatives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 0)
        self.false_positives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 0 and p == 1)
        self.false_negatives = sum(1 for t, p in zip(true_labels, predicted_labels) if t == 1 and p == 0)

    def accuracy(self) -> float:
        """Overall accuracy"""
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        return (self.true_positives + self.true_negatives) / total if total > 0 else 0

    def precision_score(self) -> float:
        """Positive predictive value"""
        denom = self.true_positives + self.false_positives
        return self.true_positives / denom if denom > 0 else 0

    def recall_score(self) -> float:
        """True positive rate / Sensitivity"""
        denom = self.true_positives + self.false_negatives
        return self.true_positives / denom if denom > 0 else 0

    def f1_measure(self) -> float:
        """Harmonic mean of precision and recall"""
        p = self.precision_score()
        r = self.recall_score()
        return 2 * p * r / (p + r) if (p + r) > 0 else 0

    def display_confusion_matrix(self) -> None:
        """Print confusion matrix format"""
        print(f"\n  Confusion Matrix:")
        print(f"                  Predicted")
        print(f"                  Pos   Neg")
        print(f"  Actual Pos     {self.true_positives:4d}  {self.false_negatives:4d}")
        print(f"  Actual Neg     {self.false_positives:4d}  {self.true_negatives:4d}")

    def display_report(self) -> None:
        """Print full classification report"""
        self.display_confusion_matrix()
        print(f"\n  Accuracy:  {self.accuracy():.4f}")
        print(f"  Precision: {self.precision_score():.4f}")
        print(f"  Recall:    {self.recall_score():.4f}")
        print(f"  F1 Score:  {self.f1_measure():.4f}")


class MultiClassClassifier:
    """Softmax regression for multiple classes"""

    def __init__(self, num_features: int, num_classes: int, learning_rate: float = 0.01):
        self.feature_dim = num_features
        self.class_count = num_classes
        self.learning_rate = learning_rate
        self.weight_matrix = [[0.0] * num_features for _ in range(num_classes)]
        self.bias_vector = [0.0] * num_classes

    def compute_logits(self, features: List[float]) -> List[float]:
        """Compute raw scores for each class"""
        return [
            sum(self.weight_matrix[k][j] * features[j] for j in range(self.feature_dim)) + self.bias_vector[k]
            for k in range(self.class_count)
        ]

    def class_probabilities(self, features: List[float]) -> List[float]:
        """Get probability distribution over classes"""
        logits = self.compute_logits(features)
        return ActivationFunction.softmax_scores(logits)

    def predict_label(self, features: List[float]) -> int:
        """Predict most likely class"""
        probs = self.class_probabilities(features)
        return probs.index(max(probs))

    def fit(
        self,
        features: List[List[float]],
        labels: List[int],
        epochs: int = 1000,
        verbose: bool = True,
        log_interval: int = 200
    ) -> 'MultiClassClassifier':
        """Train using cross-entropy loss with softmax"""
        n_samples = len(labels)

        for epoch in range(epochs):
            gradient_weights = [[0.0] * self.feature_dim for _ in range(self.class_count)]
            gradient_biases = [0.0] * self.class_count
            epoch_loss = 0.0

            for i in range(n_samples):
                probs = self.class_probabilities(features[i])

                for k in range(self.class_count):
                    target = 1.0 if labels[i] == k else 0.0
                    error = probs[k] - target

                    for j in range(self.feature_dim):
                        gradient_weights[k][j] += error * features[i][j]
                    gradient_biases[k] += error

                true_prob = max(probs[labels[i]], 1e-15)
                epoch_loss -= math.log(true_prob)

            for k in range(self.class_count):
                for j in range(self.feature_dim):
                    self.weight_matrix[k][j] -= self.learning_rate * (gradient_weights[k][j] / n_samples)
                self.bias_vector[k] -= self.learning_rate * (gradient_biases[k] / n_samples)

            if verbose and epoch % log_interval == 0:
                print(f"  Epoch {epoch:4d} | Loss: {epoch_loss / n_samples:.4f}")

        return self

    def accuracy_score(self, features: List[List[float]], labels: List[int]) -> float:
        """Compute multi-class accuracy"""
        correct = sum(1 for i in range(len(labels)) if self.predict_label(features[i]) == labels[i])
        return correct / len(labels)


class ThresholdOptimizer:
    """Find optimal classification threshold"""

    @staticmethod
    def evaluate_thresholds(
        model: BinaryClassifier,
        test_features: List[List[float]],
        test_labels: List[int],
        thresholds: List[float]
    ) -> List[Dict]:
        """Evaluate model at multiple thresholds"""
        results = []

        for threshold in thresholds:
            predictions = [1 if model.probability(x) >= threshold else 0 for x in test_features]
            analyzer = ConfusionMatrixAnalyzer(test_labels, predictions)

            results.append({
                'threshold': threshold,
                'accuracy': analyzer.accuracy(),
                'precision': analyzer.precision_score(),
                'recall': analyzer.recall_score(),
                'f1': analyzer.f1_measure()
            })

        return results


def generate_binary_data(n_samples: int = 200, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate synthetic binary classification data"""
    random.seed(seed)
    features = []
    labels = []

    # Class 0: centered at (2, 2)
    for _ in range(n_samples // 2):
        features.append([random.gauss(2, 1), random.gauss(2, 1)])
        labels.append(0)

    # Class 1: centered at (5, 5)
    for _ in range(n_samples // 2):
        features.append([random.gauss(5, 1), random.gauss(5, 1)])
        labels.append(1)

    # Shuffle
    combined = list(zip(features, labels))
    random.shuffle(combined)
    features, labels = zip(*combined)

    return list(features), list(labels)


def generate_multi_class_data(num_classes: int = 3, samples_per_class: int = 50, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate synthetic multi-class classification data"""
    random.seed(seed)
    features = []
    labels = []

    centers = [(1, 1), (5, 1), (3, 5)]

    for class_idx, (cx, cy) in enumerate(centers[:num_classes]):
        for _ in range(samples_per_class):
            features.append([random.gauss(cx, 0.8), random.gauss(cy, 0.8)])
            labels.append(class_idx)

    combined = list(zip(features, labels))
    random.shuffle(combined)
    features, labels = zip(*combined)

    return list(features), list(labels)


def demonstrate_classification():
    """Main demonstration of classification implementations"""
    print("=" * 60)
    print("  FELIX LOGISTIC REGRESSION DEMONSTRATION")
    print("=" * 60)

    # Binary classification
    print("\n[1] Binary Classification with Logistic Regression")
    print("-" * 40)
    X, y = generate_binary_data(200)
    print(f"Generated {len(y)} samples (2 classes, 2 features)")
    print(f"Class 0 center: (2, 2), Class 1 center: (5, 5)")
    print(f"First 5 samples: {[(f'[{X[i][0]:.2f}, {X[i][1]:.2f}]', y[i]) for i in range(5)]}")

    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    classifier = BinaryClassifier(num_features=2, learning_rate=0.1)
    classifier.fit(X_train, y_train, epochs=1000, log_interval=200)

    print(f"\nTrain accuracy: {classifier.accuracy_score(X_train, y_train):.4f}")
    print(f"Test accuracy:  {classifier.accuracy_score(X_test, y_test):.4f}")
    print(f"Learned weights: [{classifier.weights[0]:.4f}, {classifier.weights[1]:.4f}]")
    print(f"Bias term: {classifier.bias:.4f}")

    # Classification report
    print("\n[2] Classification Report (Test Set)")
    print("-" * 40)
    predictions = [classifier.predict_class(x) for x in X_test]
    report = ConfusionMatrixAnalyzer(y_test, predictions)
    report.display_report()

    # Decision boundary
    print("\n[3] Decision Boundary Analysis")
    print("-" * 40)
    w1, w2 = classifier.weights
    b = classifier.bias
    print(f"Boundary equation: {w1:.4f}*x1 + {w2:.4f}*x2 + {b:.4f} = 0")
    if abs(w2) > 1e-10:
        print(f"Solved for x2: x2 = {-w1/w2:.4f}*x1 + {-b/w2:.4f}")

    print("\nSample predictions near boundary:")
    test_points = [[3.0, 3.0], [3.5, 3.5], [4.0, 4.0], [2.5, 2.5], [5.0, 5.0]]
    for point in test_points:
        prob = classifier.probability(point)
        pred = classifier.predict_class(point)
        print(f"  {point} -> prob={prob:.4f}, class={pred}")

    # Multi-class softmax regression
    print("\n[4] Multi-class Softmax Regression")
    print("-" * 40)
    X_multi, y_multi = generate_multi_class_data(num_classes=3)
    print(f"Generated 3-class dataset: {len(y_multi)} samples")

    split_multi = int(0.8 * len(X_multi))
    X_train_m, X_test_m = X_multi[:split_multi], X_multi[split_multi:]
    y_train_m, y_test_m = y_multi[:split_multi], y_multi[split_multi:]

    softmax_classifier = MultiClassClassifier(num_features=2, num_classes=3, learning_rate=0.1)
    softmax_classifier.fit(X_train_m, y_train_m, epochs=1000, log_interval=200)

    print(f"\nTrain accuracy: {softmax_classifier.accuracy_score(X_train_m, y_train_m):.4f}")
    print(f"Test accuracy:  {softmax_classifier.accuracy_score(X_test_m, y_test_m):.4f}")

    print("\nSample predictions:")
    for i in range(5):
        probs = softmax_classifier.class_probabilities(X_test_m[i])
        pred = softmax_classifier.predict_label(X_test_m[i])
        prob_str = ", ".join([f"{p:.3f}" for p in probs])
        print(f"  True: {y_test_m[i]}, Predicted: {pred}, Probs: [{prob_str}]")

    # Threshold tuning
    print("\n[5] Threshold Tuning for Precision-Recall Tradeoff")
    print("-" * 40)
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    results = ThresholdOptimizer.evaluate_thresholds(classifier, X_test, y_test, thresholds)

    print(f"{'Threshold':>10} {'Accuracy':>10} {'Precision':>10} {'Recall':>10} {'F1':>10}")
    print("-" * 52)
    for r in results:
        print(f"{r['threshold']:>10.1f} {r['accuracy']:>10.4f} {r['precision']:>10.4f} {r['recall']:>10.4f} {r['f1']:>10.4f}")

    # Why linear regression fails
    print("\n[6] Why Linear Regression Fails for Classification")
    print("-" * 40)
    print("Fitting linear regression to binary labels:")

    study_hours = list(range(1, 11))
    pass_labels = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1]

    n = len(study_hours)
    x_mean = sum(study_hours) / n
    y_mean = sum(pass_labels) / n

    cov = sum((study_hours[i] - x_mean) * (pass_labels[i] - y_mean) for i in range(n))
    var = sum((study_hours[i] - x_mean) ** 2 for i in range(n))
    w_lin = cov / var
    b_lin = y_mean - w_lin * x_mean

    print(f"\nLinear fit: y = {w_lin:.4f}*x + {b_lin:.4f}")
    print(f"{'Hours':>6} {'Actual':>8} {'Linear':>8} {'Sigmoid':>8}")

    for h, actual in zip(study_hours, pass_labels):
        lin_pred = w_lin * h + b_lin
        sig_pred = ActivationFunction.sigmoid(3 * (h - 4.5))
        print(f"{h:>6d} {actual:>8d} {lin_pred:>8.3f} {sig_pred:>8.3f}")

    print("\nLinear regression gives values outside [0, 1].")
    print("Logistic regression keeps everything in [0, 1] as probabilities.")

    print("\n" + "=" * 60)
    print("  Classification demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_classification()