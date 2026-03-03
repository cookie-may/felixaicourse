#!/usr/bin/env python3
"""
Felix Learning Platform - Tree-Based Models Module
Decision trees and ensemble methods for classification and regression
Author: Felix Learning
License: MIT

This module implements tree-based learning algorithms with emphasis on
modular architecture for decision tree construction and ensemble methods.
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any, Callable
from dataclasses import dataclass


@dataclass
class NodeRepresentation:
    """Data structure representing a tree node"""
    is_terminal: bool
    feature_index: Optional[int] = None
    threshold_value: Optional[float] = None
    predicted_value: Optional[Any] = None
    left_subtree: Optional['NodeRepresentation'] = None
    right_subtree: Optional['NodeRepresentation'] = None


class ImpurityCalculator:
    """Calculate impurity metrics for node splitting decisions"""

    @staticmethod
    def gini(label_list: List) -> float:
        """Compute Gini impurity for a set of labels"""
        sample_size = len(label_list)
        if sample_size == 0:
            return 0.0

        frequency_map = {}
        for label in label_list:
            frequency_map[label] = frequency_map.get(label, 0) + 1

        impurity = 1.0
        for count in frequency_map.values():
            proportion = count / sample_size
            impurity -= proportion * proportion

        return impurity

    @staticmethod
    def shannon_entropy(label_list: List) -> float:
        """Compute Shannon entropy for a set of labels"""
        sample_size = len(label_list)
        if sample_size == 0:
            return 0.0

        frequency_map = {}
        for label in label_list:
            frequency_map[label] = frequency_map.get(label, 0) + 1

        entropy_value = 0.0
        for count in frequency_map.values():
            proportion = count / sample_size
            if proportion > 0:
                entropy_value -= proportion * math.log2(proportion)

        return entropy_value

    @staticmethod
    def dispersion_score(value_list: List[float]) -> float:
        """Compute variance-based dispersion for regression"""
        if len(value_list) == 0:
            return 0.0

        mean_value = sum(value_list) / len(value_list)
        variance = sum((v - mean_value) ** 2 for v in value_list) / len(value_list)
        return variance


class SplitEvaluator:
    """Evaluate potential splits for tree construction"""

    def __init__(self, impurity_measure: str = "gini"):
        self.impurity_measure = impurity_measure
        self.impurity_func = self._select_impurity_function()

    def _select_impurity_function(self) -> Callable:
        """Select the appropriate impurity function based on measure type"""
        if self.impurity_measure == "gini":
            return ImpurityCalculator.gini
        elif self.impurity_measure == "entropy":
            return ImpurityCalculator.shannon_entropy
        else:
            return ImpurityCalculator.gini

    def evaluate(self, parent_labels: List, left_labels: List, right_labels: List) -> float:
        """Calculate information gain from a potential split"""
        parent_size = len(parent_labels)
        if parent_size == 0:
            return 0.0

        left_size = len(left_labels)
        right_size = len(right_labels)

        if left_size == 0 or right_size == 0:
            return 0.0

        parent_impurity = self.impurity_func(parent_labels)
        child_impurity = (
            (left_size / parent_size) * self.impurity_func(left_labels)
            + (right_size / parent_size) * self.impurity_func(right_labels)
        )

        return parent_impurity - child_impurity

    def evaluate_regression(self, parent_values: List[float],
                          left_values: List[float], right_values: List[float]) -> float:
        """Calculate variance reduction for regression splits"""
        parent_size = len(parent_values)
        if parent_size == 0 or len(left_values) == 0 or len(right_values) == 0:
            return 0.0

        parent_dispersion = ImpurityCalculator.dispersion_score(parent_values)
        child_dispersion = (
            (len(left_values) / parent_size) * ImpurityCalculator.dispersion_score(left_values)
            + (len(right_values) / parent_size) * ImpurityCalculator.dispersion_score(right_values)
        )

        return parent_dispersion - child_dispersion


class PredictionAggregator:
    """Aggregate predictions from tree models"""

    @staticmethod
    def majority_selection(label_list: List) -> Any:
        """Select the most frequent label (classification)"""
        if len(label_list) == 0:
            return None

        frequency_map = {}
        for label in label_list:
            frequency_map[label] = frequency_map.get(label, 0) + 1

        return max(frequency_map.keys(), key=lambda k: frequency_map[k])

    @staticmethod
    def mean_prediction(value_list: List[float]) -> float:
        """Compute mean prediction (regression)"""
        if len(value_list) == 0:
            return 0.0
        return sum(value_list) / len(value_list)


class BranchingCriteria:
    """Determine branching conditions for tree nodes"""

    @staticmethod
    def find_threshold_candidates(feature_values: List[float]) -> List[float]:
        """Find candidate thresholds between sorted unique values"""
        unique_sorted = sorted(set(feature_values))
        if len(unique_sorted) <= 1:
            return []

        thresholds = []
        for i in range(len(unique_sorted) - 1):
            mid_point = (unique_sorted[i] + unique_sorted[i + 1]) / 2.0
            thresholds.append(mid_point)

        return thresholds

    @staticmethod
    def partition_data(data: List, labels: List, feature_idx: int,
                      threshold: float) -> Tuple[List, List, List, List]:
        """Partition data based on a feature and threshold"""
        left_data, left_labels = [], []
        right_data, right_labels = [], []

        for i, sample in enumerate(data):
            if sample[feature_idx] <= threshold:
                left_data.append(sample)
                left_labels.append(labels[i])
            else:
                right_data.append(sample)
                right_labels.append(labels[i])

        return left_data, left_labels, right_data, right_labels


class TreeNodeBuilder:
    """Build individual nodes of the decision tree"""

    def __init__(self, max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 min_samples_leaf: int = 1,
                 max_features: Optional[Any] = None,
                 criterion: str = "gini",
                 task_type: str = "classification"):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.max_features = max_features
        self.criterion = criterion
        self.task_type = task_type
        self.split_evaluator = SplitEvaluator(criterion)
        self.feature_importances = []

    def construct_node(self, data: List, labels: List, depth: int) -> NodeRepresentation:
        """Recursively construct tree nodes"""
        total_samples = len(data)
        num_features = len(data[0]) if data else 0

        if self._should_stop(labels, depth, total_samples):
            return self._create_leaf(labels)

        best_feature, best_threshold, best_gain = self._find_best_split(data, labels)

        if best_feature is None or best_gain <= 0:
            return self._create_leaf(labels)

        left_data, left_labels, right_data, right_labels = BranchingCriteria.partition_data(
            data, labels, best_feature, best_threshold
        )

        if len(left_labels) < self.min_samples_leaf or len(right_labels) < self.min_samples_leaf:
            return self._create_leaf(labels)

        weight = len(labels) / self.n_total_samples
        self.feature_importances[best_feature] += weight * best_gain

        left_child = self.construct_node(left_data, left_labels, depth + 1)
        right_child = self.construct_node(right_data, right_labels, depth + 1)

        return NodeRepresentation(
            is_terminal=False,
            feature_index=best_feature,
            threshold_value=best_threshold,
            left_subtree=left_child,
            right_subtree=right_child
        )

    def _should_stop(self, labels: List, depth: int, total_samples: int) -> bool:
        """Determine if tree construction should stop"""
        if len(set(labels)) == 1:
            return True

        if self.max_depth is not None and depth >= self.max_depth:
            return True

        if total_samples < self.min_samples_split:
            return True

        return False

    def _create_leaf(self, labels: List) -> NodeRepresentation:
        """Create a leaf node with predicted value"""
        if self.task_type == "classification":
            predicted = PredictionAggregator.majority_selection(labels)
        else:
            predicted = PredictionAggregator.mean_prediction(labels)

        return NodeRepresentation(is_terminal=True, predicted_value=predicted)

    def _find_best_split(self, data: List, labels: List) -> Tuple[Optional[int], Optional[float], float]:
        """Find the best feature and threshold for splitting"""
        num_features = len(data[0])
        best_feature, best_threshold, best_gain = None, None, -1.0

        feature_indices = self._get_feature_indices(num_features)

        for feature_idx in feature_indices:
            feature_values = [sample[feature_idx] for sample in data]
            thresholds = BranchingCriteria.find_threshold_candidates(feature_values)

            for threshold in thresholds:
                left_labels = [labels[i] for i in range(len(data)) if data[i][feature_idx] <= threshold]
                right_labels = [labels[i] for i in range(len(data)) if data[i][feature_idx] > threshold]

                if len(left_labels) < self.min_samples_leaf or len(right_labels) < self.min_samples_leaf:
                    continue

                if self.task_type == "classification":
                    gain = self.split_evaluator.evaluate(labels, left_labels, right_labels)
                else:
                    left_values = [labels[i] for i in range(len(data)) if data[i][feature_idx] <= threshold]
                    right_values = [labels[i] for i in range(len(data)) if data[i][feature_idx] > threshold]
                    gain = self.split_evaluator.evaluate_regression(labels, left_values, right_values)

                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold

        return best_feature, best_threshold, best_gain

    def _get_feature_indices(self, num_features: int) -> List[int]:
        """Get the feature indices to consider for splitting"""
        if self.max_features is None:
            return list(range(num_features))
        elif self.max_features == "sqrt":
            k = max(1, int(math.sqrt(num_features)))
            return random.sample(range(num_features), k)
        elif isinstance(self.max_features, int):
            k = min(self.max_features, num_features)
            return random.sample(range(num_features), k)
        else:
            return list(range(num_features))


class TraversalEngine:
    """Navigate tree structure for predictions"""

    @staticmethod
    def traverse(sample: List, node: NodeRepresentation) -> Any:
        """Traverse tree to get prediction for a sample"""
        if node.is_terminal:
            return node.predicted_value

        if sample[node.feature_index] <= node.threshold_value:
            return TraversalEngine.traverse(sample, node.left_subtree)
        else:
            return TraversalEngine.traverse(sample, node.right_subtree)

    @staticmethod
    def visualize(node: NodeRepresentation, indent: str = "") -> None:
        """Print tree structure for debugging"""
        if node.is_terminal:
            print(f"{indent}Predict: {node.predicted_value}")
            return

        print(f"{indent}Feature {node.feature_index} <= {node.threshold_value:.4f}?")
        print(f"{indent}  Yes:")
        TraversalEngine.visualize(node.left_subtree, indent + "    ")
        print(f"{indent}  No:")
        TraversalEngine.visualize(node.right_subtree, indent + "    ")


class FelixDecisionTree:
    """Main decision tree classifier/regressor with Felix branding"""

    def __init__(self, max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 min_samples_leaf: int = 1,
                 criterion: str = "gini",
                 max_features: Optional[Any] = None,
                 task: str = "classification"):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.max_features = max_features
        self.task = task
        self.root_node: Optional[NodeRepresentation] = None
        self.feature_importances_: Optional[List[float]] = None
        self.n_features: int = 0
        self.n_samples: int = 0

    def fit(self, X: List[List], y: List) -> 'FelixDecisionTree':
        """Build the decision tree from training data"""
        self.n_features = len(X[0])
        self.n_samples = len(X)

        builder = TreeNodeBuilder(
            max_depth=self.max_depth,
            min_samples_split=self.min_samples_split,
            min_samples_leaf=self.min_samples_leaf,
            max_features=self.max_features,
            criterion=self.criterion,
            task_type=self.task
        )
        builder.n_total_samples = self.n_samples
        builder.feature_importances = [0.0] * self.n_features

        self.root_node = builder.construct_node(X, y, depth=0)
        self.feature_importances_ = builder.feature_importances

        total = sum(self.feature_importances_)
        if total > 0:
            self.feature_importances_ = [fi / total for fi in self.feature_importances_]

        return self

    def predict(self, X: List[List]) -> List:
        """Predict class labels or values for samples"""
        return [TraversalEngine.traverse(sample, self.root_node) for sample in X]

    def display_structure(self) -> None:
        """Display the tree structure"""
        if self.root_node:
            TraversalEngine.visualize(self.root_node)


class BootstrapSampler:
    """Create bootstrap samples for ensemble methods"""

    @staticmethod
    def sample_with_replacement(data: List, labels: List, seed: int = 42) -> Tuple[List, List]:
        """Create a bootstrap sample with replacement"""
        random.seed(seed)
        n = len(data)
        indices = [random.randint(0, n - 1) for _ in range(n)]
        bootstrap_data = [data[i] for i in indices]
        bootstrap_labels = [labels[i] for i in indices]
        return bootstrap_data, bootstrap_labels


class EnsembleAggregator:
    """Aggregate predictions from multiple tree models"""

    def __init__(self, task: str = "classification"):
        self.task = task

    def combine(self, predictions: List[List]) -> List:
        """Combine predictions from multiple models"""
        n_samples = len(predictions[0])
        result = []

        for i in range(n_samples):
            sample_preds = [preds[i] for preds in predictions]

            if self.task == "classification":
                result.append(PredictionAggregator.majority_selection(sample_preds))
            else:
                result.append(PredictionAggregator.mean_prediction(sample_preds))

        return result


class FelixRandomForest:
    """Random forest ensemble using Felix-branded decision trees"""

    def __init__(self, n_estimators: int = 100,
                 max_depth: Optional[int] = None,
                 min_samples_split: int = 2,
                 max_features: str = "sqrt",
                 criterion: str = "gini",
                 task: str = "classification"):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.max_features = max_features
        self.criterion = criterion
        self.task = task
        self.forest: List[FelixDecisionTree] = []

    def fit(self, X: List[List], y: List) -> 'FelixRandomForest':
        """Build the random forest from training data"""
        self.forest = []

        for i in range(self.n_estimators):
            bootstrap_data, bootstrap_labels = BootstrapSampler.sample_with_replacement(X, y, seed=i)

            tree = FelixDecisionTree(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features,
                criterion=self.criterion,
                task=self.task
            )
            tree.fit(bootstrap_data, bootstrap_labels)
            self.forest.append(tree)

        return self

    def predict(self, X: List[List]) -> List:
        """Predict using majority voting or averaging"""
        tree_predictions = [tree.predict(X) for tree in self.forest]
        aggregator = EnsembleAggregator(task=self.task)
        return aggregator.combine(tree_predictions)

    def get_feature_importances(self) -> List[float]:
        """Compute average feature importances across all trees"""
        n_features = self.forest[0].n_features
        aggregated = [0.0] * n_features

        for tree in self.forest:
            for j in range(n_features):
                aggregated[j] += tree.feature_importances_[j]

        total = sum(aggregated)
        if total > 0:
            return [imp / total for imp in aggregated]
        return aggregated


class ClassificationMetrics:
    """Compute classification metrics for tree-based models"""

    @staticmethod
    def compute_accuracy(y_true: List, y_pred: List) -> float:
        """Compute classification accuracy"""
        if len(y_true) == 0:
            return 0.0
        correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        return correct / len(y_true)


def generate_classification_synthetic(n_samples: int = 200, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate synthetic classification data"""
    random.seed(seed)
    X, y = [], []

    for _ in range(n_samples):
        coord_x = random.uniform(-3, 3)
        coord_y = random.uniform(-3, 3)
        noise = random.gauss(0, 0.3)

        if coord_x ** 2 + coord_y ** 2 + noise < 3:
            label = 0
        elif coord_x + coord_y + noise > 1:
            label = 1
        else:
            label = 2

        X.append([coord_x, coord_y])
        y.append(label)

    return X, y


def generate_regression_synthetic(n_samples: int = 200, seed: int = 42) -> Tuple[List[List[float]], List[float]]:
    """Generate synthetic regression data"""
    random.seed(seed)
    X, y = [], []

    for _ in range(n_samples):
        input_val = random.uniform(-3, 3)
        target = math.sin(input_val) * input_val + random.gauss(0, 0.2)
        X.append([input_val])
        y.append(target)

    return X, y


def partition_dataset(X: List[List], y: List, test_ratio: float = 0.2,
                     seed: int = 42) -> Tuple[List, List, List, List]:
    """Split data into train and test sets"""
    random.seed(seed)
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)

    split_pos = int(n * (1 - test_ratio))
    train_idx = indices[:split_pos]
    test_idx = indices[split_pos:]

    X_train = [X[i] for i in train_idx]
    y_train = [y[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_test = [y[i] for i in test_idx]

    return X_train, y_train, X_test, y_test


def demonstrate_impurity_measures():
    """Demonstrate different impurity measures"""
    print("=" * 65)
    print("  FELIX IMPURITY MEASURES")
    print("=" * 65)
    print()

    test_distributions = [
        ("Pure [A,A,A,A]", ["A", "A", "A", "A"]),
        ("Balanced [A,A,B,B]", ["A", "A", "B", "B"]),
        ("Imbalanced [A,A,A,B]", ["A", "A", "A", "B"]),
        ("Three-class [A,A,B,C]", ["A", "A", "B", "C"]),
        ("Uniform 4-class", ["A", "B", "C", "D"]),
    ]

    print(f"  {'Distribution':<30s} {'Gini':>8s} {'Entropy':>8s}")
    print(f"  {'-' * 30} {'-' * 8} {'-' * 8}")

    for name, labels in test_distributions:
        gini_val = ImpurityCalculator.gini(labels)
        entropy_val = ImpurityCalculator.shannon_entropy(labels)
        print(f"  {name:<30s} {gini_val:>8.4f} {entropy_val:>8.4f}")

    print()
    print("  Both measures: pure nodes = 0, balanced = maximum.")
    print()


def demonstrate_split_evaluation():
    """Demonstrate split evaluation with information gain"""
    print("=" * 65)
    print("  FELIX SPLIT EVALUATION")
    print("=" * 65)
    print()

    parent_set = ["cat", "cat", "cat", "cat", "dog", "dog", "dog", "bird", "bird", "bird"]

    candidate_splits = [
        ("Feature A: [4 cats+dogs] | [cats, dogs, birds]",
         ["cat", "cat", "cat", "dog"], ["cat", "dog", "dog", "bird", "bird", "bird"]),
        ("Feature B: [4 cats] | [dogs, dogs, dogs, birds, birds, birds]",
         ["cat", "cat", "cat", "cat"], ["dog", "dog", "dog", "bird", "bird", "bird"]),
        ("Feature C: [cat,cat,dog,bird] | [cat,cat,dog,bird]",
         ["cat", "cat", "dog", "bird"], ["cat", "cat", "dog", "bird"]),
    ]

    print(f"  Parent set: {parent_set}")
    print(f"  Parent Gini: {ImpurityCalculator.gini(parent_set):.4f}")
    print(f"  Parent Entropy: {ImpurityCalculator.shannon_entropy(parent_set):.4f}")
    print()

    gini_evaluator = SplitEvaluator("gini")
    entropy_evaluator = SplitEvaluator("entropy")

    print(f"  {'Split':<55s} {'IG(Gini)':>10s} {'IG(Entropy)':>12s}")
    print(f"  {'-' * 55} {'-' * 10} {'-' * 12}")

    for name, left, right in candidate_splits:
        gain_gini = gini_evaluator.evaluate(parent_set, left, right)
        gain_entropy = entropy_evaluator.evaluate(parent_set, left, right)
        print(f"  {name:<55s} {gain_gini:>10.4f} {gain_entropy:>12.4f}")

    print()
    print("  Feature B perfectly separates cats. Highest information gain.")
    print()


def demonstrate_felix_tree():
    """Demonstrate the Felix decision tree classifier"""
    print("=" * 65)
    print("  FELIX DECISION TREE CLASSIFIER")
    print("=" * 65)
    print()

    X, y = generate_classification_synthetic(200, seed=42)
    X_train, y_train, X_test, y_test = partition_dataset(X, y)

    print(f"  Dataset: {len(X)} samples, 2 features, 3 classes")
    print(f"  Train/Test split: {len(X_train)}/{len(X_test)}")
    print()

    max_depths = [1, 2, 3, 5, 10, None]
    print(f"  {'Max Depth':>10s}  {'Train Acc':>10s}  {'Test Acc':>10s}")
    print(f"  {'-' * 10}  {'-' * 10}  {'-' * 10}")

    for depth_limit in max_depths:
        tree = FelixDecisionTree(max_depth=depth_limit, criterion="gini")
        tree.fit(X_train, y_train)

        train_preds = tree.predict(X_train)
        test_preds = tree.predict(X_test)

        train_acc = ClassificationMetrics.compute_accuracy(y_train, train_preds)
        test_acc = ClassificationMetrics.compute_accuracy(y_test, test_preds)

        depth_str = str(depth_limit) if depth_limit is not None else "None"
        print(f"  {depth_str:>10s}  {train_acc:>10.4f}  {test_acc:>10.4f}")

    print()
    print("  Shallow trees underfit. Deep trees may overfit.")
    print("  Optimal depth balances bias-variance tradeoff.")
    print()

    tree = FelixDecisionTree(max_depth=3, criterion="gini")
    tree.fit(X_train, y_train)
    print("  Tree structure (max_depth=3):")
    tree.display_structure()
    print()


def demonstrate_felix_forest():
    """Demonstrate the Felix random forest"""
    print("=" * 65)
    print("  FELIX RANDOM FOREST")
    print("=" * 65)
    print()

    X, y = generate_classification_synthetic(300, seed=42)
    X_train, y_train, X_test, y_test = partition_dataset(X, y)

    print(f"  Dataset: {len(X)} samples, 2 features, 3 classes")
    print(f"  Train/Test split: {len(X_train)}/{len(X_test)}")
    print()

    tree_counts = [1, 3, 5, 10, 25, 50, 100]
    print(f"  {'N Trees':>8s}  {'Train Acc':>10s}  {'Test Acc':>10s}")
    print(f"  {'-' * 8}  {'-' * 10}  {'-' * 10}")

    for n_trees in tree_counts:
        forest = FelixRandomForest(n_estimators=n_trees, max_depth=5, criterion="gini")
        forest.fit(X_train, y_train)

        train_preds = forest.predict(X_train)
        test_preds = forest.predict(X_test)

        train_acc = ClassificationMetrics.compute_accuracy(y_train, train_preds)
        test_acc = ClassificationMetrics.compute_accuracy(y_test, test_preds)

        print(f"  {n_trees:>8d}  {train_acc:>10.4f}  {test_acc:>10.4f}")

    print()
    print("  More trees = better generalization with diminishing returns.")
    print()


def demonstrate_importance_ranking():
    """Demonstrate feature importance ranking"""
    print("=" * 65)
    print("  FELIX FEATURE IMPORTANCE")
    print("=" * 65)
    print()

    random.seed(42)
    n_samples = 200
    X_data, y_labels = [], []

    for _ in range(n_samples):
        important_1 = random.uniform(-2, 2)
        important_2 = random.uniform(-2, 2)
        noise_1 = random.gauss(0, 1)
        noise_2 = random.gauss(0, 1)
        label = 1 if important_1 + important_2 > 0 else 0
        X_data.append([important_1, important_2, noise_1, noise_2])
        y_labels.append(label)

    feature_names = ["important_1", "important_2", "noise_1", "noise_2"]

    forest = FelixRandomForest(n_estimators=50, max_depth=5)
    forest.fit(X_data, y_labels)
    importances = forest.get_feature_importances()

    print("  Target: 1 if feature_0 + feature_1 > 0, else 0")
    print("  Features 2 and 3 are pure noise.")
    print()
    print(f"  {'Feature':<15s}  {'Importance':>12s}")
    print(f"  {'-' * 15}  {'-' * 12}")

    for name, imp in sorted(zip(feature_names, importances), key=lambda x: -x[1]):
        bar = "#" * int(imp * 40)
        print(f"  {name:<15s}  {imp:>12.4f}  {bar}")

    print()
    print("  The forest correctly identifies meaningful features.")
    print()


def demonstrate_regression_trees():
    """Demonstrate regression with trees"""
    print("=" * 65)
    print("  FELIX REGRESSION TREES")
    print("=" * 65)
    print()

    X, y = generate_regression_synthetic(200, seed=42)
    X_train, y_train, X_test, y_test = partition_dataset(X, y)

    max_depths = [1, 2, 3, 5, 10]
    print(f"  Target: y = sin(x) * x + noise")
    print(f"  Train/Test: {len(X_train)}/{len(X_test)}")
    print()

    print(f"  {'Max Depth':>10s}  {'Train MSE':>10s}  {'Test MSE':>10s}")
    print(f"  {'-' * 10}  {'-' * 10}  {'-' * 10}")

    for depth_limit in max_depths:
        tree = FelixDecisionTree(max_depth=depth_limit, task="regression")
        tree.fit(X_train, y_train)

        train_preds = tree.predict(X_train)
        test_preds = tree.predict(X_test)

        train_mse = sum((a - b) ** 2 for a, b in zip(y_train, train_preds)) / len(y_train)
        test_mse = sum((a - b) ** 2 for a, b in zip(y_test, test_preds)) / len(y_test)

        print(f"  {depth_limit:>10d}  {train_mse:>10.4f}  {test_mse:>10.4f}")

    print()

    forest = FelixRandomForest(n_estimators=50, max_depth=5, task="regression")
    forest.fit(X_train, y_train)
    rf_preds = forest.predict(X_test)
    rf_mse = sum((a - b) ** 2 for a, b in zip(y_test, rf_preds)) / len(y_test)

    print(f"  Random Forest (50 trees, depth=5) Test MSE: {rf_mse:.4f}")
    print()
    print("  Forest averages piecewise predictions for smoother output.")
    print()


def demonstrate_criterion_comparison():
    """Compare Gini vs Entropy criteria"""
    print("=" * 65)
    print("  GINI vs ENTROPY CRITERIA COMPARISON")
    print("=" * 65)
    print()

    X, y = generate_classification_synthetic(200, seed=42)
    X_train, y_train, X_test, y_test = partition_dataset(X, y)

    for depth_limit in [3, 5, 10]:
        tree_gini = FelixDecisionTree(max_depth=depth_limit, criterion="gini")
        tree_entropy = FelixDecisionTree(max_depth=depth_limit, criterion="entropy")

        tree_gini.fit(X_train, y_train)
        tree_entropy.fit(X_train, y_train)

        acc_gini = ClassificationMetrics.compute_accuracy(y_test, tree_gini.predict(X_test))
        acc_entropy = ClassificationMetrics.compute_accuracy(y_test, tree_entropy.predict(X_test))

        diff = abs(acc_gini - acc_entropy)
        print(f"  depth={depth_limit:<4d}  Gini: {acc_gini:.4f}  "
              f"Entropy: {acc_entropy:.4f}  Diff: {diff:.4f}")

    print()
    print("  In practice, Gini and entropy produce nearly identical results.")
    print("  Gini is slightly faster (no logarithm computation).")
    print()


def demonstrate_model_stability():
    """Compare single tree vs forest stability"""
    print("=" * 65)
    print("  SINGLE TREE vs FOREST: STABILITY ANALYSIS")
    print("=" * 65)
    print()

    X, y = generate_classification_synthetic(200, seed=42)

    print("  Training 5 single trees on bootstrap samples:")
    single_accuracies = []
    for trial in range(5):
        random.seed(trial * 10)
        indices = [random.randint(0, len(X) - 1) for _ in range(len(X))]
        X_sub = [X[i] for i in indices]
        y_sub = [y[i] for i in indices]
        X_tr, y_tr, X_te, y_te = partition_dataset(X_sub, y_sub, seed=trial)

        tree = FelixDecisionTree(max_depth=5)
        tree.fit(X_tr, y_tr)
        acc = ClassificationMetrics.compute_accuracy(y_te, tree.predict(X_te))
        single_accuracies.append(acc)
        print(f"    Trial {trial + 1}: accuracy = {acc:.4f}")

    print()
    print("  Training 5 random forests on the same bootstrap samples:")
    forest_accuracies = []
    for trial in range(5):
        random.seed(trial * 10)
        indices = [random.randint(0, len(X) - 1) for _ in range(len(X))]
        X_sub = [X[i] for i in indices]
        y_sub = [y[i] for i in indices]
        X_tr, y_tr, X_te, y_te = partition_dataset(X_sub, y_sub, seed=trial)

        forest = FelixRandomForest(n_estimators=30, max_depth=5)
        forest.fit(X_tr, y_tr)
        acc = ClassificationMetrics.compute_accuracy(y_te, forest.predict(X_te))
        forest_accuracies.append(acc)
        print(f"    Trial {trial + 1}: accuracy = {acc:.4f}")

    single_mean = sum(single_accuracies) / 5
    forest_mean = sum(forest_accuracies) / 5
    single_std = (sum((a - single_mean) ** 2 for a in single_accuracies) / 5) ** 0.5
    forest_std = (sum((a - forest_mean) ** 2 for a in forest_accuracies) / 5) ** 0.5

    print()
    print(f"  Single tree:   mean = {single_mean:.4f}, std = {single_std:.4f}")
    print(f"  Random forest: mean = {forest_mean:.4f}, std = {forest_std:.4f}")
    print()
    print("  Forests are more stable (lower variance) across data perturbations.")
    print()


def print_felix_summary():
    """Print summary of Felix tree-based models"""
    print()
    print("=" * 65)
    print("  FELIX SUMMARY: TREE-BASED LEARNING")
    print("=" * 65)
    print()
    print("  1. Decision trees split data by maximizing information gain.")
    print("  2. Gini impurity and entropy produce nearly identical splits.")
    print("  3. Single trees are unstable; small data changes yield different trees.")
    print("  4. Random forests average many trees for stable, strong predictions.")
    print("  5. Bootstrap sampling + feature randomization decorrelate trees.")
    print("  6. Feature importance falls out naturally from impurity reduction.")
    print("  7. Tree-based methods dominate neural networks on tabular data.")
    print()


if __name__ == "__main__":
    demonstrate_impurity_measures()
    demonstrate_split_evaluation()
    demonstrate_felix_tree()
    demonstrate_criterion_comparison()
    demonstrate_felix_forest()
    demonstrate_importance_ranking()
    demonstrate_regression_trees()
    demonstrate_model_stability()
    print_felix_summary()