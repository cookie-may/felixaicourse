#!/usr/bin/env python3
"""
Felix Learning Platform - Support Vector Machines Module
Maximum margin classification with kernel methods
Author: Felix Learning
License: MIT

This module implements SVM-based classifiers with emphasis on
modular kernel computation and optimization algorithms.
"""

import math
import random
from typing import List, Tuple, Callable, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Vector:
    """Vector arithmetic utilities for SVM computations"""
    components: List[float]

    def inner_product(self, other: 'Vector') -> float:
        """Compute dot product between vectors"""
        return sum(a * b for a, b in zip(self.components, other.components))

    def add(self, other: 'Vector') -> 'Vector':
        """Vector addition"""
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def subtract(self, other: 'Vector') -> 'Vector':
        """Vector subtraction"""
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def scale(self, scalar: float) -> 'Vector':
        """Scalar multiplication"""
        return Vector([a * scalar for a in self.components])

    def magnitude(self) -> float:
        """Compute L2 norm"""
        return math.sqrt(self.inner_product(self))


class KernelTransformer:
    """Transform input space using various kernel functions"""

    def __init__(self, kernel_type: str = "linear", **kwargs):
        self.kernel_type = kernel_type
        self.params = kwargs

    def compute(self, vec_x: List[float], vec_z: List[float]) -> float:
        """Compute kernel similarity between two vectors"""
        v_x = Vector(vec_x)
        v_z = Vector(vec_z)

        if self.kernel_type == "linear":
            return self._linear_kernel(v_x, v_z)
        elif self.kernel_type == "polynomial":
            return self._polynomial_kernel(v_x, v_z)
        elif self.kernel_type == "rbf":
            return self._radial_basis_kernel(v_x, v_z)
        else:
            return self._linear_kernel(v_x, v_z)

    def _linear_kernel(self, vec_x: Vector, vec_z: Vector) -> float:
        """Linear kernel: K(x, z) = x · z"""
        return vec_x.inner_product(vec_z)

    def _polynomial_kernel(self, vec_x: Vector, vec_z: Vector) -> float:
        """Polynomial kernel: K(x, z) = (x · z + c)^d"""
        degree = self.params.get("degree", 3)
        constant = self.params.get("c", 1.0)
        return (vec_x.inner_product(vec_z) + constant) ** degree

    def _radial_basis_kernel(self, vec_x: Vector, vec_z: Vector) -> float:
        """RBF/Gaussian kernel: K(x, z) = exp(-gamma * ||x - z||^2)"""
        gamma = self.params.get("gamma", 0.5)
        diff = vec_x.subtract(vec_z)
        squared_distance = diff.inner_product(diff)
        return math.exp(-gamma * squared_distance)


class HingeLossCalculator:
    """Compute hinge loss for SVM training"""

    @staticmethod
    def compute(margin: float) -> float:
        """Compute hinge loss for a single sample's margin"""
        return max(0.0, 1.0 - margin)

    @staticmethod
    def batch_loss(predictions: List[Tuple[float, int]]) -> float:
        """Compute average hinge loss over batch"""
        if not predictions:
            return 0.0

        total_loss = 0.0
        for score, label in predictions:
            margin = label * score
            total_loss += HingeLossCalculator.compute(margin)

        return total_loss / len(predictions)


class OptimizationTarget:
    """SVM objective: regularization + hinge loss"""

    def __init__(self, lambda_param: float = 0.01):
        self.lambda_param = lambda_param

    def compute(self, weights: List[float], bias: float,
                X: List[List[float]], y: List[int]) -> float:
        """Compute the full SVM objective"""
        weight_norm = sum(w * w for w in weights)
        regularization = 0.5 * self.lambda_param * weight_norm

        hinge = HingeLossCalculator.batch_loss([
            (sum(w * x_i for w, x_i in zip(weights, x_i)) + bias, y_i)
            for x_i, y_i in zip(X, y)
        ])

        return regularization + hinge


class GradientDescentOptimizer:
    """Stochastic gradient descent for SVM training"""

    def __init__(self, learning_rate: float = 0.001,
                 regularization: float = 0.01,
                 epochs: int = 1000):
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.epochs = epochs

    def step(self, weights: List[float], bias: float,
             sample_x: List[float], sample_y: int) -> Tuple[List[float], float]:
        """Perform one gradient descent step"""
        score = sum(w * x for w, x in zip(weights, sample_x)) + bias
        margin = sample_y * score

        new_weights = []
        for w_j, x_j in zip(weights, sample_x):
            if margin >= 1.0:
                gradient = self.regularization * w_j
            else:
                gradient = self.regularization * w_j - sample_y * x_j
            new_weights.append(w_j - self.learning_rate * gradient)

        new_bias = bias
        if margin < 1.0:
            new_bias = bias - self.learning_rate * (-sample_y)

        return new_weights, new_bias


class MarginCalculator:
    """Compute geometric margin for SVM"""

    @staticmethod
    def geometric_width(weights: List[float]) -> float:
        """Calculate margin width: 2 / ||w||"""
        weight_vec = Vector(weights)
        norm = weight_vec.magnitude()
        if norm == 0:
            return 0.0
        return 2.0 / norm

    @staticmethod
    def functional_margin(sample_x: List[float], label: int,
                         weights: List[float], bias: float) -> float:
        """Compute functional margin: y * (w · x + b)"""
        score = sum(w * x for w, x in zip(weights, sample_x)) + bias
        return label * score


class SupportVectorIdentifier:
    """Identify support vectors from trained SVM"""

    def __init__(self, tolerance: float = 0.1):
        self.tolerance = tolerance

    def find_indices(self, X: List[List[float]], y: List[int],
                     weights: List[float], bias: float) -> List[int]:
        """Find sample indices that are support vectors"""
        support_indices = []

        for i in range(len(X)):
            margin = y[i] * (sum(w * x for w, x in zip(weights, X[i])) + bias)
            if abs(margin - 1.0) < self.tolerance:
                support_indices.append(i)

        return support_indices


class FelixSVMClassifier:
    """Linear SVM classifier with Felix branding"""

    def __init__(self, learning_rate: float = 0.001,
                 regularization: float = 0.01,
                 n_epochs: int = 1000):
        self.learning_rate = learning_rate
        self.regularization = regularization
        self.n_epochs = n_epochs

        self.weights: Optional[List[float]] = None
        self.bias: float = 0.0
        self.loss_progression: List[Tuple[int, float]] = []
        self.optimizer = GradientDescentOptimizer(
            learning_rate, regularization, n_epochs
        )
        self.objective = OptimizationTarget(regularization)

    def fit(self, X: List[List[float]], y: List[int]) -> 'FelixSVMClassifier':
        """Train the SVM classifier"""
        n_features = len(X[0])
        n_samples = len(X)

        self.weights = [0.0] * n_features
        self.bias = 0.0
        self.loss_progression = []

        for epoch in range(self.n_epochs):
            indices = list(range(n_samples))
            random.shuffle(indices)

            for idx in indices:
                self.weights, self.bias = self.optimizer.step(
                    self.weights, self.bias, X[idx], y[idx]
                )

            if epoch % 100 == 0 or epoch == self.n_epochs - 1:
                loss = self.objective.compute(self.weights, self.bias, X, y)
                self.loss_progression.append((epoch, loss))

        return self

    def predict(self, X: List[List[float]]) -> List[int]:
        """Predict binary labels"""
        return [1 if self._score(x) >= 0 else -1 for x in X]

    def decision_scores(self, X: List[List[float]]) -> List[float]:
        """Compute decision function scores"""
        return [self._score(x) for x in X]

    def _score(self, sample: List[float]) -> float:
        """Compute w · x + b"""
        return sum(w * x for w, x in zip(self.weights, sample)) + self.bias

    def get_margin_width(self) -> float:
        """Get geometric margin width"""
        return MarginCalculator.geometric_width(self.weights)

    def get_support_vector_count(self, X: List[List[float]], y: List[int]) -> int:
        """Count number of support vectors"""
        identifier = SupportVectorIdentifier(tolerance=0.3)
        return len(identifier.find_indices(X, y, self.weights, self.bias))


class KernelMatrixBuilder:
    """Build kernel matrices for kernel methods"""

    @staticmethod
    def build(X: List[List[float]], kernel: KernelTransformer) -> List[List[float]]:
        """Compute full kernel matrix K[i][j] = kernel(X[i], X[j])"""
        n = len(X)
        matrix = [[0.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i, n):
                similarity = kernel.compute(X[i], X[j])
                matrix[i][j] = similarity
                matrix[j][i] = similarity

        return matrix


class BinaryClassifierMetrics:
    """Compute metrics for binary classification"""

    @staticmethod
    def compute_accuracy(y_true: List[int], y_pred: List[int]) -> float:
        """Compute classification accuracy"""
        if len(y_true) == 0:
            return 0.0
        correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
        return correct / len(y_true)


def generate_linear_separable(n_samples: int = 100, separation: float = 1.0,
                              seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate linearly separable binary classification data"""
    random.seed(seed)
    X, y = [], []

    for _ in range(n_samples):
        coord_1 = random.uniform(-3, 3)
        coord_2 = random.uniform(-3, 3)
        decision_value = coord_1 + coord_2

        if decision_value > separation / 2:
            X.append([coord_1, coord_2])
            y.append(1)
        elif decision_value < -separation / 2:
            X.append([coord_1, coord_2])
            y.append(-1)

    return X, y


def generate_noisy_classification(n_samples: int = 200, noise_level: float = 0.5,
                                  seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate noisy classification data"""
    random.seed(seed)
    X, y = [], []

    for _ in range(n_samples):
        coord_1 = random.uniform(-3, 3)
        coord_2 = random.uniform(-3, 3)
        decision_value = coord_1 - 0.5 * coord_2 + random.gauss(0, noise_level)
        label = 1 if decision_value > 0 else -1
        X.append([coord_1, coord_2])
        y.append(label)

    return X, y


def generate_circular_boundary(n_samples: int = 200,
                               seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate data with circular decision boundary"""
    random.seed(seed)
    X, y = [], []

    for _ in range(n_samples):
        radius = random.uniform(0, 3)
        angle = random.uniform(0, 2 * math.pi)
        coord_1 = radius * math.cos(angle) + random.gauss(0, 0.1)
        coord_2 = radius * math.sin(angle) + random.gauss(0, 0.1)
        label = 1 if radius > 1.5 else -1
        X.append([coord_1, coord_2])
        y.append(label)

    return X, y


def split_data(X: List[List[float]], y: List[int],
               test_ratio: float = 0.2,
               seed: int = 42) -> Tuple[List, List, List, List]:
    """Split data into training and test sets"""
    random.seed(seed)
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)

    split_pos = int(n * (1 - test_ratio))
    train_idx = indices[:split_pos]
    test_idx = indices[split_pos:]

    return (
        [X[i] for i in train_idx],
        [y[i] for i in train_idx],
        [X[i] for i in test_idx],
        [y[i] for i in test_idx]
    )


def demonstrate_hinge_loss():
    """Demonstrate the hinge loss function"""
    print("=" * 65)
    print("  FELIX HINGE LOSS VISUALIZATION")
    print("=" * 65)
    print()

    margin_values = [-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 3.0]
    print(f"  {'Margin':>10s}  {'Hinge Loss':>12s}  {'Visual':>20s}")
    print(f"  {'-' * 10}  {'-' * 12}  {'-' * 20}")

    for m in margin_values:
        h_loss = HingeLossCalculator.compute(m)
        bar_length = int(h_loss * 5)
        bar = "#" * bar_length
        print(f"  {m:>10.1f}  {h_loss:>12.3f}  {bar}")

    print()
    print("  Hinge loss = 0 when margin >= 1 (outside margin zone).")
    print("  Creates sparse model: points far from boundary don't affect training.")
    print()


def demonstrate_felix_svm():
    """Demonstrate the Felix SVM classifier"""
    print("=" * 65)
    print("  FELIX SVM: LINEAR MAXIMUM MARGIN CLASSIFIER")
    print("=" * 65)
    print()

    X, y = generate_linear_separable(200, separation=1.0, seed=42)
    X_train, y_train, X_test, y_test = split_data(X, y)

    print(f"  Dataset: {len(X)} samples, linearly separable")
    print(f"  Train/Test: {len(X_train)}/{len(X_test)}")
    print()

    classifier = FelixSVMClassifier(
        learning_rate=0.001,
        regularization=0.01,
        n_epochs=500
    )
    classifier.fit(X_train, y_train)

    train_predictions = classifier.predict(X_train)
    test_predictions = classifier.predict(X_test)

    train_accuracy = BinaryClassifierMetrics.compute_accuracy(y_train, train_predictions)
    test_accuracy = BinaryClassifierMetrics.compute_accuracy(y_test, test_predictions)

    print(f"  Learned weights: [{classifier.weights[0]:.4f}, {classifier.weights[1]:.4f}]")
    print(f"  Learned bias: {classifier.bias:.4f}")
    print(f"  Margin width: {classifier.get_margin_width():.4f}")
    print(f"  Train accuracy: {train_accuracy:.4f}")
    print(f"  Test accuracy: {test_accuracy:.4f}")

    n_support = classifier.get_support_vector_count(X_train, y_train)
    print(f"  Support vectors: {n_support} / {len(X_train)} training points")
    print()

    print("  Training loss progression:")
    print(f"  {'Epoch':>8s}  {'Loss':>10s}")
    print(f"  {'-' * 8}  {'-' * 10}")
    for epoch, loss in classifier.loss_progression:
        print(f"  {epoch:>8d}  {loss:>10.4f}")
    print()


def demonstrate_regularization_tradeoff():
    """Demonstrate C parameter effect on SVM"""
    print("=" * 65)
    print("  FELIX REGULARIZATION TRADE-OFF")
    print("=" * 65)
    print()

    X, y = generate_noisy_classification(300, noise_level=0.8, seed=42)
    X_train, y_train, X_test, y_test = split_data(X, y)

    print(f"  Dataset: {len(X)} samples with noise (not perfectly separable)")
    print(f"  Train/Test: {len(X_train)}/{len(X_test)}")
    print()

    c_values = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    print(f"  {'C':>8s}  {'Lambda':>8s}  {'Train Acc':>10s}  {'Test Acc':>10s}  "
          f"{'Margin':>8s}  {'SVs':>6s}")
    print(f"  {'-' * 8}  {'-' * 8}  {'-' * 10}  {'-' * 10}  {'-' * 8}  {'-' * 6}")

    for c in c_values:
        lam = 1.0 / (c * len(X_train))
        classifier = FelixSVMClassifier(
            learning_rate=0.001,
            regularization=lam,
            n_epochs=500
        )
        classifier.fit(X_train, y_train)

        train_acc = BinaryClassifierMetrics.compute_accuracy(y_train, classifier.predict(X_train))
        test_acc = BinaryClassifierMetrics.compute_accuracy(y_test, classifier.predict(X_test))
        margin = classifier.get_margin_width()
        n_sv = classifier.get_support_vector_count(X_train, y_train)

        print(f"  {c:>8.3f}  {lam:>8.5f}  {train_acc:>10.4f}  {test_acc:>10.4f}  "
              f"{margin:>8.4f}  {n_sv:>6d}")

    print()
    print("  Small C (large lambda): wide margin, more training errors.")
    print("  Large C (small lambda): narrow margin, fewer training errors.")
    print()


def demonstrate_kernel_functions():
    """Demonstrate different kernel functions"""
    print("=" * 65)
    print("  FELIX KERNEL FUNCTIONS")
    print("=" * 65)
    print()

    reference = [1.0, 0.0]
    test_points = [
        ("same direction", [2.0, 0.0]),
        ("perpendicular", [0.0, 1.0]),
        ("close", [1.1, 0.1]),
        ("far same dir", [5.0, 0.0]),
        ("opposite", [-1.0, 0.0]),
    ]

    linear_kernel = KernelTransformer("linear")
    poly_kernel_2 = KernelTransformer("polynomial", degree=2)
    poly_kernel_3 = KernelTransformer("polynomial", degree=3)
    rbf_kernel = KernelTransformer("rbf", gamma=0.5)

    print(f"  Reference point: {reference}")
    print()
    print(f"  {'Point':<20s}  {'Linear':>8s}  {'Poly(d=2)':>10s}  "
          f"{'Poly(d=3)':>10s}  {'RBF(g=0.5)':>12s}")
    print(f"  {'-' * 20}  {'-' * 8}  {'-' * 10}  {'-' * 10}  {'-' * 12}")

    for name, point in test_points:
        k_lin = linear_kernel.compute(reference, point)
        k_p2 = poly_kernel_2.compute(reference, point)
        k_p3 = poly_kernel_3.compute(reference, point)
        k_rbf = rbf_kernel.compute(reference, point)
        print(f"  {name:<20s}  {k_lin:>8.3f}  {k_p2:>10.3f}  {k_p3:>10.3f}  {k_rbf:>12.4f}")

    print()
    print("  Linear kernel: raw dot product (projection similarity).")
    print("  Polynomial kernel: captures feature interactions up to degree d.")
    print("  RBF kernel: locality-based, high for nearby, near zero for distant.")
    print()


def demonstrate_kernel_matrix():
    """Demonstrate kernel matrix computation"""
    print("=" * 65)
    print("  FELIX KERNEL MATRIX ON CIRCULAR DATA")
    print("=" * 65)
    print()

    X, y = generate_circular_boundary(20, seed=42)

    linear_kernel = KernelTransformer("linear")
    rbf_kernel = KernelTransformer("rbf", gamma=1.0)

    K_linear = KernelMatrixBuilder.build(X, linear_kernel)
    K_rbf = KernelMatrixBuilder.build(X, rbf_kernel)

    print(f"  Generated {len(X)} points with circular decision boundary")
    print()

    pos_pos_lin, pos_neg_lin, neg_neg_lin = [], [], []
    pos_pos_rbf, pos_neg_rbf, neg_neg_rbf = [], [], []

    for i in range(len(X)):
        for j in range(i + 1, len(X)):
            if y[i] == 1 and y[j] == 1:
                pos_pos_lin.append(K_linear[i][j])
                pos_pos_rbf.append(K_rbf[i][j])
            elif y[i] == -1 and y[j] == -1:
                neg_neg_lin.append(K_linear[i][j])
                neg_neg_rbf.append(K_rbf[i][j])
            else:
                pos_neg_lin.append(K_linear[i][j])
                pos_neg_rbf.append(K_rbf[i][j])

    def mean_of(lst: List[float]) -> float:
        return sum(lst) / len(lst) if lst else 0.0

    print(f"  Average kernel values between class pairs:")
    print(f"  {'Pair':<15s}  {'Linear':>10s}  {'RBF(g=1)':>12s}")
    print(f"  {'-' * 15}  {'-' * 10}  {'-' * 12}")
    print(f"  {'Same (+/+)':<15s}  {mean_of(pos_pos_lin):>10.4f}  {mean_of(pos_pos_rbf):>12.4f}")
    print(f"  {'Same (-/-)':<15s}  {mean_of(neg_neg_lin):>10.4f}  {mean_of(neg_neg_rbf):>12.4f}")
    print(f"  {'Different':<15s}  {mean_of(pos_neg_lin):>10.4f}  {mean_of(pos_neg_rbf):>12.4f}")
    print()
    print("  Linear kernel: struggles with circular separation.")
    print("  RBF kernel: creates clear separation via local similarity.")
    print()


def demonstrate_feature_augmentation():
    """Demonstrate feature augmentation for nonlinear boundaries"""
    print("=" * 65)
    print("  FELIX FEATURE AUGMENTATION")
    print("=" * 65)
    print()

    X, y = generate_circular_boundary(200, seed=42)
    X_train, y_train, X_test, y_test = split_data(X, y)

    classifier = FelixSVMClassifier(
        learning_rate=0.001,
        regularization=0.01,
        n_epochs=500
    )
    classifier.fit(X_train, y_train)

    train_acc = BinaryClassifierMetrics.compute_accuracy(y_train, classifier.predict(X_train))
    test_acc = BinaryClassifierMetrics.compute_accuracy(y_test, classifier.predict(X_test))

    print(f"  Circular data (not linearly separable)")
    print(f"  Basic Felix SVM: train acc = {train_acc:.4f}, test acc = {test_acc:.4f}")
    print()

    X_train_augmented = [
        [x[0], x[1], x[0] ** 2, x[1] ** 2, x[0] * x[1]]
        for x in X_train
    ]
    X_test_augmented = [
        [x[0], x[1], x[0] ** 2, x[1] ** 2, x[0] * x[1]]
        for x in X_test
    ]

    augmented_classifier = FelixSVMClassifier(
        learning_rate=0.0005,
        regularization=0.01,
        n_epochs=1000
    )
    augmented_classifier.fit(X_train_augmented, y_train)

    train_acc_aug = BinaryClassifierMetrics.compute_accuracy(
        y_train, augmented_classifier.predict(X_train_augmented)
    )
    test_acc_aug = BinaryClassifierMetrics.compute_accuracy(
        y_test, augmented_classifier.predict(X_test_augmented)
    )

    print("  After polynomial feature mapping:")
    print("  (x1, x2) -> (x1, x2, x1², x2², x1*x2)")
    print(f"  Augmented SVM: train acc = {train_acc_aug:.4f}, test acc = {test_acc_aug:.4f}")
    print()
    print("  The kernel trick does this feature mapping implicitly.")
    print("  You compute K(x, z) instead of explicitly building features.")
    print()


def demonstrate_support_vectors():
    """Demonstrate the importance of support vectors"""
    print("=" * 65)
    print("  FELIX SUPPORT VECTORS")
    print("=" * 65)
    print()

    X, y = generate_linear_separable(200, separation=1.5, seed=42)
    X_train, y_train, X_test, y_test = split_data(X, y)

    classifier = FelixSVMClassifier(
        learning_rate=0.001,
        regularization=0.01,
        n_epochs=1000
    )
    classifier.fit(X_train, y_train)

    margin_list = []
    for i in range(len(X_train)):
        m = MarginCalculator.functional_margin(
            X_train[i], y_train[i], classifier.weights, classifier.bias
        )
        margin_list.append((i, m))

    margin_list.sort(key=lambda x: x[1])

    print(f"  Trained on {len(X_train)} points")
    print(f"  Weights: [{classifier.weights[0]:.4f}, {classifier.weights[1]:.4f}]")
    print(f"  Bias: {classifier.bias:.4f}")
    print()
    print("  Points sorted by margin (y * f(x)):")
    print(f"  {'Index':>6s}  {'y':>4s}  {'Margin':>8s}  {'Role':<20s}")
    print(f"  {'-' * 6}  {'-' * 4}  {'-' * 8}  {'-' * 20}")

    for idx, margin in margin_list[:8]:
        if margin < 0:
            role = "MISCLASSIFIED"
        elif margin < 1.0:
            role = "inside margin"
        elif margin < 1.2:
            role = "SUPPORT VECTOR"
        else:
            role = "safely classified"
        print(f"  {idx:>6d}  {y_train[idx]:>4d}  {margin:>8.4f}  {role:<20s}")

    print(f"  ...")
    for idx, margin in margin_list[-3:]:
        print(f"  {idx:>6d}  {y_train[idx]:>4d}  {margin:>8.4f}  {'safely classified':<20s}")

    n_sv = sum(1 for _, m in margin_list if 0.7 < m < 1.3)
    n_safe = sum(1 for _, m in margin_list if m >= 1.3)
    n_inside = sum(1 for _, m in margin_list if 0 < m < 0.7)

    print()
    print(f"  Support vectors (margin ~ 1.0): {n_sv}")
    print(f"  Safely classified (margin >> 1): {n_safe}")
    print(f"  Inside margin (0 < margin < 1): {n_inside}")
    print(f"  Only {n_sv} out of {len(X_train)} points define the boundary!")
    print()


def demonstrate_svm_vs_logistic():
    """Compare SVM with logistic regression"""
    print("=" * 65)
    print("  FELIX SVM vs LOGISTIC REGRESSION")
    print("=" * 65)
    print()

    X, y = generate_noisy_classification(200, noise_level=0.3, seed=42)
    X_train, y_train, X_test, y_test = split_data(X, y)

    svm_classifier = FelixSVMClassifier(
        learning_rate=0.001,
        regularization=0.01,
        n_epochs=500
    )
    svm_classifier.fit(X_train, y_train)
    svm_test_acc = BinaryClassifierMetrics.compute_accuracy(
        y_test, svm_classifier.predict(X_test)
    )

    w_lr = [0.0, 0.0]
    b_lr = 0.0
    lr_rate = 0.01
    for _ in range(500):
        for i in range(len(X_train)):
            z = sum(w_lr[j] * X_train[i][j] for j in range(len(w_lr))) + b_lr
            z = max(-500, min(500, z))
            probability = 1.0 / (1.0 + math.exp(-z))
            y_01 = (y_train[i] + 1) / 2
            error = probability - y_01
            for j in range(len(w_lr)):
                w_lr[j] -= lr_rate * error * X_train[i][j]
            b_lr -= lr_rate * error

    lr_predictions = [1 if sum(w_lr[j] * x[j] for j in range(len(w_lr))) + b_lr >= 0 else -1 for x in X_test]
    lr_test_acc = BinaryClassifierMetrics.compute_accuracy(y_test, lr_predictions)

    n_support = svm_classifier.get_support_vector_count(X_train, y_train)

    print(f"  SVM test accuracy:              {svm_test_acc:.4f}")
    print(f"  Logistic regression test acc: {lr_test_acc:.4f}")
    print()
    print(f"  SVM support vectors:          {n_support} / {len(X_train)}")
    print(f"  Logistic regression:          ALL {len(X_train)} points used")
    print()
    print("  SVM: sparse model, only support vectors matter at prediction time.")
    print("  Logistic: dense model, all training points contribute.")
    print()


def demonstrate_margin_generalization():
    """Demonstrate relationship between margin and generalization"""
    print("=" * 65)
    print("  FELIX MARGIN AND GENERALIZATION")
    print("=" * 65)
    print()

    margin_values = [0.5, 1.0, 2.0, 3.0]
    print(f"  {'Data Margin':>12s}  {'SVM Margin':>12s}  {'Train Acc':>10s}  {'Test Acc':>10s}")
    print(f"  {'-' * 12}  {'-' * 12}  {'-' * 10}  {'-' * 10}")

    for data_margin in margin_values:
        X, y = generate_linear_separable(200, separation=data_margin, seed=42)
        X_train, y_train, X_test, y_test = split_data(X, y)

        classifier = FelixSVMClassifier(
            learning_rate=0.001,
            regularization=0.01,
            n_epochs=500
        )
        classifier.fit(X_train, y_train)

        train_acc = BinaryClassifierMetrics.compute_accuracy(y_train, classifier.predict(X_train))
        test_acc = BinaryClassifierMetrics.compute_accuracy(y_test, classifier.predict(X_test))

        print(f"  {data_margin:>12.1f}  {classifier.get_margin_width():>12.4f}  "
              f"{train_acc:>10.4f}  {test_acc:>10.4f}")

    print()
    print("  Wider data separation leads to wider learned margin.")
    print("  Wider margins generally lead to better generalization.")
    print()


def print_felix_summary():
    """Print summary of Felix SVM module"""
    print()
    print("=" * 65)
    print("  FELIX SVM SUMMARY")
    print("=" * 65)
    print()
    print("  1. SVMs find the maximum margin hyperplane between classes.")
    print("  2. Only support vectors (points on the margin) define the boundary.")
    print("  3. Hinge loss creates sparse models (zero loss outside margin zone).")
    print("  4. The C parameter trades off margin width vs classification errors.")
    print("  5. Kernel trick enables nonlinear boundaries via implicit feature maps.")
    print("  6. RBF kernel maps to infinite dimensions using local similarity.")
    print("  7. Linear SVMs train in O(n·d) per epoch using gradient descent.")
    print("  8. SVMs remain powerful for small datasets and sparse high-dim data.")
    print()


if __name__ == "__main__":
    demonstrate_hinge_loss()
    demonstrate_felix_svm()
    demonstrate_regularization_tradeoff()
    demonstrate_kernel_functions()
    demonstrate_kernel_matrix()
    demonstrate_feature_augmentation()
    demonstrate_support_vectors()
    demonstrate_svm_vs_logistic()
    demonstrate_margin_generalization()
    print_felix_summary()