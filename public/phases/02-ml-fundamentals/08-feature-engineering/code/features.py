#!/usr/bin/env python3
"""
Felix Learning Platform - Feature Engineering Module
Data preprocessing, transformation, and feature engineering
Author: Felix Learning
License: MIT

This module implements comprehensive feature engineering techniques
for machine learning data preparation and transformation pipelines.
"""

import math
import random
from typing import List, Tuple, Dict, Optional, Any, Callable
from dataclasses import dataclass


@dataclass
class DataStatistics:
    """Statistics for a dataset column"""
    mean: float = 0.0
    std: float = 0.0
    min_val: float = 0.0
    max_val: float = 0.0
    median: float = 0.0
    n_missing: int = 0


class NumericalTransformer:
    """Transform numerical features with scaling and normalization"""

    @staticmethod
    def min_max_transform(values: List[float]) -> List[float]:
        """Scale values to [0, 1] range"""
        min_val = min(values)
        max_val = max(values)
        if max_val == min_val:
            return [0.0] * len(values)
        return [(v - min_val) / (max_val - min_val) for v in values]

    @staticmethod
    def standardize_transform(values: List[float]) -> List[float]:
        """Standardize to zero mean and unit variance"""
        n = len(values)
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        std = math.sqrt(variance) if variance > 0 else 1.0
        return [(v - mean) / std for v in values]

    @staticmethod
    def log_transform(values: List[float]) -> List[float]:
        """Apply log transformation to compress range"""
        return [math.log(v + 1) for v in values]

    @staticmethod
    def sqrt_transform(values: List[float]) -> List[float]:
        """Apply square root transformation"""
        return [math.sqrt(max(0, v)) for v in values]


class DiscretizationBinner:
    """Convert continuous values to discrete bins"""

    def __init__(self, n_bins: int = 5):
        self.n_bins = n_bins
        self.bin_edges: List[float] = []
        self.bin_labels: List[int] = []

    def fit(self, values: List[float]) -> 'DiscretizationBinner':
        """Learn bin edges from data"""
        min_val = min(values)
        max_val = max(values)
        bin_width = (max_val - min_val) / self.n_bins

        self.bin_edges = [min_val + i * bin_width for i in range(self.n_bins + 1)]
        return self

    def transform(self, values: List[float]) -> List[int]:
        """Convert values to bin indices"""
        if not self.bin_edges:
            self.fit(values)

        bin_width = (self.bin_edges[-1] - self.bin_edges[0]) / self.n_bins
        if bin_width == 0:
            return [0] * len(values)

        result = []
        for v in values:
            bin_idx = int((v - self.bin_edges[0]) / bin_width)
            bin_idx = max(0, min(bin_idx, self.n_bins - 1))
            result.append(bin_idx)
        return result

    def fit_transform(self, values: List[float]) -> List[int]:
        """Fit and transform in one step"""
        return self.fit(values).transform(values)


class PolynomialFeatureGenerator:
    """Generate polynomial and interaction features"""

    def __init__(self, degree: int = 2, interaction_only: bool = False):
        self.degree = degree
        self.interaction_only = interaction_only

    def transform(self, row: List[float]) -> List[float]:
        """Generate polynomial features from a single row"""
        n = len(row)
        result = list(row)

        if self.degree >= 2:
            for i in range(n):
                result.append(row[i] ** 2)

            if not self.interaction_only:
                for i in range(n):
                    for j in range(i + 1, n):
                        result.append(row[i] * row[j])

        if self.degree >= 3:
            for i in range(n):
                result.append(row[i] ** 3)

            for i in range(n):
                for j in range(i + 1, n):
                    result.append(row[i] ** 2 * row[j])
                    result.append(row[i] * row[j] ** 2)

        return result


class CategoricalEncoder:
    """Encode categorical variables as numbers"""

    @staticmethod
    def one_hot_encode(values: List[Any]) -> Tuple[List[List[int]], List[Any]]:
        """Convert categories to one-hot vectors"""
        categories = sorted(set(values))
        cat_to_idx = {cat: i for i, cat in enumerate(categories)}
        n_cats = len(categories)

        encoded = []
        for v in values:
            row = [0] * n_cats
            row[cat_to_idx[v]] = 1
            encoded.append(row)

        return encoded, categories

    @staticmethod
    def label_encode(values: List[Any]) -> Tuple[List[int], Dict[Any, int]]:
        """Convert categories to integer labels"""
        categories = sorted(set(values))
        cat_to_int = {cat: i for i, cat in enumerate(categories)}
        return [cat_to_int[v] for v in values], cat_to_int


class TargetMeanEncoder:
    """Encode categories using target variable statistics"""

    def __init__(self, smoothing: float = 10.0):
        self.smoothing = smoothing
        self.global_mean: float = 0.0
        self.category_means: Dict[Any, float] = {}

    def fit(self, feature_values: List[Any], target_values: List[float]) -> 'TargetMeanEncoder':
        """Learn category encodings from target values"""
        self.global_mean = sum(target_values) / len(target_values)

        category_stats = {}
        for feat, target in zip(feature_values, target_values):
            if feat not in category_stats:
                category_stats[feat] = {"sum": 0.0, "count": 0}
            category_stats[feat]["sum"] += target
            category_stats[feat]["count"] += 1

        self.category_means = {}
        for cat, stats in category_stats.items():
            cat_mean = stats["sum"] / stats["count"]
            weight = stats["count"] / (stats["count"] + self.smoothing)
            self.category_means[cat] = weight * cat_mean + (1 - weight) * self.global_mean

        return self

    def transform(self, feature_values: List[Any]) -> List[float]:
        """Encode feature values using learned statistics"""
        return [self.category_means.get(v, self.global_mean) for v in feature_values]

    def fit_transform(self, feature_values: List[Any], target_values: List[float]) -> List[float]:
        """Fit and transform in one step"""
        return self.fit(feature_values, target_values).transform(feature_values)


class TextVectorizer:
    """Convert text documents to feature vectors"""

    @staticmethod
    def count_vectorize(documents: List[str]) -> Tuple[List[List[int]], Dict[str, int]]:
        """Convert documents to count vectors"""
        vocab = {}
        idx = 0
        for doc in documents:
            for word in doc.lower().split():
                if word not in vocab:
                    vocab[word] = idx
                    idx += 1

        vectors = []
        for doc in documents:
            vec = [0] * len(vocab)
            for word in doc.lower().split():
                vec[vocab[word]] += 1
            vectors.append(vec)

        return vectors, vocab

    @staticmethod
    def tfidf_vectorize(documents: List[str]) -> Tuple[List[List[float]], Dict[str, int]]:
        """Convert documents to TF-IDF vectors"""
        n_docs = len(documents)

        vocab = {}
        idx = 0
        for doc in documents:
            for word in doc.lower().split():
                if word not in vocab:
                    vocab[word] = idx
                    idx += 1

        doc_freq = {}
        for doc in documents:
            seen = set()
            for word in doc.lower().split():
                if word not in seen:
                    doc_freq[word] = doc_freq.get(word, 0) + 1
                    seen.add(word)

        vectors = []
        for doc in documents:
            words = doc.lower().split()
            word_count = len(words)

            tf_map = {}
            for word in words:
                tf_map[word] = tf_map.get(word, 0) + 1

            vec = [0.0] * len(vocab)
            for word, count in tf_map.items():
                tf = count / word_count
                idf = math.log(n_docs / doc_freq[word])
                vec[vocab[word]] = tf * idf
            vectors.append(vec)

        return vectors, vocab


class MissingValueHandler:
    """Handle missing values in datasets"""

    @staticmethod
    def impute_with_mean(values: List[Optional[float]]) -> Tuple[List[float], float]:
        """Replace missing values with column mean"""
        present = [v for v in values if v is not None]
        if not present:
            return [0.0] * len(values), 0.0
        mean_val = sum(present) / len(present)
        return [v if v is not None else mean_val for v in values], mean_val

    @staticmethod
    def impute_with_median(values: List[Optional[float]]) -> Tuple[List[float], float]:
        """Replace missing values with column median"""
        present = sorted(v for v in values if v is not None)
        if not present:
            return [0.0] * len(values), 0.0

        n = len(present)
        if n % 2 == 0:
            median_val = (present[n // 2 - 1] + present[n // 2]) / 2
        else:
            median_val = present[n // 2]

        return [v if v is not None else median_val for v in values], median_val

    @staticmethod
    def impute_with_mode(values: List[Optional[Any]]) -> Tuple[List[Any], Optional[Any]]:
        """Replace missing values with most frequent value"""
        present = [v for v in values if v is not None]
        if not present:
            return values, None

        counts = {}
        for v in present:
            counts[v] = counts.get(v, 0) + 1
        mode_val = max(counts, key=counts.get)
        return [v if v is not None else mode_val for v in values], mode_val

    @staticmethod
    def add_missing_indicator(values: List[Optional[Any]]) -> List[int]:
        """Add binary indicator for missing values"""
        return [0 if v is not None else 1 for v in values]


class StatisticalAssociator:
    """Calculate statistical associations between features and targets"""

    @staticmethod
    def pearson_correlation(x: List[float], y: List[float]) -> float:
        """Compute Pearson correlation coefficient"""
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / n
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / n)
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / n)

        if std_x == 0 or std_y == 0:
            return 0.0
        return cov / (std_x * std_y)

    @staticmethod
    def mutual_information_score(feature: List[float], target: List[int],
                                  n_bins: int = 10) -> float:
        """Compute mutual information between feature and target"""
        feat_min = min(feature)
        feat_max = max(feature)
        bin_width = (feat_max - feat_min) / n_bins if feat_max != feat_min else 1.0

        feat_binned = [
            min(int((f - feat_min) / bin_width), n_bins - 1)
            for f in feature
        ]

        n = len(feature)
        target_classes = sorted(set(target))

        feat_bins = sorted(set(feat_binned))
        p_feat = {}
        for b in feat_bins:
            p_feat[b] = feat_binned.count(b) / n

        p_target = {}
        for t in target_classes:
            p_target[t] = target.count(t) / n

        mi = 0.0
        for b in feat_bins:
            for t in target_classes:
                joint_count = sum(
                    1 for fb, tv in zip(feat_binned, target)
                    if fb == b and tv == t
                )
                p_joint = joint_count / n
                if p_joint > 0:
                    mi += p_joint * math.log(p_joint / (p_feat[b] * p_target[t]))

        return mi


class FeatureSelector:
    """Select most relevant features based on various criteria"""

    @staticmethod
    def variance_threshold(features: List[List[float]], threshold: float = 0.01) -> List[int]:
        """Select features with variance above threshold"""
        n_features = len(features[0])
        n_samples = len(features)
        selected = []

        for j in range(n_features):
            column = [features[i][j] for i in range(n_samples)]
            mean = sum(column) / n_samples
            variance = sum((v - mean) ** 2 for v in column) / n_samples
            if variance >= threshold:
                selected.append(j)

        return selected

    @staticmethod
    def remove_correlated_features(features: List[List[float]],
                                   threshold: float = 0.9) -> List[int]:
        """Remove features with high correlation to other features"""
        n_features = len(features[0])
        n_samples = len(features)

        to_remove = set()
        for i in range(n_features):
            if i in to_remove:
                continue
            col_i = [features[r][i] for r in range(n_samples)]
            for j in range(i + 1, n_features):
                if j in to_remove:
                    continue
                col_j = [features[r][j] for r in range(n_samples)]
                corr = abs(StatisticalAssociator.pearson_correlation(col_i, col_j))
                if corr >= threshold:
                    to_remove.add(j)

        return [i for i in range(n_features) if i not in to_remove]


class FelixPreprocessingPipeline:
    """Complete preprocessing pipeline with Felix branding"""

    def __init__(self):
        self.scaler = None
        self.encoder = None
        self.imputer = None
        self.selected_features: List[int] = []

    def fit_transform_numerical(self, values: List[float],
                                method: str = "standardize") -> List[float]:
        """Transform numerical features"""
        if method == "minmax":
            return NumericalTransformer.min_max_transform(values)
        elif method == "log":
            return NumericalTransformer.log_transform(values)
        else:
            return NumericalTransformer.standardize_transform(values)

    def fit_transform_categorical(self, values: List[Any],
                                 method: str = "onehot") -> List[List[int]]:
        """Transform categorical features"""
        if method == "label":
            encoded, _ = CategoricalEncoder.label_encode(values)
            return [[e] for e in encoded]
        else:
            encoded, _ = CategoricalEncoder.one_hot_encode(values)
            return encoded


class HousingDataGenerator:
    """Generate synthetic housing data for demonstrations"""

    @staticmethod
    def generate(n_samples: int = 200, seed: int = 42) -> List[Dict[str, Any]]:
        """Generate synthetic housing dataset"""
        random.seed(seed)
        data = []

        for _ in range(n_samples):
            sqft = random.uniform(500, 5000)
            bedrooms = random.choice([1, 2, 3, 4, 5])
            age = random.uniform(0, 50)
            neighborhood = random.choice(["downtown", "suburbs", "rural"])
            has_pool = random.choice([True, False])

            sqft_with_missing = sqft if random.random() > 0.05 else None
            age_with_missing = age if random.random() > 0.08 else None

            price = (
                50 * sqft
                + 20000 * bedrooms
                - 1000 * age
                + (50000 if neighborhood == "downtown" else 10000 if neighborhood == "suburbs" else 0)
                + (15000 if has_pool else 0)
                + random.gauss(0, 20000)
            )

            data.append({
                "sqft": sqft_with_missing,
                "bedrooms": bedrooms,
                "age": age_with_missing,
                "neighborhood": neighborhood,
                "has_pool": has_pool,
                "price": price,
            })

        return data


def demonstrate_numerical_transforms():
    """Demonstrate numerical feature transformations"""
    print("=" * 65)
    print("  FELIX NUMERICAL TRANSFORMS")
    print("=" * 65)
    print()

    test_values = [10, 20, 30, 40, 50]

    print(f"  Original values: {test_values}")
    print()

    minmax = NumericalTransformer.min_max_transform(test_values)
    standardized = NumericalTransformer.standardize_transform(test_values)
    logged = NumericalTransformer.log_transform(test_values)

    print(f"  Min-Max scaled: {[round(v, 3) for v in minmax]}")
    print(f"  Standardized:  {[round(v, 3) for v in standardized]}")
    print(f"  Log transformed: {[round(v, 3) for v in logged]}")
    print()


def demonstrate_discretization():
    """Demonstrate binning/discretization"""
    print("=" * 65)
    print("  FELIX DISCRETIZATION")
    print("=" * 65)
    print()

    values = [10, 25, 35, 45, 55, 65, 75, 85, 95]

    print(f"  Original values: {values}")
    print()

    for n_bins in [3, 5]:
        binner = DiscretizationBinner(n_bins=n_bins)
        binned = binner.fit_transform(values)
        print(f"  {n_bins} bins: {binned}")
        print(f"    Edges: {[round(e, 1) for e in binner.bin_edges]}")
    print()


def demonstrate_polynomial_features():
    """Demonstrate polynomial feature generation"""
    print("=" * 65)
    print("  FELIX POLYNOMIAL FEATURES")
    print("=" * 65)
    print()

    row = [2.0, 3.0]

    poly_gen = PolynomialFeatureGenerator(degree=2)
    poly_features = poly_gen.transform(row)

    print(f"  Original features: {row}")
    print(f"  Polynomial (degree=2): {poly_features}")
    print(f"  Feature names: [x1, x2, x1², x2², x1*x2]")
    print()


def demonstrate_categorical_encoding():
    """Demonstrate various categorical encoding methods"""
    print("=" * 65)
    print("  FELIX CATEGORICAL ENCODING")
    print("=" * 65)
    print()

    categories = ["cat", "dog", "bird", "cat", "dog", "bird", "bird"]

    onehot, cat_labels = CategoricalEncoder.one_hot_encode(categories)
    labelenc, label_map = CategoricalEncoder.label_encode(categories)

    print(f"  Categories: {categories}")
    print()
    print(f"  One-hot encoding categories: {cat_labels}")
    print(f"  One-hot result: {onehot[:3]}...")
    print()
    print(f"  Label encoding map: {label_map}")
    print(f"  Label encoded: {labelenc}")
    print()


def demonstrate_target_encoding():
    """Demonstrate target encoding"""
    print("=" * 65)
    print("  FELIX TARGET ENCODING")
    print("=" * 65)
    print()

    neighborhoods = ["downtown", "suburbs", "rural", "downtown", "suburbs", "downtown", "rural"]
    prices = [250000, 150000, 100000, 280000, 160000, 240000, 95000]

    encoder = TargetMeanEncoder(smoothing=10)
    encoded = encoder.fit_transform(neighborhoods, prices)

    print(f"  Neighborhoods: {neighborhoods}")
    print(f"  Prices: {prices}")
    print()
    print(f"  Target-encoded means:")
    for cat, mean in sorted(encoder.category_means.items()):
        print(f"    {cat}: ${mean:,.0f}")
    print()


def demonstrate_text_features():
    """Demonstrate text vectorization"""
    print("=" * 65)
    print("  FELIX TEXT FEATURES")
    print("=" * 65)
    print()

    documents = [
        "large modern house with pool",
        "small cozy cottage near downtown",
        "spacious family home with large yard",
        "modern apartment downtown with view",
        "rustic cabin in rural area",
    ]

    count_vec, count_vocab = TextVectorizer.count_vectorize(documents)
    tfidf_vec, tfidf_vocab = TextVectorizer.tfidf_vectorize(documents)

    print(f"  Documents: {len(documents)}")
    print(f"  Count vectorizer vocab size: {len(count_vocab)}")
    print(f"  TF-IDF vocab size: {len(tfidf_vocab)}")
    print()

    print(f"  Doc 0 (original): '{documents[0]}'")
    print(f"  Non-zero count features: {sum(1 for v in count_vec[0] if v > 0)}")

    top_words = sorted(tfidf_vocab.keys(), key=lambda w: tfidf_vec[0][tfidf_vocab[w]], reverse=True)[:3]
    print(f"  Top TF-IDF words: {top_words}")
    print()


def demonstrate_missing_values():
    """Demonstrate missing value handling"""
    print("=" * 65)
    print("  FELIX MISSING VALUE HANDLING")
    print("=" * 65)
    print()

    values_with_missing = [100, None, 150, None, 200, 175, 125, None, 225]

    print(f"  Original values: {values_with_missing}")
    print(f"  Missing count: {sum(1 for v in values_with_missing if v is None)}")
    print()

    imputed_mean, mean_fill = MissingValueHandler.impute_with_mean(values_with_missing)
    imputed_median, median_fill = MissingValueHandler.impute_with_median(values_with_missing)
    imputed_mode, mode_fill = MissingValueHandler.impute_with_mode(values_with_missing)
    indicators = MissingValueHandler.add_missing_indicator(values_with_missing)

    print(f"  Imputed with mean ({mean_fill:.1f}): {imputed_mean}")
    print(f"  Imputed with median ({median_fill:.1f}): {imputed_median}")
    print(f"  Missing indicators: {indicators}")
    print()


def demonstrate_feature_selection():
    """Demonstrate feature selection methods"""
    print("=" * 65)
    print("  FELIX FEATURE SELECTION")
    print("=" * 65)
    print()

    housing = HousingDataGenerator.generate(200)

    sqft_raw = [d["sqft"] for d in housing]
    age_raw = [d["age"] for d in housing]
    prices = [d["price"] for d in housing]

    sqft_imputed, _ = MissingValueHandler.impute_with_median(sqft_raw)
    age_imputed, _ = MissingValueHandler.impute_with_mean(age_raw)

    sqft_scaled = NumericalTransformer.standardize_transform(sqft_imputed)
    age_scaled = NumericalTransformer.min_max_transform(age_imputed)

    sqft_indicator = MissingValueHandler.add_missing_indicator(sqft_raw)
    age_indicator = MissingValueHandler.add_missing_indicator(age_raw)

    neighborhoods = [d["neighborhood"] for d in housing]
    ohe, _ = CategoricalEncoder.one_hot_encode(neighborhoods)

    feature_matrix = [
        [sqft_scaled[i], age_scaled[i], float(sqft_indicator[i]), float(age_indicator[i])] + ohe[i]
        for i in range(len(housing))
    ]

    print(f"  Total features before selection: {len(feature_matrix[0])}")

    surviving_var = FeatureSelector.variance_threshold(feature_matrix, threshold=0.01)
    surviving_corr = FeatureSelector.remove_correlated_features(feature_matrix, threshold=0.9)

    print(f"  After variance threshold (0.01): {len(surviving_var)} features")
    print(f"  After correlation filter (0.9): {len(surviving_corr)} features")
    print()


def demonstrate_correlation_analysis():
    """Demonstrate statistical association measures"""
    print("=" * 65)
    print("  FELIX CORRELATION ANALYSIS")
    print("=" * 65)
    print()

    housing = HousingDataGenerator.generate(200)
    prices = [d["price"] for d in housing]

    sqft = [d["sqft"] if d["sqft"] is not None else 0 for d in housing]
    sqft_clean, _ = MissingValueHandler.impute_with_median([d["sqft"] for d in housing])
    sqft_scaled = NumericalTransformer.standardize_transform(sqft_clean)

    neighborhoods = [d["neighborhood"] for d in housing]
    _, label_map = CategoricalEncoder.label_encode(neighborhoods)
    neigh_encoded = [label_map[n] for n in neighborhoods]

    corr_sqft = StatisticalAssociator.pearson_correlation(sqft_scaled, prices)
    corr_neigh = StatisticalAssociator.pearson_correlation(neigh_encoded, prices)

    print(f"  Correlation with price:")
    print(f"    Square footage: {corr_sqft:.4f}")
    print(f"    Neighborhood type: {corr_neigh:.4f}")
    print()


def demonstrate_complete_pipeline():
    """Demonstrate complete preprocessing pipeline"""
    print("=" * 65)
    print("  FELIX COMPLETE PREPROCESSING PIPELINE")
    print("=" * 65)
    print()

    housing = HousingDataGenerator.generate(200)

    print(f"  Generated {len(housing)} housing records")
    print()

    sqft_raw = [d["sqft"] for d in housing]
    age_raw = [d["age"] for d in housing]
    prices = [d["price"] for d in housing]

    sqft_indicator = MissingValueHandler.add_missing_indicator(sqft_raw)
    age_indicator = MissingValueHandler.add_missing_indicator(age_raw)

    sqft_imputed, sqft_fill = MissingValueHandler.impute_with_median(sqft_raw)
    age_imputed, age_fill = MissingValueHandler.impute_with_mean(age_raw)

    sqft_scaled = NumericalTransformer.standardize_transform(sqft_imputed)
    age_scaled = NumericalTransformer.min_max_transform(age_imputed)

    print(f"  Missing values handled:")
    print(f"    sqft: {sum(sqft_indicator)} missing, filled with median ${sqft_fill:,.0f}")
    print(f"    age: {sum(age_indicator)} missing, filled with mean ${age_fill:,.0f}")
    print()

    neighborhoods = [d["neighborhood"] for d in housing]
    ohe, ohe_cats = CategoricalEncoder.one_hot_encode(neighborhoods)

    print(f"  Categorical encoding (one-hot): {ohe_cats}")
    print()

    binary_prices = [1 if p > sum(prices) / len(prices) else 0 for p in prices]
    mi_sqft = StatisticalAssociator.mutual_information_score(sqft_scaled, binary_prices)
    mi_age = StatisticalAssociator.mutual_information_score(age_scaled, binary_prices)

    print(f"  Mutual information with price class:")
    print(f"    Square footage: {mi_sqft:.4f}")
    print(f"    Age: {mi_age:.4f}")
    print()


def print_felix_summary():
    """Print summary of Felix feature engineering module"""
    print()
    print("=" * 65)
    print("  FELIX FEATURE ENGINEERING SUMMARY")
    print("=" * 65)
    print()
    print("  1. Numerical transforms: scale, standardize, log for different distributions.")
    print("  2. Discretization: convert continuous to categorical via binning.")
    print("  3. Polynomial features: capture non-linear relationships.")
    print("  4. Categorical encoding: one-hot for nominal, label for ordinal.")
    print("  5. Target encoding: use target statistics for supervised encoding.")
    print("  6. Text vectorization: count and TF-IDF for text data.")
    print("  7. Missing value handling: mean, median, mode imputation + indicators.")
    print("  8. Feature selection: variance threshold and correlation filtering.")
    print()


if __name__ == "__main__":
    demonstrate_numerical_transforms()
    demonstrate_discretization()
    demonstrate_polynomial_features()
    demonstrate_categorical_encoding()
    demonstrate_target_encoding()
    demonstrate_text_features()
    demonstrate_missing_values()
    demonstrate_feature_selection()
    demonstrate_correlation_analysis()
    demonstrate_complete_pipeline()
    print_felix_summary()