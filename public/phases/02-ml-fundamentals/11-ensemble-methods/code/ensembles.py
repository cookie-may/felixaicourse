#!/usr/bin/env python3
"""
Felix Learning Platform - Ensemble Methods Module
Combining multiple models for better predictions
Author: Felix Learning
License: MIT

This module implements ensemble methods with custom class-based
architecture for Felix's ML curriculum.
"""

import numpy as np
from typing import List, Tuple, Callable, Optional, Any
from dataclasses import dataclass


@dataclass
class SplitCandidate:
    """Represents a potential split point for weak learners"""
    feature_idx: int
    threshold: float
    polarity: int = 1


class WeakLearnerEvaluator:
    """Evaluate weak learners (decision stumps) for boosting"""

    def __init__(self):
        self.feature_idx: Optional[int] = None
        self.threshold: Optional[float] = None
        self.polarity: int = 1
        self.alpha: Optional[float] = None

    def find_best_split(self, X: np.ndarray, y: np.ndarray, weights: np.ndarray) -> 'WeakLearnerEvaluator':
        """Find the best feature and threshold for weak learner"""
        n_samples, n_features = X.shape
        best_error = float("inf")

        for f in range(n_features):
            thresholds = np.unique(X[:, f])
            for thresh in thresholds:
                for polarity in [1, -1]:
                    pred = np.ones(n_samples)
                    pred[polarity * X[:, f] < polarity * thresh] = -1
                    error = np.sum(weights[pred != y])
                    if error < best_error:
                        best_error = error
                        self.feature_idx = f
                        self.threshold = thresh
                        self.polarity = polarity

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Apply weak learner predictions"""
        n = X.shape[0]
        pred = np.ones(n)
        idx = self.polarity * X[:, self.feature_idx] < self.polarity * self.threshold
        pred[idx] = -1
        return pred


class SampleWeightManager:
    """Manage sample weights for boosting algorithms"""

    @staticmethod
    def initialize(n_samples: int) -> np.ndarray:
        """Initialize uniform weights"""
        return np.full(n_samples, 1.0 / n_samples)

    @staticmethod
    def update(weights: np.ndarray, predictions: np.ndarray, labels: np.ndarray, alpha: float) -> np.ndarray:
        """Update weights based on misclassification"""
        new_weights = weights * np.exp(-alpha * labels * predictions)
        return new_weights / new_weights.sum()


class FelixAdaBoost:
    """AdaBoost classifier combining weak learners adaptively"""

    def __init__(self, n_estimators: int = 50):
        self.n_estimators = n_estimators
        self.weak_learners: List[WeakLearnerEvaluator] = []
        self.learner_weights: List[float] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'FelixAdaBoost':
        """Train AdaBoost ensemble"""
        n = X.shape[0]
        weights = SampleWeightManager.initialize(n)

        for _ in range(self.n_estimators):
            stump = WeakLearnerEvaluator()
            stump.find_best_split(X, y, weights)
            pred = stump.predict(X)

            err = np.sum(weights[pred != y])
            err = np.clip(err, 1e-10, 1 - 1e-10)

            alpha = 0.5 * np.log((1 - err) / err)
            weights = SampleWeightManager.update(weights, pred, y, alpha)

            stump.alpha = alpha
            self.weak_learners.append(stump)
            self.learner_weights.append(alpha)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Weighted vote from all weak learners"""
        total = sum(a * s.predict(X) for a, s in zip(self.learner_weights, self.weak_learners))
        return np.sign(total)

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy"""
        return np.mean(self.predict(X) == y)


@dataclass
class TreeBranch:
    """Branch in regression tree structure"""
    feature_idx: Optional[int] = None
    threshold: Optional[float] = None
    left: Optional['TreeBranch'] = None
    right: Optional['TreeBranch'] = None
    value: Optional[float] = None


class RegressionTreeBuilder:
    """Build regression trees for gradient boosting"""

    def __init__(self, max_depth: int = 3, min_samples_split: int = 2):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.root: Optional[TreeBranch] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'RegressionTreeBuilder':
        """Build regression tree"""
        self.root = self._build(X, y, depth=0)
        return self

    def _build(self, X: np.ndarray, y: np.ndarray, depth: int) -> TreeBranch:
        """Recursively build tree"""
        n_samples, n_features = X.shape

        if depth >= self.max_depth or n_samples < self.min_samples_split:
            return TreeBranch(value=np.mean(y))

        best_gain = -float("inf")
        best_feature = None
        best_threshold = None
        current_var = np.var(y) * n_samples

        for f in range(n_features):
            thresholds = np.unique(X[:, f])
            if len(thresholds) > 20:
                thresholds = np.percentile(X[:, f], np.linspace(0, 100, 20))

            for thresh in thresholds:
                left_mask = X[:, f] <= thresh
                right_mask = ~left_mask

                if left_mask.sum() < 1 or right_mask.sum() < 1:
                    continue

                left_var = np.var(y[left_mask]) * left_mask.sum()
                right_var = np.var(y[right_mask]) * right_mask.sum()
                gain = current_var - left_var - right_var

                if gain > best_gain:
                    best_gain = gain
                    best_feature = f
                    best_threshold = thresh

        if best_feature is None or best_gain <= 0:
            return TreeBranch(value=np.mean(y))

        left_mask = X[:, best_feature] <= best_threshold
        node = TreeBranch(feature_idx=best_feature, threshold=best_threshold)
        node.left = self._build(X[left_mask], y[left_mask], depth + 1)
        node.right = self._build(X[~left_mask], y[~left_mask], depth + 1)
        return node

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict for all samples"""
        return np.array([self._predict_one(x, self.root) for x in X])

    def _predict_one(self, x: np.ndarray, node: TreeBranch) -> float:
        """Predict single sample"""
        if node.value is not None:
            return node.value
        if x[node.feature_idx] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)


class FelixGradientBoosting:
    """Gradient Boosting Regressor for sequential ensemble learning"""

    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1, max_depth: int = 3):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.base_learners: List[RegressionTreeBuilder] = []
        self.initial_prediction: Optional[float] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'FelixGradientBoosting':
        """Train gradient boosting ensemble"""
        self.initial_prediction = np.mean(y)
        current_pred = np.full(len(y), self.initial_prediction)

        for _ in range(self.n_estimators):
            residuals = y - current_pred
            tree = RegressionTreeBuilder(max_depth=self.max_depth)
            tree.fit(X, residuals)
            update = tree.predict(X)
            current_pred += self.learning_rate * update
            self.base_learners.append(tree)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Aggregate predictions from all trees"""
        pred = np.full(X.shape[0], self.initial_prediction)
        for tree in self.base_learners:
            pred += self.learning_rate * tree.predict(X)
        return pred

    def mse(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute mean squared error"""
        return np.mean((self.predict(X) - y) ** 2)


class BootstrapSampler:
    """Bootstrap sampling for bagging"""

    @staticmethod
    def sample(X: np.ndarray, y: np.ndarray, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """Create bootstrap sample with replacement"""
        rng = np.random.RandomState(seed)
        n = len(y)
        idx = rng.choice(n, size=n, replace=True)
        return X[idx], y[idx]


class FelixBaggingClassifier:
    """Bagging ensemble for variance reduction"""

    def __init__(self, n_estimators: int = 20, max_depth: int = 5):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.base_learners: List[RegressionTreeBuilder] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'FelixBaggingClassifier':
        """Train bagging ensemble"""
        rng = np.random.RandomState(42)
        n = len(y)

        for _ in range(self.n_estimators):
            idx = rng.choice(n, size=n, replace=True)
            tree = RegressionTreeBuilder(max_depth=self.max_depth)
            tree.fit(X[idx], y[idx])
            self.base_learners.append(tree)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Majority vote across all learners"""
        predictions = np.array([tree.predict(X) for tree in self.base_learners])
        return np.sign(np.mean(predictions, axis=0))

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy"""
        return np.mean(self.predict(X) == y)


class MetaLearner:
    """Meta-learner for stacking ensemble"""

    def __init__(self, learning_rate: float = 0.1, n_iterations: int = 200):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights: Optional[np.ndarray] = None
        self.bias: float = 0.0

    def fit(self, meta_features: np.ndarray, y: np.ndarray) -> 'MetaLearner':
        """Train meta-learner with gradient descent"""
        n = len(y)
        self.weights = np.zeros(meta_features.shape[1])
        self.bias = 0.0

        for _ in range(self.n_iterations):
            logits = meta_features @ self.weights + self.bias
            preds = np.tanh(logits)
            errors = y - preds
            grad_w = -2 * meta_features.T @ errors / n
            grad_b = -2 * np.sum(errors) / n
            self.weights -= self.learning_rate * grad_w
            self.bias -= self.learning_rate * grad_b

        return self

    def predict(self, meta_features: np.ndarray) -> np.ndarray:
        """Predict from meta-features"""
        logits = meta_features @ self.weights + self.bias
        return np.sign(logits)


class ModelWrapper:
    """Wrapper for base models in stacking"""

    def __init__(self, model_fn: Callable):
        self.model_fn = model_fn
        self.model: Optional[Any] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'ModelWrapper':
        """Fit wrapped model"""
        self.model = self.model_fn()
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict with wrapped model"""
        return self.model.predict(X)


class FelixStackingClassifier:
    """Stacking ensemble with meta-learner"""

    def __init__(self, base_models: List[Callable], meta_learning_rate: float = 0.1, n_folds: int = 5):
        self.base_models = base_models
        self.meta_learning_rate = meta_learning_rate
        self.n_folds = n_folds
        self.meta_learner: Optional[MetaLearner] = None
        self.fitted_models: List[Any] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'FelixStackingClassifier':
        """Train stacking ensemble with cross-validation"""
        n = len(y)
        meta_features = np.zeros((n, len(self.base_models)))

        fold_size = n // self.n_folds
        indices = np.arange(n)

        for fold in range(self.n_folds):
            val_start = fold * fold_size
            val_end = val_start + fold_size if fold < self.n_folds - 1 else n
            val_idx = indices[val_start:val_end]
            train_idx = np.concatenate([indices[:val_start], indices[val_end:]])

            for m_idx, model_fn in enumerate(self.base_models):
                wrapper = ModelWrapper(model_fn)
                wrapper.fit(X[train_idx], y[train_idx])
                meta_features[val_idx, m_idx] = wrapper.predict(X[val_idx])

        self.meta_learner = MetaLearner(learning_rate=self.meta_learning_rate)
        self.meta_learner.fit(meta_features, y)

        self.fitted_models = []
        for model_fn in self.base_models:
            wrapper = ModelWrapper(model_fn)
            wrapper.fit(X, y)
            self.fitted_models.append(wrapper)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using meta-learner"""
        meta_features = np.column_stack([m.predict(X) for m in self.fitted_models])
        return self.meta_learner.predict(meta_features)

    def accuracy(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy"""
        return np.mean(self.predict(X) == y)


class DataGenerator:
    """Generate synthetic datasets for ensemble demos"""

    @staticmethod
    def classification(n_samples: int = 300, n_features: int = 5, noise: float = 0.1, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """Generate classification data"""
        rng = np.random.RandomState(seed)
        X = rng.randn(n_samples, n_features)
        boundary = 0.5 * X[:, 0] + 0.3 * X[:, 1] ** 2 - 0.2 * X[:, 2]
        y = np.where(boundary + rng.normal(0, noise, n_samples) > 0, 1, -1)
        return X, y

    @staticmethod
    def regression(n_samples: int = 300, n_features: int = 5, noise: float = 0.3, seed: int = 42) -> Tuple[np.ndarray, np.ndarray]:
        """Generate regression data"""
        rng = np.random.RandomState(seed)
        X = rng.randn(n_samples, n_features)
        y = 2.0 * X[:, 0] + np.sin(3 * X[:, 1]) - 0.5 * X[:, 2] ** 2 + rng.normal(0, noise, n_samples)
        return X, y

    @staticmethod
    def train_test_split(X: np.ndarray, y: np.ndarray, test_ratio: float = 0.2, seed: int = 42) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Split data into train and test"""
        rng = np.random.RandomState(seed)
        idx = rng.permutation(len(y))
        split = int(len(y) * (1 - test_ratio))
        return X[idx[:split]], X[idx[split:]], y[idx[:split]], y[idx[split:]]


def demonstrate_adaboost():
    """Demo: AdaBoost ensemble learning"""
    print("=" * 60)
    print("  FELIX ADABOOST FROM SCRATCH")
    print("=" * 60)

    X, y = DataGenerator.classification(n_samples=400, n_features=5)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    for n_est in [1, 5, 10, 25, 50]:
        model = FelixAdaBoost(n_estimators=n_est)
        model.fit(X_train, y_train)
        train_acc = model.accuracy(X_train, y_train)
        test_acc = model.accuracy(X_test, y_test)
        print(f"  n_estimators={n_est:>3d}  train_acc={train_acc:.3f}  test_acc={test_acc:.3f}")

    print()


def demonstrate_gradient_boosting():
    """Demo: Gradient Boosting ensemble"""
    print("=" * 60)
    print("  FELIX GRADIENT BOOSTING FROM SCRATCH")
    print("=" * 60)

    X, y = DataGenerator.regression(n_samples=400, n_features=5)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    for n_est in [1, 10, 50, 100, 200]:
        model = FelixGradientBoosting(n_estimators=n_est, learning_rate=0.1)
        model.fit(X_train, y_train)
        train_mse = model.mse(X_train, y_train)
        test_mse = model.mse(X_test, y_test)
        print(f"  n_estimators={n_est:>3d}  train_mse={train_mse:.4f}  test_mse={test_mse:.4f}")

    print()


def demonstrate_learning_rate_effect():
    """Demo: Learning rate vs number of trees"""
    print("=" * 60)
    print("  FELIX LEARNING RATE vs NUMBER OF TREES")
    print("=" * 60)

    X, y = DataGenerator.regression(n_samples=400)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    configs = [(0.5, 20), (0.1, 100), (0.05, 200), (0.01, 500)]

    for lr, n_est in configs:
        model = FelixGradientBoosting(n_estimators=n_est, learning_rate=lr)
        model.fit(X_train, y_train)
        test_mse = model.mse(X_test, y_test)
        print(f"  lr={lr:.2f}, n_trees={n_est:>3d}  test_mse={test_mse:.4f}")

    print()
    print("  Lower learning rates need more trees but often generalize better.")
    print()


def demonstrate_bagging():
    """Demo: Bagging ensemble"""
    print("=" * 60)
    print("  FELIX BAGGING CLASSIFIER")
    print("=" * 60)

    X, y = DataGenerator.classification(n_samples=400)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    single_tree = RegressionTreeBuilder(max_depth=5)
    single_tree.fit(X_train, y_train)
    single_acc = np.mean(np.sign(single_tree.predict(X_test)) == y_test)

    bagging = FelixBaggingClassifier(n_estimators=20, max_depth=5)
    bagging.fit(X_train, y_train)
    bag_acc = bagging.accuracy(X_test, y_test)

    print(f"  Single tree accuracy: {single_acc:.3f}")
    print(f"  Bagging (20 trees):   {bag_acc:.3f}")
    print(f"  Variance reduction:   {bag_acc - single_acc:+.3f}")
    print()


def demonstrate_stacking():
    """Demo: Stacking ensemble"""
    print("=" * 60)
    print("  FELIX STACKING ENSEMBLE")
    print("=" * 60)

    X, y = DataGenerator.classification(n_samples=400)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    def make_tree_d3():
        return RegressionTreeBuilder(max_depth=3)

    def make_tree_d5():
        return RegressionTreeBuilder(max_depth=5)

    def make_tree_d7():
        return RegressionTreeBuilder(max_depth=7)

    base_models = [make_tree_d3, make_tree_d5, make_tree_d7]

    stack = FelixStackingClassifier(base_models=base_models, meta_learning_rate=0.05)
    stack.fit(X_train, y_train)

    for depth, model_fn in zip([3, 5, 7], base_models):
        m = RegressionTreeBuilder(max_depth=depth)
        m.fit(X_train, y_train)
        acc = np.mean(np.sign(m.predict(X_test)) == y_test)
        print(f"  Tree depth={depth} accuracy: {acc:.3f}")

    stack_acc = stack.accuracy(X_test, y_test)
    print(f"  Stacking accuracy:    {stack_acc:.3f}")
    print()


def demonstrate_comparison():
    """Demo: Full ensemble comparison"""
    print("=" * 60)
    print("  FELIX FULL COMPARISON")
    print("=" * 60)

    X, y = DataGenerator.classification(n_samples=500)
    X_train, X_test, y_train, y_test = DataGenerator.train_test_split(X, y)

    single = RegressionTreeBuilder(max_depth=5)
    single.fit(X_train, y_train)
    print(f"  Single tree (d=5):    {np.mean(np.sign(single.predict(X_test)) == y_test):.3f}")

    bag = FelixBaggingClassifier(n_estimators=20, max_depth=5)
    bag.fit(X_train, y_train)
    print(f"  Bagging (20, d=5):    {bag.accuracy(X_test, y_test):.3f}")

    ada = FelixAdaBoost(n_estimators=50)
    ada.fit(X_train, y_train)
    print(f"  AdaBoost (50 stumps): {ada.accuracy(X_test, y_test):.3f}")

    print()
    print("  Bagging reduces variance (better than single tree).")
    print("  Boosting reduces bias (learns complex boundaries from weak learners).")
    print()


if __name__ == "__main__":
    demonstrate_adaboost()
    demonstrate_gradient_boosting()
    demonstrate_learning_rate_effect()
    demonstrate_bagging()
    demonstrate_stacking()
    demonstrate_comparison()
    print("  All ensemble demos complete.")
