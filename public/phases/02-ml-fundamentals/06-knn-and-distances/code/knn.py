#!/usr/bin/env python3
"""
Felix Learning Platform - K-Nearest Neighbors Module
Distance-based classification and regression algorithms
Author: Felix Learning
License: MIT

This module implements KNN and KD-Tree algorithms with custom
class-based architecture for Felix's ML curriculum.
"""

import math
import random
from typing import List, Callable, Tuple, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VectorPoint:
    """Container for vector data points"""
    coordinates: List[float]
    index: int
    label: Any = None


class MetricCalculator:
    """Compute various distance metrics between vectors"""

    @staticmethod
    def euclidean(vec_a: List[float], vec_b: List[float]) -> float:
        """L2/Euclidean distance"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec_a, vec_b)))

    @staticmethod
    def manhattan(vec_a: List[float], vec_b: List[float]) -> float:
        """L1/Manhattan distance"""
        return sum(abs(a - b) for a, b in zip(vec_a, vec_b))

    @staticmethod
    def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
        """Cosine similarity measure"""
        dot_val = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a ** 2 for a in vec_a))
        norm_b = math.sqrt(sum(b ** 2 for b in vec_b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_val / (norm_a * norm_b)

    @staticmethod
    def cosine_distance(vec_a: List[float], vec_b: List[float]) -> float:
        """Cosine distance (1 - similarity)"""
        return 1.0 - MetricCalculator.cosine_similarity(vec_a, vec_b)

    @staticmethod
    def minkowski(vec_a: List[float], vec_b: List[float], power: float = 2.0) -> float:
        """Minkowski distance family"""
        if power == float('inf'):
            return max(abs(a - b) for a, b in zip(vec_a, vec_b))
        return sum(abs(a - b) ** power for a, b in zip(vec_a, vec_b)) ** (1 / power)


class DataScaler:
    """Standardize features to zero mean and unit variance"""

    def __init__(self):
        self.means: List[float] = []
        self.stds: List[float] = []
        self.is_fitted: bool = False

    def fit(self, X: List[List[float]]) -> 'DataScaler':
        """Compute mean and std for each feature"""
        n = len(X)
        d = len(X[0])
        self.means = [sum(X[i][j] for i in range(n)) / n for j in range(d)]
        self.stds = [
            max(1e-10, (sum((X[i][j] - self.means[j]) ** 2 for i in range(n)) / n) ** 0.5)
            for j in range(d)
        ]
        self.is_fitted = True
        return self

    def transform(self, X: List[List[float]]) -> List[List[float]]:
        """Apply standardization"""
        if not self.is_fitted:
            raise RuntimeError("Scaler must be fitted before transform")
        return [
            [(x[j] - self.means[j]) / self.stds[j] for j in range(len(x))]
            for x in X
        ]

    def fit_transform(self, X: List[List[float]]) -> Tuple[List[List[float]], List[float], List[float]]:
        """Fit and transform in one step"""
        self.fit(X)
        return self.transform(X), self.means, self.stds


class NeighborFinder:
    """Find k-nearest neighbors from a dataset"""

    def __init__(self, k: int = 5, distance_fn: Callable = MetricCalculator.euclidean):
        self.k = k
        self.distance_fn = distance_fn

    def find(self, query: List[float], dataset: List[List[float]]) -> List[Tuple[float, int, Any]]:
        """Find k nearest neighbors with their indices"""
        distances = []
        for i in range(len(dataset)):
            d = self.distance_fn(query, dataset[i])
            distances.append((d, i))
        distances.sort(key=lambda pair: pair[0])
        return distances[:self.k]


class VoteAggregator:
    """Aggregate neighbor votes for classification/regression"""

    @staticmethod
    def majority_vote(labels: List[Any]) -> Any:
        """Simple majority voting"""
        counts = {}
        for label in labels:
            counts[label] = counts.get(label, 0) + 1
        return max(counts, key=counts.get)

    @staticmethod
    def weighted_vote(neighbor_distances: List[Tuple[float, Any]]) -> Any:
        """Distance-weighted majority voting"""
        votes = {}
        for dist, label in neighbor_distances:
            weight = 1.0 / (dist + 1e-10)
            votes[label] = votes.get(label, 0) + weight
        return max(votes, key=votes.get)

    @staticmethod
    def average_regression(values: List[float]) -> float:
        """Simple average for regression"""
        return sum(values) / len(values)

    @staticmethod
    def weighted_regression(neighbor_distances: List[Tuple[float, float]]) -> float:
        """Distance-weighted average for regression"""
        w_sum = 0.0
        val_sum = 0.0
        for dist, val in neighbor_distances:
            w = 1.0 / (dist + 1e-10)
            val_sum += w * val
            w_sum += w
        return val_sum / w_sum if w_sum > 0 else 0.0


class FelixKNNClassifier:
    """K-Nearest Neighbors classifier with configurable distance metrics"""

    def __init__(self, k: int = 5, distance_fn: Callable = MetricCalculator.euclidean,
                 weighted: bool = False):
        self.k = k
        self.distance_fn = distance_fn
        self.weighted = weighted
        self.X_train: List[List[float]] = []
        self.y_train: List[Any] = []

    def fit(self, X: List[List[float]], y: List[Any]) -> 'FelixKNNClassifier':
        """Store training data"""
        self.X_train = list(X)
        self.y_train = list(y)
        return self

    def predict_single(self, x: List[float]) -> Any:
        """Predict label for single sample"""
        finder = NeighborFinder(self.k, self.distance_fn)
        neighbors = finder.find(x, self.X_train)

        neighbor_data = [(dist, self.y_train[idx]) for dist, idx in neighbors]

        if self.weighted:
            return VoteAggregator.weighted_vote(neighbor_data)
        return VoteAggregator.majority_vote([label for _, label in neighbor_data])

    def predict(self, X: List[List[float]]) -> List[Any]:
        """Predict labels for multiple samples"""
        return [self.predict_single(x) for x in X]

    def predict_with_neighbors(self, x: List[float]) -> Tuple[Any, List[Tuple[float, int, Any]]]:
        """Predict and return neighbor information"""
        finder = NeighborFinder(self.k, self.distance_fn)
        neighbors = finder.find(x, self.X_train)
        prediction = self.predict_single(x)
        return prediction, neighbors


class FelixKNNRegressor:
    """K-Nearest Neighbors regressor"""

    def __init__(self, k: int = 5, distance_fn: Callable = MetricCalculator.euclidean,
                 weighted: bool = False):
        self.k = k
        self.distance_fn = distance_fn
        self.weighted = weighted
        self.X_train: List[List[float]] = []
        self.y_train: List[float] = []

    def fit(self, X: List[List[float]], y: List[float]) -> 'FelixKNNRegressor':
        """Store training data"""
        self.X_train = list(X)
        self.y_train = list(y)
        return self

    def predict_single(self, x: List[float]) -> float:
        """Predict value for single sample"""
        finder = NeighborFinder(self.k, self.distance_fn)
        neighbors = finder.find(x, self.X_train)

        neighbor_data = [(dist, self.y_train[idx]) for dist, idx in neighbors]

        if self.weighted:
            return VoteAggregator.weighted_regression(neighbor_data)
        return VoteAggregator.average_regression([val for _, val in neighbor_data])

    def predict(self, X: List[List[float]]) -> List[float]:
        """Predict values for multiple samples"""
        return [self.predict_single(x) for x in X]


@dataclass
class KDNode:
    """Node in KD-Tree structure"""
    point: List[float]
    index: int
    axis: int
    left: Optional['KDNode'] = None
    right: Optional['KDNode'] = None


class KDTreeBuilder:
    """Build KD-Tree for efficient nearest neighbor search"""

    def __init__(self):
        self.root: Optional[KDNode] = None
        self.dimensions: int = 0

    def build(self, points: List[List[float]]) -> KDNode:
        """Construct KD-Tree from point coordinates"""
        if not points:
            return None

        indexed = [(points[i], i) for i in range(len(points))]
        self.dimensions = len(points[0])
        self.root = self._construct(indexed, depth=0)
        return self.root

    def _construct(self, points: List[Tuple[List[float], int]], depth: int) -> Optional[KDNode]:
        """Recursively construct tree nodes"""
        if not points:
            return None

        axis = depth % self.dimensions
        points.sort(key=lambda p: p[0][axis])
        mid = len(points) // 2

        return KDNode(
            point=points[mid][0],
            index=points[mid][1],
            axis=axis,
            left=self._construct(points[:mid], depth + 1),
            right=self._construct(points[mid + 1:], depth + 1)
        )


class KDTreeSearcher:
    """Search KD-Tree for nearest neighbors"""

    def __init__(self, tree_root: KDNode, dimensions: int):
        self.root = tree_root
        self.dimensions = dimensions

    def query(self, point: List[float], k: int = 1) -> List[Tuple[float, int, List[float]]]:
        """Find k nearest neighbors"""
        best: List[Tuple[float, int, List[float]]] = []
        self._search(self.root, point, k, best)
        best.sort(key=lambda x: x[0])
        return best

    def _search(self, node: Optional[KDNode], point: List[float], k: int,
               best: List[Tuple[float, int, List[float]]]):
        """Recursive search with pruning"""
        if node is None:
            return

        dist = MetricCalculator.euclidean(point, node.point)

        if len(best) < k:
            best.append((dist, node.index, node.point))
            best.sort(key=lambda x: x[0])
        elif dist < best[-1][0]:
            best[-1] = (dist, node.index, node.point)
            best.sort(key=lambda x: x[0])

        axis = node.axis
        diff = point[axis] - node.point[axis]

        first = node.left if diff <= 0 else node.right
        second = node.right if diff <= 0 else node.left

        self._search(first, point, k, best)

        if len(best) < k or abs(diff) < best[-1][0]:
            self._search(second, point, k, best)


class FelixKDTree:
    """KD-Tree wrapper for nearest neighbor search"""

    def __init__(self, X: List[List[float]]):
        builder = KDTreeBuilder()
        self.root = builder.build(X)
        self.dimensions = builder.dimensions
        self.searcher = KDTreeSearcher(self.root, self.dimensions)

    def query(self, point: List[float], k: int = 1) -> List[Tuple[float, int, List[float]]]:
        """Find k nearest neighbors"""
        return self.searcher.query(point, k)


class PerformanceMetrics:
    """Compute classification and regression metrics"""

    @staticmethod
    def accuracy(y_true: List[Any], y_pred: List[Any]) -> float:
        """Classification accuracy"""
        correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
        return correct / len(y_true)

    @staticmethod
    def mse(y_true: List[float], y_pred: List[float]) -> float:
        """Mean squared error"""
        return sum((a - b) ** 2 for a, b in zip(y_true, y_pred)) / len(y_true)


class DataGenerator:
    """Generate synthetic datasets for demos"""

    @staticmethod
    def classification(n_samples: int = 200, n_classes: int = 3, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
        """Generate multi-class classification data"""
        random.seed(seed)
        X, y = [], []
        centers = [[1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]]

        for _ in range(n_samples):
            c = random.randint(0, n_classes - 1)
            x1 = centers[c][0] + random.gauss(0, 0.5)
            x2 = centers[c][1] + random.gauss(0, 0.5)
            X.append([x1, x2])
            y.append(c)

        return X, y

    @staticmethod
    def regression(n_samples: int = 200, seed: int = 42) -> Tuple[List[List[float]], List[float]]:
        """Generate sine wave regression data"""
        random.seed(seed)
        X, y = [], []

        for _ in range(n_samples):
            x = random.uniform(-3, 3)
            target = math.sin(x) + random.gauss(0, 0.15)
            X.append([x])
            y.append(target)

        return X, y

    @staticmethod
    def high_dimensional(n_samples: int = 500, n_dims: int = 2, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
        """Generate data with noisy extra dimensions"""
        random.seed(seed)
        X, y = [], []

        for _ in range(n_samples):
            point = [random.uniform(0, 1) for _ in range(n_dims)]
            label = 1 if sum(point[:2]) > 1.0 else 0
            X.append(point)
            y.append(label)

        return X, y

    @staticmethod
    def train_test_split(X: List[List[float]], y: List[Any], test_ratio: float = 0.2, seed: int = 42) -> Tuple[List[List[float]], List[Any], List[List[float]], List[Any]]:
        """Split data into train and test sets"""
        random.seed(seed)
        n = len(X)
        indices = list(range(n))
        random.shuffle(indices)
        split = int(n * (1 - test_ratio))
        train_idx = indices[:split]
        test_idx = indices[split:]
        return (
            [X[i] for i in train_idx], [y[i] for i in train_idx],
            [X[i] for i in test_idx], [y[i] for i in test_idx]
        )


def demonstrate_basic_knn():
    """Demo: Basic KNN classification"""
    print("=" * 65)
    print("  FELIX KNN CLASSIFICATION: THE BASICS")
    print("=" * 65)
    print()

    X, y = DataGenerator.classification(200, seed=42)
    X_train, y_train, X_test, y_test = DataGenerator.train_test_split(X, y)

    print(f"  Dataset: {len(X)} samples, 2 features, 3 classes")
    print(f"  Train: {len(X_train)}  Test: {len(X_test)}")
    print()

    k_values = [1, 3, 5, 7, 11, 15, 25, 50]
    print(f"  {'K':>6s}  {'Train Acc':>10s}  {'Test Acc':>10s}")
    print(f"  {'-' * 6}  {'-' * 10}  {'-' * 10}")

    for k in k_values:
        knn = FelixKNNClassifier(k=k)
        knn.fit(X_train, y_train)
        train_acc = PerformanceMetrics.accuracy(y_train, knn.predict(X_train))
        test_acc = PerformanceMetrics.accuracy(y_test, knn.predict(X_test))
        print(f"  {k:>6d}  {train_acc:>10.4f}  {test_acc:>10.4f}")

    print()
    print("  K=1: perfect training accuracy (memorization), lower test accuracy.")
    print("  Increasing K smooths the decision boundary.")
    print()


def demonstrate_distance_metrics():
    """Demo: Different distance metrics"""
    print("=" * 65)
    print("  FELIX DISTANCE METRICS: SAME DATA, DIFFERENT NEIGHBORS")
    print("=" * 65)
    print()

    X, y = DataGenerator.classification(200, seed=42)
    scaler = DataScaler()
    X_scaled, _, _ = scaler.fit_transform(X)
    X_train, y_train, X_test, y_test = DataGenerator.train_test_split(X_scaled, y)

    metrics = [
        ("L2 (Euclidean)", MetricCalculator.euclidean),
        ("L1 (Manhattan)", MetricCalculator.manhattan),
        ("Cosine", MetricCalculator.cosine_distance),
    ]

    k = 5
    print(f"  K = {k}, features standardized")
    print()
    print(f"  {'Metric':<20s}  {'Test Accuracy':>14s}")
    print(f"  {'-' * 20}  {'-' * 14}")

    for name, dist_fn in metrics:
        knn = FelixKNNClassifier(k=k, distance_fn=dist_fn)
        knn.fit(X_train, y_train)
        test_acc = PerformanceMetrics.accuracy(y_test, knn.predict(X_test))
        print(f"  {name:<20s}  {test_acc:>14.4f}")

    print()


def demonstrate_weighted_knn():
    """Demo: Weighted vs unweighted KNN"""
    print("=" * 65)
    print("  FELIX WEIGHTED vs UNWEIGHTED KNN")
    print("=" * 65)
    print()

    X, y = DataGenerator.classification(200, seed=42)
    scaler = DataScaler()
    X_scaled, _, _ = scaler.fit_transform(X)
    X_train, y_train, X_test, y_test = DataGenerator.train_test_split(X_scaled, y)

    k_values = [3, 7, 15, 25]
    print(f"  {'K':>6s}  {'Unweighted':>12s}  {'Weighted':>12s}  {'Diff':>8s}")
    print(f"  {'-' * 6}  {'-' * 12}  {'-' * 12}  {'-' * 8}")

    for k in k_values:
        knn_uw = FelixKNNClassifier(k=k, weighted=False)
        knn_w = FelixKNNClassifier(k=k, weighted=True)
        knn_uw.fit(X_train, y_train)
        knn_w.fit(X_train, y_train)
        acc_uw = PerformanceMetrics.accuracy(y_test, knn_uw.predict(X_test))
        acc_w = PerformanceMetrics.accuracy(y_test, knn_w.predict(X_test))
        diff = acc_w - acc_uw
        print(f"  {k:>6d}  {acc_uw:>12.4f}  {acc_w:>12.4f}  {diff:>+8.4f}")

    print()
    print("  Weighted KNN is less sensitive to large K values.")
    print()


def demonstrate_regression():
    """Demo: KNN regression"""
    print("=" * 65)
    print("  FELIX KNN REGRESSION: APPROXIMATING sin(x)")
    print("=" * 65)
    print()

    X, y = DataGenerator.regression(200, seed=42)
    X_train, y_train, X_test, y_test = DataGenerator.train_test_split(X, y)

    k_values = [1, 3, 5, 10, 20, 50]
    print(f"  Target: y = sin(x) + noise")
    print(f"  Train: {len(X_train)}  Test: {len(X_test)}")
    print()
    print(f"  {'K':>6s}  {'Unweighted MSE':>16s}  {'Weighted MSE':>14s}")
    print(f"  {'-' * 6}  {'-' * 16}  {'-' * 14}")

    for k in k_values:
        reg_uw = FelixKNNRegressor(k=k, weighted=False)
        reg_w = FelixKNNRegressor(k=k, weighted=True)
        reg_uw.fit(X_train, y_train)
        reg_w.fit(X_train, y_train)
        mse_uw = PerformanceMetrics.mse(y_test, reg_uw.predict(X_test))
        mse_w = PerformanceMetrics.mse(y_test, reg_w.predict(X_test))
        print(f"  {k:>6d}  {mse_uw:>16.6f}  {mse_w:>14.6f}")

    print()


def demonstrate_curse_of_dimensionality():
    """Demo: Curse of dimensionality effect"""
    print("=" * 65)
    print("  FELIX CURSE OF DIMENSIONALITY")
    print("=" * 65)
    print()

    dims = [2, 5, 10, 20, 50, 100]
    n_points = 200

    print("  Part 1: Distance ratio convergence")
    print(f"  {n_points} random uniform points in [0, 1]^d")
    print()
    print(f"  {'Dimensions':>12s}  {'Max/Min dist':>14s}  {'Mean dist':>10s}")
    print(f"  {'-' * 12}  {'-' * 14}  {'-' * 10}")

    for d in dims:
        random.seed(42)
        points = [[random.uniform(0, 1) for _ in range(d)] for _ in range(n_points)]

        distances = []
        sample_size = min(500, n_points * (n_points - 1) // 2)
        for _ in range(sample_size):
            i = random.randint(0, n_points - 1)
            j = random.randint(0, n_points - 1)
            if i != j:
                distances.append(MetricCalculator.euclidean(points[i], points[j]))

        if distances:
            max_d = max(distances)
            min_d = min(val for val in distances if val > 0)
            mean_d = sum(distances) / len(distances)
            ratio = max_d / min_d if min_d > 0 else float("inf")
            print(f"  {d:>12d}  {ratio:>14.4f}  {mean_d:>10.4f}")

    print()
    print("  As dimensions grow, max/min ratio shrinks toward 1.")
    print()


def demonstrate_kdtree():
    """Demo: KD-Tree efficiency"""
    print("=" * 65)
    print("  FELIX KD-TREE: EFFICIENT NEAREST NEIGHBOR SEARCH")
    print("=" * 65)
    print()

    random.seed(42)
    sizes = [100, 500, 1000, 5000]

    print(f"  2D data, finding 5 nearest neighbors")
    print()
    print(f"  {'N points':>10s}  {'Brute force':>14s}  {'KD-tree':>14s}  {'Speedup':>10s}")
    print(f"  {'-' * 10}  {'-' * 14}  {'-' * 14}  {'-' * 10}")

    for n in sizes:
        X = [[random.uniform(0, 10) for _ in range(2)] for _ in range(n)]
        query = [5.0, 5.0]
        k = 5

        import time

        n_queries = 100
        queries = [[random.uniform(0, 10) for _ in range(2)] for _ in range(n_queries)]

        start = time.time()
        for q in queries:
            dists = [(MetricCalculator.euclidean(q, X[i]), i) for i in range(n)]
            dists.sort()
            _ = dists[:k]
        brute_time = time.time() - start

        tree = FelixKDTree(X)

        start = time.time()
        for q in queries:
            _ = tree.query(q, k=k)
        kd_time = time.time() - start

        speedup = brute_time / kd_time if kd_time > 0 else float("inf")
        print(f"  {n:>10d}  {brute_time:>14.4f}s  {kd_time:>14.4f}s  {speedup:>10.1f}x")

    print()


def demonstrate_minkowski_family():
    """Demo: Minkowski distance family"""
    print("=" * 65)
    print("  FELIX MINKOWSKI DISTANCE FAMILY")
    print("=" * 65)
    print()

    a = [1.0, 2.0, 3.0]
    b = [4.0, 0.0, 6.0]

    p_values = [1, 1.5, 2, 3, 5, 10, float("inf")]
    print(f"  a = {a}")
    print(f"  b = {b}")
    print()
    print(f"  {'p':>8s}  {'Distance':>12s}  {'Name':>15s}")
    print(f"  {'-' * 8}  {'-' * 12}  {'-' * 15}")

    for p in p_values:
        d = MetricCalculator.minkowski(a, b, p)
        if p == 1:
            name = "Manhattan (L1)"
        elif p == 2:
            name = "Euclidean (L2)"
        elif p == float("inf"):
            name = "Chebyshev (Linf)"
        else:
            name = f"Lp (p={p})"
        p_str = "inf" if p == float("inf") else str(p)
        print(f"  {p_str:>8s}  {d:>12.4f}  {name:>15s}")

    print()
    print("  As p increases, distance dominated by largest component difference.")
    print()


def demonstrate_k_selection():
    """Demo: K selection via cross-validation"""
    print("=" * 65)
    print("  FELIX SELECTING K: CROSS-VALIDATION APPROACH")
    print("=" * 65)
    print()

    X, y = DataGenerator.classification(300, seed=42)

    n = len(X)
    random.seed(42)
    indices = list(range(n))
    random.shuffle(indices)

    n_folds = 5
    fold_size = n // n_folds

    k_values = [1, 3, 5, 7, 9, 11, 15, 21, 31]

    print(f"  {n_folds}-fold cross-validation on {n} samples")
    print()
    print(f"  {'K':>6s}  {'Mean Acc':>10s}  {'Std Acc':>10s}")
    print(f"  {'-' * 6}  {'-' * 10}  {'-' * 10}")

    for k in k_values:
        fold_accs = []

        for fold in range(n_folds):
            val_start = fold * fold_size
            val_end = val_start + fold_size
            val_idx = indices[val_start:val_end]
            train_idx = indices[:val_start] + indices[val_end:]

            X_tr = [X[i] for i in train_idx]
            y_tr = [y[i] for i in train_idx]
            X_val = [X[i] for i in val_idx]
            y_val = [y[i] for i in val_idx]

            knn = FelixKNNClassifier(k=k)
            knn.fit(X_tr, y_tr)
            acc_val = PerformanceMetrics.accuracy(y_val, knn.predict(X_val))
            fold_accs.append(acc_val)

        mean_acc = sum(fold_accs) / len(fold_accs)
        std_acc = (sum((a - mean_acc) ** 2 for a in fold_accs) / len(fold_accs)) ** 0.5
        print(f"  {k:>6d}  {mean_acc:>10.4f}  {std_acc:>10.4f}")

    print()


def print_summary():
    """Print summary of KNN concepts"""
    print()
    print("=" * 65)
    print("  FELIX KNN SUMMARY")
    print("=" * 65)
    print()
    print("  1. KNN is lazy: zero training, all work at prediction time.")
    print("  2. K controls bias-variance: small K overfits, large K underfits.")
    print("  3. Distance metric choice matters. L2 is default, cosine for text.")
    print("  4. Always scale features. Unscaled features distort distances.")
    print("  5. Weighted KNN reduces sensitivity to K.")
    print("  6. Curse of dimensionality: KNN degrades beyond ~20-50 dimensions.")
    print("  7. KD-trees speed up search in low dimensions.")
    print("  8. KNN is the algorithm behind vector databases and RAG retrieval.")
    print()


if __name__ == "__main__":
    demonstrate_basic_knn()
    demonstrate_distance_metrics()
    demonstrate_weighted_knn()
    demonstrate_regression()
    demonstrate_minkowski_family()
    demonstrate_curse_of_dimensionality()
    demonstrate_kdtree()
    demonstrate_k_selection()
    print_summary()
