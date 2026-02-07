#!/usr/bin/env python3
"""
Felix Learning Platform - Statistical Analysis Module
Custom implementation for machine learning statistics
Author: Felix Learning
License: MIT

This module provides comprehensive statistical tools for ML analysis,
including hypothesis testing, Bayesian inference, and bootstrap methods.
"""

import math
import random
from typing import List, Dict, Tuple, Optional, Callable
from collections import Counter

# Set seed for reproducibility in educational examples
random.seed(2024)


class DatasetStatistics:
    """Handles all statistical computations for a dataset"""

    def __init__(self, observations: List[float]):
        self.observations = sorted(observations)
        self.n = len(observations)

    def compute_mean(self) -> float:
        """Arithmetic mean calculation"""
        return sum(self.observations) / self.n

    def compute_median(self) -> float:
        """Median with linear interpolation for even samples"""
        idx = self.n // 2
        if self.n % 2 == 0:
            return (self.observations[idx - 1] + self.observations[idx]) / 2
        return self.observations[idx]

    def compute_mode(self) -> float:
        """Most frequent value"""
        counts = Counter(self.observations)
        max_freq = max(counts.values())
        modes = [val for val, count in counts.items() if count == max_freq]
        return min(modes)  # Return smallest mode in case of tie

    def compute_variance(self, unbiased: bool = True) -> float:
        """Sample or population variance"""
        avg = self.compute_mean()
        squared_diffs = [(x - avg) ** 2 for x in self.observations]
        divisor = self.n - 1 if unbiased and self.n > 1 else self.n
        return sum(squared_diffs) / divisor

    def compute_std(self, unbiased: bool = True) -> float:
        """Standard deviation"""
        return math.sqrt(self.compute_variance(unbiased))

    def compute_quantile(self, q: float) -> float:
        """General quantile calculation using linear interpolation"""
        if q < 0 or q > 1:
            raise ValueError("Quantile must be between 0 and 1")
        index = q * (self.n - 1)
        lower = int(index)
        upper = lower + 1
        fraction = index - lower
        if upper >= self.n:
            return self.observations[-1]
        return self.observations[lower] * (1 - fraction) + self.observations[upper] * fraction

    def compute_iqr(self) -> float:
        """Interquartile range"""
        return self.compute_quantile(0.75) - self.compute_quantile(0.25)


class CorrelationAnalyzer:
    """Correlation and dependency measures"""

    @staticmethod
    def pearson_r(x_vals: List[float], y_vals: List[float]) -> float:
        """Pearson correlation coefficient"""
        n = len(x_vals)
        if n != len(y_vals) or n < 2:
            return 0.0

        x_mean = sum(x_vals) / n
        y_mean = sum(y_vals) / n

        numerator = sum((x_vals[i] - x_mean) * (y_vals[i] - y_mean) for i in range(n))
        x_denom = math.sqrt(sum((x - x_mean) ** 2 for x in x_vals))
        y_denom = math.sqrt(sum((y - y_mean) ** 2 for y in y_vals))

        if x_denom == 0 or y_denom == 0:
            return 0.0
        return numerator / (x_denom * y_denom)

    @staticmethod
    def rank_transform(values: List[float]) -> List[float]:
        """Rank transformation with average ties handling"""
        indexed = sorted(enumerate(values), key=lambda p: p[1])
        ranks = [0.0] * len(values)
        i = 0
        while i < len(indexed):
            j = i
            while j < len(indexed) - 1 and indexed[j + 1][1] == indexed[i][1]:
                j += 1
            average_rank = (i + j) / 2.0 + 1.0
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = average_rank
            i = j + 1
        return ranks

    @staticmethod
    def spearman_r(x_vals: List[float], y_vals: List[float]) -> float:
        """Spearman rank correlation"""
        rx = CorrelationAnalyzer.rank_transform(x_vals)
        ry = CorrelationAnalyzer.rank_transform(y_vals)
        return CorrelationAnalyzer.pearson_r(rx, ry)


class HypothesisTester:
    """Statistical hypothesis testing suite"""

    @staticmethod
    def t_stat_single(sample: List[float], hypothesized_mean: float) -> Dict:
        """One-sample t-test"""
        n = len(sample)
        sample_mean = sum(sample) / n
        sample_std = DatasetStatistics(sample).compute_std(unbiased=True)
        t_value = (sample_mean - hypothesized_mean) / (sample_std / math.sqrt(n))
        return {
            "t_value": t_value,
            "degrees_freedom": n - 1,
            "p_value": HypothesisTester._t_distribution_p(t_value, n - 1)
        }

    @staticmethod
    def t_stat_paired(sample_a: List[float], sample_b: List[float]) -> Dict:
        """Paired samples t-test"""
        differences = [a - b for a, b in zip(sample_a, sample_b)]
        n = len(differences)
        mean_diff = sum(differences) / n
        std_diff = DatasetStatistics(differences).compute_std(unbiased=True)
        if std_diff == 0:
            return {"t_value": 0.0, "df": n - 1, "p_value": 1.0}
        t_value = mean_diff / (std_diff / math.sqrt(n))
        return {
            "t_value": t_value,
            "df": n - 1,
            "p_value": HypothesisTester._t_distribution_p(t_value, n - 1)
        }

    @staticmethod
    def _t_distribution_p(t: float, df: int) -> float:
        """Approximate t-distribution p-value (two-tailed)"""
        x = df / (df + t * t)
        if t < 0:
            return HypothesisTester._beta incomplete(x, df / 2, 0.5)
        return 1.0 - HypothesisTester._beta incomplete(x, df / 2, 0.5)

    @staticmethod
    def _beta incomplete(x: float, a: float, b: float) -> float:
        """Regularized incomplete beta function approximation"""
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        steps = 200
        dt = x / steps
        total = 0.0
        for i in range(steps):
            t_val = (i + 0.5) * dt
            total += (t_val ** (a - 1)) * ((1 - t_val) ** (b - 1)) * dt
        beta_val = math.exp(math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b))
        if beta_val == 0:
            return 0.0
        return total / beta_val


class BayesianInference:
    """Bayesian statistical methods"""

    @staticmethod
    def bayes_factor(prior_odds: float, likelihood_ratio: float) -> float:
        """Calculate Bayes factor from prior odds and likelihood ratio"""
        return prior_odds * likelihood_ratio

    @staticmethod
    def posterior_probability(prior: float, likelihood_ratio: float) -> float:
        """Calculate posterior probability from prior and likelihood ratio"""
        odds = prior / (1 - prior)
        posterior_odds = odds * likelihood_ratio
        return posterior_odds / (1 + posterior_odds)

    @staticmethod
    def credible_interval(samples: List[float], credible_level: float = 0.95) -> Tuple[float, float]:
        """Highest density credible interval from posterior samples"""
        sorted_samples = sorted(samples)
        n = len(sorted_samples)
        lower_idx = int((1 - credible_level) * n / 2)
        upper_idx = int(n - (1 - credible_level) * n / 2)
        return (sorted_samples[lower_idx], sorted_samples[upper_idx])


class Resampler:
    """Bootstrap and Monte Carlo resampling methods"""

    def __init__(self, data: List[float], rng_seed: Optional[int] = None):
        self.data = data
        self.rng = random.Random(rng_seed)

    def bootstrap(self, statistic_func: Callable, iterations: int = 5000) -> Dict:
        """Bootstrap confidence interval for any statistic"""
        estimates = []
        n = len(self.data)
        for _ in range(iterations):
            resample = [self.data[self.rng.randint(0, n - 1)] for _ in range(n)]
            estimates.append(statistic_func(resample))
        estimates.sort()
        lower = int(0.025 * iterations)
        upper = int(0.975 * iterations)
        return {
            "point_estimate": statistic_func(self.data),
            "ci_low": estimates[lower],
            "ci_high": estimates[upper],
            "std_error": DatasetStatistics(estimates).compute_std(unbiased=False)
        }

    def permutation_test(self, group_a: List[float], group_b: List[float],
                        iterations: int = 5000) -> float:
        """Permutation test for two-sample equality"""
        observed_diff = abs(sum(group_a) / len(group_a) - sum(group_b) / len(group_b))
        combined = group_a + group_b
        n_a = len(group_a)
        count_extreme = 0

        for _ in range(iterations):
            self.rng.shuffle(combined)
            perm_a = combined[:n_a]
            perm_b = combined[n_a:]
            perm_diff = abs(sum(perm_a) / n_a - sum(perm_b) / len(perm_b))
            if perm_diff >= observed_diff:
                count_extreme += 1

        return count_extreme / iterations


def generate_gaussian_samples(sample_size: int, mu: float = 0.0,
                              sigma: float = 1.0) -> List[float]:
    """Generate Gaussian samples using Box-Muller transform"""
    samples = []
    for _ in range(sample_size // 2 + 1):
        u1 = random.random()
        u2 = random.random()
        while u1 == 0:
            u1 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        samples.extend([mu + sigma * z0, mu + sigma * z1])
    return samples[:sample_size]


def main():
    """Demonstrate all statistical methods"""
    print("=" * 65)
    print("  FELIX STATISTICAL ANALYSIS MODULE - DEMONSTRATION")
    print("=" * 65)

    # Generate test data
    test_data = generate_gaussian_samples(100, mu=50, sigma=10)

    # Basic statistics
    stats = DatasetStatistics(test_data)
    print("\n📊 BASIC DESCRIPTIVE STATISTICS")
    print("-" * 40)
    print(f"  Sample size:    {stats.n}")
    print(f"  Mean:            {stats.compute_mean():.4f}")
    print(f"  Median:          {stats.compute_median():.4f}")
    print(f"  Std deviation:    {stats.compute_std():.4f}")
    print(f"  Variance:        {stats.compute_variance():.4f}")
    print(f"  95th percentile: {stats.compute_quantile(0.95):.4f}")
    print(f"  IQR:             {stats.compute_iqr():.4f}")

    # Correlation example
    print("\n📈 CORRELATION ANALYSIS")
    print("-" * 40)
    x_data = list(range(1, 21))
    y_linear = [2 * x + random.gauss(0, 2) for x in x_data]
    y_curved = [x ** 2 + random.gauss(0, 10) for x in x_data]

    r_linear = CorrelationAnalyzer.pearson_r(x_data, y_linear)
    r_curved = CorrelationAnalyzer.pearson_r(x_data, y_curved)
    rho_linear = CorrelationAnalyzer.spearman_r(x_data, y_linear)
    rho_curved = CorrelationAnalyzer.spearman_r(x_data, y_curved)

    print(f"  Linear trend:    Pearson={r_linear:.4f}, Spearman={rho_linear:.4f}")
    print(f"  Curved trend:    Pearson={r_curved:.4f}, Spearman={rho_curved:.4f}")
    print("  Note: Pearson detects linear, Spearman detects monotonic")

    # Hypothesis testing
    print("\n🧪 HYPOTHESIS TESTING")
    print("-" * 40)
    sample1 = generate_gaussian_samples(30, mu=85, sigma=5)
    sample2 = generate_gaussian_samples(30, mu=88, sigma=5)
    test_result = HypothesisTester.t_stat_paired(sample1, sample2)
    print(f"  Testing difference between sample means")
    print(f"  t-statistic: {test_result['t_value']:.4f}")
    print(f"  p-value:     {test_result['p_value']:.4f}")
    print(f"  Significant: {'Yes' if test_result['p_value'] < 0.05 else 'No'} (alpha=0.05)")

    # Bayesian inference
    print("\n🔮 BAYESIAN INFERENCE")
    print("-" * 40)
    prior_prob = 0.3
    likelihood = 2.5  # Evidence strength
    posterior = BayesianInference.posterior_probability(prior_prob, likelihood)
    print(f"  Prior probability:     {prior_prob:.4f}")
    print(f"  Likelihood ratio:   {likelihood:.4f}")
    print(f"  Posterior probability: {posterior:.4f}")

    # Bootstrap
    print("\n🔄 BOOTSTRAP RESAMPLING")
    print("-" * 40)
    resampler = Resampler(test_data, rng_seed=42)
    boot_result = resampler.bootstrap(DatasetStatistics.compute_mean, iterations=2000)
    print(f"  Point estimate:     {boot_result['point_estimate']:.4f}")
    print(f"  95% CI:               [{boot_result['ci_low']:.4f}, {boot_result['ci_high']:.4f}]")
    print(f"  Standard error:       {boot_result['std_error']:.4f}")

    print("\n" + "=" * 65)
    print("  Module loaded successfully. Ready for ML statistics.")
    print("=" * 65)


if __name__ == "__main__":
    main()