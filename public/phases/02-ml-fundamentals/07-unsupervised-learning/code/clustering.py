#!/usr/bin/env python3
"""
Felix Learning Platform - Clustering Module
Unsupervised learning algorithms for data segmentation
Author: Felix Learning
License: MIT

This module implements clustering algorithms including K-means, DBSCAN,
GMM, and hierarchical clustering with modular architecture.
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Callable, Any
from dataclasses import dataclass


@dataclass
class DataPoint:
    """Represents a data point with coordinates and optional cluster assignment"""
    coordinates: List[float]
    cluster_id: Optional[int] = None
    is_noise: bool = False


class DistanceCalculator:
    """Compute distances between data points"""

    @staticmethod
    def euclidean(point_a: List[float], point_b: List[float]) -> float:
        """Compute Euclidean distance between two points"""
        squared_sum = sum((a - b) ** 2 for a, b in zip(point_a, point_b))
        return math.sqrt(squared_sum)

    @staticmethod
    def manhattan(point_a: List[float], point_b: List[float]) -> float:
        """Compute Manhattan distance between two points"""
        return sum(abs(a - b) for a, b in zip(point_a, point_b))


class CentroidTracker:
    """Track and update cluster centroids"""

    @staticmethod
    def compute(data: List[List[float]], cluster_ids: List[int],
               n_clusters: int, n_features: int) -> List[List[float]]:
        """Calculate centroids for each cluster"""
        cluster_points = [[] for _ in range(n_clusters)]

        for point, cluster_id in zip(data, cluster_ids):
            if cluster_id >= 0:
                cluster_points[cluster_id].append(point)

        centroids = []
        for points in cluster_points:
            if len(points) == 0:
                centroids.append([0.0] * n_features)
            else:
                centroid = [
                    sum(p[j] for p in points) / len(points)
                    for j in range(n_features)
                ]
                centroids.append(centroid)

        return centroids

    @staticmethod
    def has_converged(old_centroids: List[List[float]],
                      new_centroids: List[List[float]],
                      tolerance: float = 1e-6) -> bool:
        """Check if centroids have converged"""
        for old, new in zip(old_centroids, new_centroids):
            if DistanceCalculator.euclidean(old, new) >= tolerance:
                return False
        return True


class ClusterAssignment:
    """Assign points to nearest centroids"""

    @staticmethod
    def assign(data: List[List[float]], centroids: List[List[float]]) -> List[int]:
        """Assign each point to the nearest centroid"""
        assignments = []
        for point in data:
            distances = [
                DistanceCalculator.euclidean(point, centroid)
                for centroid in centroids
            ]
            nearest = distances.index(min(distances))
            assignments.append(nearest)
        return assignments

    @staticmethod
    def compute_inertia(data: List[List[float]], assignments: List[int],
                        centroids: List[List[float]]) -> float:
        """Compute within-cluster sum of squares (inertia)"""
        total = 0.0
        for point, cluster_id in zip(data, assignments):
            total += DistanceCalculator.euclidean(point, centroids[cluster_id]) ** 2
        return total


class InitialCentroidSelector:
    """Strategy for selecting initial centroids"""

    @staticmethod
    def random(data: List[List[float]], k: int, seed: int = 42) -> List[List[float]]:
        """Select k random points as initial centroids"""
        random.seed(seed)
        indices = random.sample(range(len(data)), k)
        return [list(data[i]) for i in indices]

    @staticmethod
    def kmeans_plusplus(data: List[List[float]], k: int,
                        seed: int = 42) -> List[List[float]]:
        """K-means++ initialization for better convergence"""
        random.seed(seed)
        n = len(data)

        centroids = [list(data[random.randint(0, n - 1)])]

        for _ in range(k - 1):
            distances = []
            for point in data:
                min_dist = min(
                    DistanceCalculator.euclidean(point, c)
                    for c in centroids
                )
                distances.append(min_dist ** 2)

            total = sum(distances)
            if total == 0:
                idx = random.randint(0, n - 1)
            else:
                probs = [d / total for d in distances]
                idx = random.choices(range(n), weights=probs, k=1)[0]

            centroids.append(list(data[idx]))

        return centroids


class FelixKMeansClusterer:
    """K-means clustering with Felix branding"""

    def __init__(self, n_clusters: int = 3, max_iterations: int = 100,
                 init_method: str = "random", seed: int = 42):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.init_method = init_method
        self.seed = seed

        self.centroids: List[List[float]] = []
        self.cluster_assignments: List[int] = []
        self.inertia: float = 0.0

    def fit(self, data: List[List[float]]) -> 'FelixKMeansClusterer':
        """Perform K-means clustering"""
        n_features = len(data[0])

        if self.init_method == "kmeans++":
            self.centroids = InitialCentroidSelector.kmeans_plusplus(
                data, self.n_clusters, self.seed
            )
        else:
            self.centroids = InitialCentroidSelector.random(
                data, self.n_clusters, self.seed
            )

        for iteration in range(self.max_iterations):
            old_centroids = [list(c) for c in self.centroids]

            self.cluster_assignments = ClusterAssignment.assign(data, self.centroids)

            self.centroids = CentroidTracker.compute(
                data, self.cluster_assignments, self.n_clusters, n_features
            )

            if CentroidTracker.has_converged(old_centroids, self.centroids):
                print(f"  Converged at iteration {iteration + 1}")
                break

        self.inertia = ClusterAssignment.compute_inertia(
            data, self.cluster_assignments, self.centroids
        )

        return self

    def predict(self, data: List[List[float]]) -> List[int]:
        """Predict cluster assignments for new data"""
        return ClusterAssignment.assign(data, self.centroids)

    def get_cluster_sizes(self) -> List[int]:
        """Get the number of points in each cluster"""
        sizes = [0] * self.n_clusters
        for assignment in self.cluster_assignments:
            sizes[assignment] += 1
        return sizes


class DBSCANNeighborFinder:
    """Find neighbors within epsilon radius"""

    def __init__(self, epsilon: float, min_samples: int):
        self.epsilon = epsilon
        self.min_samples = min_samples

    def find_neighbors(self, point_idx: int, data: List[List[float]]) -> List[int]:
        """Find all points within epsilon of the given point"""
        neighbors = []
        for i in range(len(data)):
            if DistanceCalculator.euclidean(data[point_idx], data[i]) <= self.epsilon:
                neighbors.append(i)
        return neighbors

    def expand_cluster(self, point_idx: int, neighbors: List[int],
                       labels: List[int], cluster_id: int,
                       data: List[List[float]], visited: List[bool]) -> None:
        """Expand cluster from a seed point"""
        labels[point_idx] = cluster_id
        seed_set = list(neighbors)
        seed_set.remove(point_idx)

        idx = 0
        while idx < len(seed_set):
            current = seed_set[idx]

            if not visited[current]:
                visited[current] = True
                current_neighbors = self.find_neighbors(current, data)

                if len(current_neighbors) >= self.min_samples:
                    for neighbor in current_neighbors:
                        if neighbor not in seed_set:
                            seed_set.append(neighbor)

            if labels[current] == -1:
                labels[current] = cluster_id

            idx += 1


class FelixDBSCANClusterer:
    """DBSCAN density-based clustering with Felix branding"""

    def __init__(self, epsilon: float = 0.5, min_samples: int = 5):
        self.epsilon = epsilon
        self.min_samples = min_samples
        self.cluster_labels: List[int] = []
        self.n_clusters: int = 0
        self.n_noise: int = 0

    def fit(self, data: List[List[float]]) -> 'FelixDBSCANClusterer':
        """Perform DBSCAN clustering"""
        n = len(data)
        self.cluster_labels = [-1] * n
        self.n_clusters = 0
        self.n_noise = 0
        visited = [False] * n

        neighbor_finder = DBSCANNeighborFinder(self.epsilon, self.min_samples)

        for i in range(n):
            if visited[i]:
                continue

            visited[i] = True
            neighbors = neighbor_finder.find_neighbors(i, data)

            if len(neighbors) < self.min_samples:
                self.cluster_labels[i] = -1
            else:
                self.n_clusters += 1
                neighbor_finder.expand_cluster(
                    i, neighbors, self.cluster_labels,
                    self.n_clusters, data, visited
                )

        self.n_noise = sum(1 for label in self.cluster_labels if label == -1)

        return self

    def predict(self) -> List[int]:
        """Return cluster labels (no prediction for new points in DBSCAN)"""
        return self.cluster_labels


class GaussianComponent:
    """Single Gaussian component for GMM"""

    def __init__(self, mean: List[float], variance: float, weight: float):
        self.mean = mean
        self.variance = variance
        self.weight = weight
        self.n_dims = len(mean)

    def compute_log_probability(self, point: List[float]) -> float:
        """Compute log probability under this Gaussian"""
        diff_squared = sum((p - m) ** 2 for p, m in zip(point, self.mean))
        log_coeff = -0.5 * self.n_dims * math.log(2 * math.pi * self.variance)
        log_exp = -0.5 * diff_squared / self.variance
        return log_coeff + log_exp

    def compute_probability(self, point: List[float]) -> float:
        """Compute probability under this Gaussian"""
        diff_squared = sum((p - m) ** 2 for p, m in zip(point, self.mean))
        coeff = 1.0 / ((2 * math.pi * self.variance) ** (self.n_dims / 2))
        exponent = -diff_squared / (2 * self.variance)
        capped_exp = max(exponent, -500)
        return coeff * math.exp(capped_exp)


class GMMParameterEstimator:
    """Estimate GMM parameters using EM algorithm"""

    @staticmethod
    def compute_responsibilities(data: List[List[float]],
                                 components: List[GaussianComponent]) -> List[List[float]]:
        """Compute posterior probabilities for each point"""
        n = len(data)
        k = len(components)
        responsibilities = []

        for i in range(n):
            probs = []
            for j in range(k):
                prob = components[j].weight * components[j].compute_probability(data[i])
                probs.append(prob)

            total = sum(probs)
            if total == 0:
                total = 1e-300

            responsibilities.append([p / total for p in probs])

        return responsibilities

    @staticmethod
    def update_parameters(data: List[List[float]],
                          responsibilities: List[List[float]],
                          old_components: List[GaussianComponent]) -> List[GaussianComponent]:
        """Update Gaussian component parameters"""
        n = len(data)
        k = len(old_components)
        d = len(data[0])

        new_components = []

        for j in range(k):
            r_sum = sum(responsibilities[i][j] for i in range(n))

            if r_sum < 1e-10:
                new_components.append(GaussianComponent(
                    old_components[j].mean,
                    old_components[j].variance,
                    old_components[j].weight
                ))
                continue

            new_weight = r_sum / n

            new_mean = [
                sum(responsibilities[i][j] * data[i][dim] for i in range(n)) / r_sum
                for dim in range(d)
            ]

            variance = sum(
                responsibilities[i][j] * sum((data[i][dim] - new_mean[dim]) ** 2 for dim in range(d))
                for i in range(n)
            ) / (r_sum * d)
            variance = max(variance, 1e-6)

            new_components.append(GaussianComponent(new_mean, variance, new_weight))

        return new_components


class FelixGMMClusterer:
    """Gaussian Mixture Model clustering with Felix branding"""

    def __init__(self, n_clusters: int = 3, max_iterations: int = 100,
                 seed: int = 42):
        self.n_clusters = n_clusters
        self.max_iterations = max_iterations
        self.seed = seed

        self.components: List[GaussianComponent] = []
        self.cluster_assignments: List[int] = []
        self.responsibilities: List[List[float]] = []

    def fit(self, data: List[List[float]]) -> 'FelixGMMClusterer':
        """Perform GMM clustering"""
        random.seed(self.seed)
        n = len(data)
        d = len(data[0])

        indices = random.sample(range(n), self.n_clusters)
        self.components = [
            GaussianComponent(
                mean=list(data[i]),
                variance=1.0,
                weight=1.0 / self.n_clusters
            )
            for i in indices
        ]

        for iteration in range(self.max_iterations):
            old_means = [list(c.mean) for c in self.components]

            self.responsibilities = GMMParameterEstimator.compute_responsibilities(
                data, self.components
            )

            self.components = GMMParameterEstimator.update_parameters(
                data, self.responsibilities, self.components
            )

            shift = sum(
                DistanceCalculator.euclidean(old_means[j], self.components[j].mean)
                for j in range(self.n_clusters)
            )

            if shift < 1e-6:
                print(f"  GMM converged at iteration {iteration + 1}")
                break

        self.cluster_assignments = [
            responsibilities.index(max(responsibilities))
            for responsibilities in self.responsibilities
        ]

        return self

    def predict(self) -> List[int]:
        """Return cluster assignments"""
        return self.cluster_assignments

    def predict_proba(self, point: List[float]) -> List[float]:
        """Return probability of point belonging to each cluster"""
        probs = []
        for component in self.components:
            probs.append(component.weight * component.compute_probability(point))
        total = sum(probs)
        if total == 0:
            return [1.0 / self.n_clusters] * self.n_clusters
        return [p / total for p in probs]


class DistanceLinkage:
    """Compute distances between clusters for hierarchical clustering"""

    @staticmethod
    def single_linkage(cluster_a: List[int], cluster_b: List[int],
                      data: List[List[float]]) -> float:
        """Single linkage: minimum distance between any two points"""
        return min(
            DistanceCalculator.euclidean(data[i], data[j])
            for i in cluster_a
            for j in cluster_b
        )

    @staticmethod
    def complete_linkage(cluster_a: List[int], cluster_b: List[int],
                        data: List[List[float]]) -> float:
        """Complete linkage: maximum distance between any two points"""
        return max(
            DistanceCalculator.euclidean(data[i], data[j])
            for i in cluster_a
            for j in cluster_b
        )

    @staticmethod
    def average_linkage(cluster_a: List[int], cluster_b: List[int],
                        data: List[List[float]]) -> float:
        """Average linkage: mean distance between all point pairs"""
        total = sum(
            DistanceCalculator.euclidean(data[i], data[j])
            for i in cluster_a
            for j in cluster_b
        )
        return total / (len(cluster_a) * len(cluster_b))

    @staticmethod
    def ward_linkage(cluster_a: List[int], cluster_b: List[int],
                     data: List[List[float]]) -> float:
        """Ward linkage: increase in variance from merging"""
        merged = cluster_a + cluster_b

        centroid_merged = [
            sum(data[i][d] for i in merged) / len(merged)
            for d in range(len(data[0]))
        ]
        centroid_a = [
            sum(data[i][d] for i in cluster_a) / len(cluster_a)
            for d in range(len(data[0]))
        ]
        centroid_b = [
            sum(data[i][d] for i in cluster_b) / len(cluster_b)
            for d in range(len(data[0]))
        ]

        var_merged = sum(
            DistanceCalculator.euclidean(data[i], centroid_merged) ** 2
            for i in merged
        )
        var_a = sum(
            DistanceCalculator.euclidean(data[i], centroid_a) ** 2
            for i in cluster_a
        )
        var_b = sum(
            DistanceCalculator.euclidean(data[i], centroid_b) ** 2
            for i in cluster_b
        )

        return var_merged - var_a - var_b


class FelixHierarchicalClusterer:
    """Agglomerative hierarchical clustering with Felix branding"""

    def __init__(self, n_clusters: int = 3, linkage: str = "ward"):
        self.n_clusters = n_clusters
        self.linkage = linkage
        self.cluster_labels: List[int] = []
        self.merge_history: List[Tuple[int, int, float, int]] = []

    def fit(self, data: List[List[float]]) -> 'FelixHierarchicalClusterer':
        """Perform agglomerative hierarchical clustering"""
        n = len(data)
        cluster_map = {i: [i] for i in range(n)}
        active_clusters = list(range(n))

        if self.linkage == "single":
            linkage_func = DistanceLinkage.single_linkage
        elif self.linkage == "complete":
            linkage_func = DistanceLinkage.complete_linkage
        elif self.linkage == "average":
            linkage_func = DistanceLinkage.average_linkage
        else:
            linkage_func = DistanceLinkage.ward_linkage

        next_id = n

        while len(active_clusters) > self.n_clusters:
            best_distance = float("inf")
            best_pair = None

            for idx_a in range(len(active_clusters)):
                for idx_b in range(idx_a + 1, len(active_clusters)):
                    c_a = active_clusters[idx_a]
                    c_b = active_clusters[idx_b]
                    dist = linkage_func(cluster_map[c_a], cluster_map[c_b], data)

                    if dist < best_distance:
                        best_distance = dist
                        best_pair = (c_a, c_b)

            c_a, c_b = best_pair
            cluster_map[next_id] = cluster_map[c_a] + cluster_map[c_b]
            self.merge_history.append((c_a, c_b, best_distance, len(cluster_map[next_id])))

            active_clusters.remove(c_a)
            active_clusters.remove(c_b)
            active_clusters.append(next_id)
            next_id += 1

        self.cluster_labels = [0] * n
        for cluster_label, cluster_id in enumerate(active_clusters):
            for point_idx in cluster_map[cluster_id]:
                self.cluster_labels[point_idx] = cluster_label

        return self

    def get_dendrogram_data(self) -> List[Tuple[int, int, float, int]]:
        """Return merge history for dendrogram visualization"""
        return self.merge_history


class ClusterQualityMetrics:
    """Evaluate clustering quality"""

    @staticmethod
    def silhouette_coefficient(data: List[List[float]],
                               assignments: List[int]) -> float:
        """Compute average silhouette coefficient"""
        n = len(data)
        if n < 2:
            return 0.0

        cluster_map = {}
        for i, cluster_id in enumerate(assignments):
            cluster_map.setdefault(cluster_id, []).append(i)

        if len(cluster_map) < 2:
            return 0.0

        scores = []

        for i in range(n):
            own_cluster = assignments[i]
            own_members = [j for j in cluster_map[own_cluster] if j != i]

            if len(own_members) == 0:
                scores.append(0.0)
                continue

            a = sum(
                DistanceCalculator.euclidean(data[i], data[j])
                for j in own_members
            ) / len(own_members)

            b = float("inf")
            for cluster_id, members in cluster_map.items():
                if cluster_id == own_cluster:
                    continue
                avg_dist = sum(
                    DistanceCalculator.euclidean(data[i], data[j])
                    for j in members
                ) / len(members)
                b = min(b, avg_dist)

            if max(a, b) == 0:
                scores.append(0.0)
            else:
                scores.append((b - a) / max(a, b))

        return sum(scores) / len(scores)

    @staticmethod
    def davies_bouldin_index(data: List[List[float]],
                           assignments: List[int]) -> float:
        """Compute Davies-Bouldin index (lower is better)"""
        cluster_map = {}
        for i, cluster_id in enumerate(assignments):
            cluster_map.setdefault(cluster_id, []).append(i)

        n_clusters = len(cluster_map)
        if n_clusters <= 1:
            return 0.0

        centroids = []
        for cluster_id in cluster_map:
            points = [data[i] for i in cluster_map[cluster_id]]
            centroid = [
                sum(p[j] for p in points) / len(points)
                for j in range(len(data[0]))
            ]
            centroids.append((cluster_id, centroid))

        intra_dists = []
        for cluster_id, centroid in centroids:
            points = [data[i] for i in cluster_map[cluster_id]]
            if len(points) > 0:
                avg_dist = sum(
                    DistanceCalculator.euclidean(point, centroid)
                    for point in points
                ) / len(points)
                intra_dists.append((cluster_id, avg_dist))
            else:
                intra_dists.append((cluster_id, 0.0))

        db_score = 0.0
        for i in range(n_clusters):
            max_ratio = 0.0
            for j in range(n_clusters):
                if i == j:
                    continue
                centroid_i = centroids[i][1]
                centroid_j = centroids[j][1]
                inter_dist = DistanceCalculator.euclidean(centroid_i, centroid_j)

                if inter_dist > 0:
                    ratio = (intra_dists[i][1] + intra_dists[j][1]) / inter_dist
                    max_ratio = max(max_ratio, ratio)

            db_score += max_ratio

        return db_score / n_clusters


def generate_blob_data(centers: List[List[float]], n_per_cluster: int = 50,
                      spread: float = 0.5, seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate blob-like clusters for testing"""
    random.seed(seed)
    data, true_labels = [], []

    for label, (cx, cy) in enumerate(centers):
        for _ in range(n_per_cluster):
            x = cx + random.gauss(0, spread)
            y = cy + random.gauss(0, spread)
            data.append([x, y])
            true_labels.append(label)

    return data, true_labels


def generate_moon_data(n_samples: int = 200, noise: float = 0.1,
                       seed: int = 42) -> Tuple[List[List[float]], List[int]]:
    """Generate moon-shaped clusters"""
    random.seed(seed)
    data, labels = [], []
    n_half = n_samples // 2

    for i in range(n_half):
        angle = math.pi * i / n_half
        x = math.cos(angle) + random.gauss(0, noise)
        y = math.sin(angle) + random.gauss(0, noise)
        data.append([x, y])
        labels.append(0)

    for i in range(n_half):
        angle = math.pi * i / n_half
        x = 1 - math.cos(angle) + random.gauss(0, noise)
        y = 1 - math.sin(angle) - 0.5 + random.gauss(0, noise)
        data.append([x, y])
        labels.append(1)

    return data, labels


def demonstrate_felix_kmeans():
    """Demonstrate Felix K-means clustering"""
    print("=" * 65)
    print("  FELIX K-MEANS CLUSTERING")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    print(f"  Dataset: {len(data)} points, 3 true clusters")
    print()

    clusterer = FelixKMeansClusterer(n_clusters=3, max_iterations=100, seed=42)
    clusterer.fit(data)

    print(f"  Learned centroids: {[[round(c, 2) for c in cent] for cent in clusterer.centroids]}")
    print(f"  Cluster sizes: {clusterer.get_cluster_sizes()}")
    print(f"  Inertia: {clusterer.inertia:.2f}")

    silhouette = ClusterQualityMetrics.silhouette_coefficient(data, clusterer.cluster_assignments)
    print(f"  Silhouette score: {silhouette:.4f}")
    print()


def demonstrate_elbow_method():
    """Demonstrate elbow method for choosing K"""
    print("=" * 65)
    print("  FELIX ELBOW METHOD")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    print(f"  {'K':>4s}  {'Inertia':>10s}")
    print(f"  {'-' * 4}  {'-' * 10}")

    for k in range(1, 7):
        clusterer = FelixKMeansClusterer(n_clusters=k, seed=42)
        clusterer.fit(data)
        print(f"  {k:>4d}  {clusterer.inertia:>10.2f}")

    print()


def demonstrate_felix_dbscan():
    """Demonstrate Felix DBSCAN clustering"""
    print("=" * 65)
    print("  FELIX DBSCAN DENSITY-BASED CLUSTERING")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    print(f"  Dataset: {len(data)} points, 3 true clusters")
    print()

    clusterer = FelixDBSCANClusterer(epsilon=1.5, min_samples=5)
    clusterer.fit(data)

    print(f"  Found {clusterer.n_clusters} clusters, {clusterer.n_noise} noise points")
    print()


def demonstrate_dbscan_on_moons():
    """Demonstrate DBSCAN on non-convex clusters"""
    print("=" * 65)
    print("  FELIX DBSCAN ON MOON-SHAPED DATA")
    print("=" * 65)
    print()

    data, labels = generate_moon_data(n_samples=200, noise=0.1)

    print(f"  Moon-shaped data: {len(data)} points, 2 crescents")
    print()

    clusterer = FelixDBSCANClusterer(epsilon=0.3, min_samples=5)
    clusterer.fit(data)

    print(f"  DBSCAN found {clusterer.n_clusters} clusters, {clusterer.n_noise} noise points")
    print()

    kmeans = FelixKMeansClusterer(n_clusters=2, seed=42)
    kmeans.fit(data)
    silhouette_km = ClusterQualityMetrics.silhouette_coefficient(data, kmeans.cluster_assignments)

    print(f"  K-means silhouette on moons: {silhouette_km:.4f}")
    print(f"  (K-means fails because moons are not spherical)")
    print()


def demonstrate_felix_gmm():
    """Demonstrate Felix GMM clustering"""
    print("=" * 65)
    print("  FELIX GAUSSIAN MIXTURE MODEL")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    print(f"  Dataset: {len(data)} points, 3 true clusters")
    print()

    clusterer = FelixGMMClusterer(n_clusters=3, max_iterations=100, seed=42)
    clusterer.fit(data)

    print(f"  Learned means: {[[round(m, 2) for m in comp.mean] for comp in clusterer.components]}")
    print(f"  Learned weights: {[round(w, 3) for w in [c.weight for c in clusterer.components]]}")

    silhouette = ClusterQualityMetrics.silhouette_coefficient(data, clusterer.cluster_assignments)
    print(f"  Silhouette score: {silhouette:.4f}")
    print()


def demonstrate_felix_hierarchical():
    """Demonstrate Felix hierarchical clustering"""
    print("=" * 65)
    print("  FELIX HIERARCHICAL CLUSTERING")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    small_data = data[:30]

    print(f"  Dataset: {len(small_data)} points (subset for visualization)")
    print()

    clusterer = FelixHierarchicalClusterer(n_clusters=3, linkage="ward")
    clusterer.fit(small_data)

    silhouette = ClusterQualityMetrics.silhouette_coefficient(small_data, clusterer.cluster_labels)
    print(f"  Silhouette score: {silhouette:.4f}")

    print("  Last 3 merges:")
    for merge in clusterer.merge_history[-3:]:
        print(f"    Merge {merge[0]} + {merge[1]} -> dist={merge[2]:.2f}, size={merge[3]}")
    print()


def demonstrate_anomaly_detection():
    """Demonstrate anomaly detection with DBSCAN"""
    print("=" * 65)
    print("  FELIX ANOMALY DETECTION WITH DBSCAN")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    anomaly_points = [[20.0, 20.0], [-5.0, -5.0], [15.0, 0.0]]
    data.extend(anomaly_points)

    print(f"  Added 3 anomalies to the dataset")
    print()

    clusterer = FelixDBSCANClusterer(epsilon=1.5, min_samples=5)
    clusterer.fit(data)

    anomalies = [
        data[i] for i in range(len(clusterer.cluster_labels))
        if clusterer.cluster_labels[i] == -1
    ]

    print(f"  Detected {len(anomalies)} anomalies:")
    for point in anomalies[-3:]:
        print(f"    Point: [{point[0]:.2f}, {point[1]:.2f}]")
    print()


def demonstrate_quality_metrics():
    """Compare quality metrics across algorithms"""
    print("=" * 65)
    print("  FELIX CLUSTERING QUALITY COMPARISON")
    print("=" * 65)
    print()

    centers = [[2, 2], [8, 3], [5, 8]]
    data, true_labels = generate_blob_data(centers, n_per_cluster=50, spread=0.8)

    algorithms = {
        "K-Means": FelixKMeansClusterer(n_clusters=3, seed=42),
        "GMM": FelixGMMClusterer(n_clusters=3, seed=42),
        "Hierarchical": FelixHierarchicalClusterer(n_clusters=3, linkage="ward"),
    }

    print(f"  {'Algorithm':<15s}  {'Silhouette':>12s}  {'DB Index':>10s}")
    print(f"  {'-' * 15}  {'-' * 12}  {'-' * 10}")

    for name, clusterer in algorithms.items():
        clusterer.fit(data)
        assignments = clusterer.cluster_labels

        silhouette = ClusterQualityMetrics.silhouette_coefficient(data, assignments)
        db_index = ClusterQualityMetrics.davies_bouldin_index(data, assignments)

        print(f"  {name:<15s}  {silhouette:>12.4f}  {db_index:>10.4f}")

    print()


def print_felix_summary():
    """Print summary of Felix clustering module"""
    print()
    print("=" * 65)
    print("  FELIX CLUSTERING SUMMARY")
    print("=" * 65)
    print()
    print("  1. K-means: fast, works well for spherical clusters.")
    print("  2. DBSCAN: density-based, finds arbitrary shapes, detects outliers.")
    print("  3. GMM: probabilistic, soft assignments, handles elliptical clusters.")
    print("  4. Hierarchical: builds dendrogram, no need to pre-specify K.")
    print("  5. Silhouette score: measures cluster cohesion vs separation.")
    print("  6. Davies-Bouldin index: measures intra-cluster vs inter-cluster distances.")
    print("  7. Elbow method: choose K by looking at inertia curve.")
    print("  8. DBSCAN is great for anomaly detection.")
    print()


if __name__ == "__main__":
    demonstrate_felix_kmeans()
    demonstrate_elbow_method()
    demonstrate_felix_dbscan()
    demonstrate_felix_gmm()
    demonstrate_felix_hierarchical()
    demonstrate_dbscan_on_moons()
    demonstrate_anomaly_detection()
    demonstrate_quality_metrics()
    print_felix_summary()