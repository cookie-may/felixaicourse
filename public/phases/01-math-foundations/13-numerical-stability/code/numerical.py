#!/usr/bin/env python3
"""
Felix Learning Platform - Numerical Stability Module
Precision-safe implementations for machine learning operations
Author: Felix Learning
License: MIT

This module demonstrates numerical stability issues commonly encountered
in ML computations and provides robust solutions.
"""

import math
from typing import List, Callable, Tuple, Optional
from enum import Enum


class StabilityMode(Enum):
    """Computation stability modes"""
    NAIVE = "naive"
    STABLE = "stable"
    ROBUST = "robust"


class FloatingPointAnalyzer:
    """Analyze and demonstrate floating point precision issues"""

    EPSILON = 1e-10
    MAX_LOG = 700.0
    MIN_LOG = -700.0

    @staticmethod
    def check_overflow(value: float, threshold: float = 1e10) -> bool:
        """Detect potential overflow conditions"""
        return abs(value) > threshold

    @staticmethod
    def check_underflow(value: float, threshold: float = 1e-10) -> bool:
        """Detect potential underflow conditions"""
        return 0 < abs(value) < threshold

    @staticmethod
    def relative_error(a: float, b: float) -> float:
        """Compute relative error between two values"""
        denom = max(abs(a), abs(b), FloatingPointAnalyzer.EPSILON)
        return abs(a - b) / denom


class SoftmaxComputer:
    """Numerically stable softmax implementations"""

    @staticmethod
    def compute_naive(logits: List[float]) -> List[float]:
        """Naive softmax - prone to overflow with large logits"""
        max_logit = max(logits) if logits else 0
        exps = [math.exp(z - max_logit) for z in logits]
        total = sum(exps)
        return [e / total for e in exps] if total > 0 else [0] * len(logits)

    @staticmethod
    def compute_log_space(logits: List[float]) -> List[float]:
        """Log-space softmax for numerical stability"""
        if not logits:
            return []
        shift = max(logits)
        log_shifted = [z - shift for z in logits]
        log_sum = shift + math.log(sum(math.exp(z) for z in log_shifted))
        return [z - log_sum for z in logits]

    @staticmethod
    def compute_gradient(probs: List[float], target_idx: int) -> List[float]:
        """Compute softmax gradient for backpropagation"""
        grad = probs[:]
        grad[target_idx] -= 1.0
        return grad


class LogSumExp:
    """Log-sum-exp operations with stability guarantees"""

    @staticmethod
    def naive(values: List[float]) -> float:
        """Naive log-sum-exp - overflow risk"""
        return math.log(sum(math.exp(v) for v in values))

    @staticmethod
    def stable(values: List[float]) -> float:
        """Stable log-sum-exp using maximum subtraction"""
        if not values:
            return float('-inf')
        max_val = max(values)
        if max_val > FloatingPointAnalyzer.MAX_LOG:
            return max_val
        return max_val + math.log(sum(math.exp(v - max_val) for v in values))

    @staticmethod
    def pairwise(values: List[float]) -> float:
        """Pairwise log-sum-exp for better stability"""
        if not values:
            return float('-inf')
        result = values[0]
        for v in values[1:]:
            if result > v:
                result = result + math.log(1 + math.exp(v - result))
            else:
                result = v + math.log(1 + math.exp(result - v))
        return result


class CrossEntropyCalculator:
    """Categorical cross-entropy with numerical safeguards"""

    @staticmethod
    def compute(probabilities: List[float], target_class: int) -> float:
        """Compute cross-entropy loss from probabilities"""
        if target_class < 0 or target_class >= len(probabilities):
            raise IndexError("Target class out of bounds")
        p = probabilities[target_class]
        if p < FloatingPointAnalyzer.EPSILON:
            return -math.log(FloatingPointAnalyzer.EPSILON)
        return -math.log(p)

    @staticmethod
    def from_logits(logits: List[float], target_class: int) -> float:
        """Compute cross-entropy directly from logits (log-sum-exp stable)"""
        max_logit = max(logits)
        shifted = [z - max_logit for z in logits]
        log_sum_exp = max_logit + math.log(sum(math.exp(z) for z in shifted))
        return log_sum_exp - logits[target_class]


class SigmoidComputer:
    """Sigmoid activation with overflow protection"""

    @staticmethod
    def basic(x: float) -> float:
        """Basic sigmoid implementation"""
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def safe(x: float) -> float:
        """Overflow-safe sigmoid using branch optimization"""
        if x > 20:
            return 1.0 - 1e-15
        if x < -20:
            return 1e-15
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def stable(x: float) -> float:
        """Stable sigmoid using symmetry property"""
        if x >= 0:
            z = math.exp(-x)
            return 1.0 / (1.0 + z)
        else:
            z = math.exp(x)
            return z / (1.0 + z)

    @staticmethod
    def gradient(x: float) -> float:
        """Sigmoid gradient at given input"""
        s = SigmoidComputer.stable(x)
        return s * (1.0 - s)


class BinaryCrossEntropy:
    """Binary cross-entropy with log-space stability"""

    @staticmethod
    def compute(label: float, prediction: float) -> float:
        """Standard binary cross-entropy"""
        eps = FloatingPointAnalyzer.EPSILON
        p = max(eps, min(1 - eps, prediction))
        return -(label * math.log(p) + (1 - label) * math.log(1 - p))

    @staticmethod
    def from_logit(label: float, logit: float) -> float:
        """Logit-space BCE to avoid numerical issues"""
        if label == 1:
            return BinaryCrossEntropy._softplus(-logit)
        else:
            return BinaryCrossEntropy._softplus(logit)

    @staticmethod
    def _softplus(x: float) -> float:
        """Numerically stable softplus: log(1 + exp(x))"""
        if x > 20:
            return x
        return math.log(1.0 + math.exp(x))


class GradientChecker:
    """Verify analytical gradients against numerical approximations"""

    def __init__(self, tolerance: float = 1e-6):
        self.tolerance = tolerance

    def numerical_gradient(
        self,
        func: Callable[[List[float]], float],
        point: List[float],
        epsilon: float = 1e-5
    ) -> List[float]:
        """Compute numerical gradient using central differences"""
        n = len(point)
        grad = [0.0] * n
        for i in range(n):
            point_plus = point[:]
            point_minus = point[:]
            point_plus[i] += epsilon
            point_minus[i] -= epsilon
            grad[i] = (func(point_plus) - func(point_minus)) / (2 * epsilon)
        return grad

    def verify(
        self,
        analytical_grad: List[float],
        numerical_grad: List[float],
        verbose: bool = True
    ) -> bool:
        """Compare analytical and numerical gradients"""
        all_ok = True
        for i, (a, n) in enumerate(zip(analytical_grad, numerical_grad)):
            rel_error = FloatingPointAnalyzer.relative_error(a, n)
            status = rel_error < self.tolerance
            if not status:
                all_ok = False
            if verbose:
                symbol = "✓" if status else "✗"
                print(f"  [{symbol}] param[{i}]: "
                      f"analytical={a:.8f}, numerical={n:.8f}, "
                      f"rel_error={rel_error:.2e}")
        return all_ok


class GradientClipper:
    """Gradient clipping utilities for training stability"""

    @staticmethod
    def by_value(gradients: List[float], max_abs: float) -> List[float]:
        """Clip gradients by absolute value"""
        return [max(-max_abs, min(max_abs, g)) for g in gradients]

    @staticmethod
    def by_norm(gradients: List[float], max_norm: float) -> List[float]:
        """Clip gradients by L2 norm"""
        total_norm = math.sqrt(sum(g ** 2 for g in gradients))
        if total_norm > max_norm:
            scale = max_norm / total_norm
            return [g * scale for g in gradients]
        return gradients

    @staticmethod
    def adaptive(gradients: List[float], max_norm: float,
                  threshold: float = 1.0) -> List[float]:
        """Adaptive gradient clipping based on magnitude"""
        grad_norm = math.sqrt(sum(g ** 2 for g in gradients))
        if grad_norm > max_norm * threshold:
            return GradientClipper.by_norm(gradients, max_norm)
        return gradients


def run_stability_demo():
    """Demonstrate numerical stability concepts"""
    print("=" * 60)
    print("  FELIX NUMERICAL STABILITY DEMONSTRATION")
    print("=" * 60)

    # Test log-sum-exp stability
    print("\n📊 Log-Sum-Exp Stability Test")
    print("-" * 40)
    large_values = [1000.0, 1001.0, 1002.0, 1003.0]
    try:
        naive_result = LogSumExp.naive(large_values)
        print(f"  Naive result: {naive_result}")
    except OverflowError:
        print("  Naive: OVERFLOW!")

    stable_result = LogSumExp.stable(large_values)
    print(f"  Stable result: {stable_result:.4f}")

    # Test softmax with extreme values
    print("\n📊 Softmax with Extreme Logits")
    print("-" * 40)
    extreme_logits = [1000.0, 1001.0, 1002.0]
    probs = SoftmaxComputer.compute_naive(extreme_logits)
    print(f"  Input: {extreme_logits}")
    print(f"  Output probabilities: {[f'{p:.6f}' for p in probs]}")
    print(f"  Sum: {sum(probs):.10f}")

    # Test sigmoid stability
    print("\n📊 Sigmoid Stability Across Ranges")
    print("-" * 40)
    test_values = [-100, -50, -10, -5, 0, 5, 10, 50, 100]
    for val in test_values:
        basic = SigmoidComputer.basic(val)
        safe = SigmoidComputer.safe(val)
        stable = SigmoidComputer.stable(val)
        print(f"  x={val:5d}: basic={basic:.12f}, stable={stable:.12f}")

    # Test gradient checking
    print("\n📊 Gradient Verification")
    print("-" * 40)

    def sample_function(weights: List[float]) -> float:
        """Sample function for gradient checking"""
        return (weights[0] ** 2 + weights[1] ** 2 + weights[0] * weights[1])

    def analytical_gradient(weights: List[float]) -> List[float]:
        """Analytical gradient for sample function"""
        return [2 * weights[0] + weights[1], 2 * weights[1] + weights[0]]

    test_point = [1.0, 2.0]
    checker = GradientChecker(tolerance=1e-5)
    numerical = checker.numerical_gradient(sample_function, test_point)
    analytical = analytical_gradient(test_point)

    print(f"  Testing at weights = {test_point}")
    print(f"  Function value: {sample_function(test_point):.6f}")
    checker.verify(analytical, numerical, verbose=True)

    # Test gradient clipping
    print("\n📊 Gradient Clipping Demonstration")
    print("-" * 40)
    sample_grads = [3.0, 1.5, 2.5, 0.5, 4.0]
    print(f"  Original gradients: {sample_grads}")
    print(f"  Original norm: {math.sqrt(sum(g**2 for g in sample_grads)):.4f}")

    clipped_by_val = GradientClipper.by_value(sample_grads, max_abs=2.0)
    clipped_by_norm = GradientClipper.by_norm(sample_grads, max_norm=3.0)
    print(f"  Clipped (value<2):  {clipped_by_val}")
    print(f"  Clipped (norm<3):   {clipped_by_norm}")

    print("\n" + "=" * 60)
    print("  Numerical stability analysis complete!")
    print("=" * 60)


if __name__ == "__main__":
    run_stability_demo()