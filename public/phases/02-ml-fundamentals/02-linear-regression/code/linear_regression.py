#!/usr/bin/env python3
"""
Felix Learning Platform - Linear Regression Module
Custom implementation of linear regression with multiple variants
Author: Felix Learning
License: MIT

This module provides comprehensive linear regression implementations
including gradient descent, normal equations, and regularization.
"""

import random
import math
from typing import List, Tuple, Callable, Optional, Dict


class RegressionModel:
    """Base class for regression models"""

    def __init__(self, coefficient: float = 0.0, intercept: float = 0.0):
        self.slope = coefficient
        self.intercept = intercept

    def apply(self, feature: float) -> float:
        """Compute prediction for single feature"""
        return self.slope * feature + self.intercept


class GradientDescentSolver:
    """Finds optimal coefficients using iterative gradient descent"""

    def __init__(self, step_size: float = 0.01):
        self.learning_rate = step_size
        self.residual_history: List[float] = []

    def optimize(
        self,
        inputs: List[float],
        targets: List[float],
        weight: float,
        bias: float,
        iterations: int = 1000
    ) -> Tuple[float, float]:
        """Run gradient descent optimization"""
        samples = len(targets)

        for iteration in range(iterations):
            predictions = [weight * x + bias for x in inputs]
            residuals = [p - t for p, t in zip(predictions, targets)]

            weight_gradient = (2.0 / samples) * sum(r * x for r, x in zip(residuals, inputs))
            bias_gradient = (2.0 / samples) * sum(residuals)

            weight -= self.learning_rate * weight_gradient
            bias -= self.learning_rate * bias_gradient

            cost = sum(r ** 2 for r in residuals) / samples
            self.residual_history.append(cost)

        return weight, bias


class DirectSolutionFinder:
    """Closed-form solution using normal equations"""

    @staticmethod
    def solve(inputs: List[float], targets: List[float]) -> Tuple[float, float]:
        """Compute optimal coefficients directly"""
        count = len(inputs)
        x_avg = sum(inputs) / count
        y_avg = sum(targets) / count

        covariance = sum((inputs[i] - x_avg) * (targets[i] - y_avg) for i in range(count))
        variance = sum((inputs[i] - x_avg) ** 2 for i in range(count))

        if variance == 0:
            return 0.0, y_avg

        coefficient = covariance / variance
        intercept = y_avg - coefficient * x_avg

        return coefficient, intercept


class MultivariateRegressor:
    """Handles regression with multiple input features"""

    def __init__(self, num_features: int, learning_rate: float = 0.01):
        self.feature_count = num_features
        self.learning_rate = learning_rate
        self.coefficients = [0.0] * num_features
        self.bias = 0.0
        self.cost_trajectory: List[float] = []

    def compute_output(self, features: List[float]) -> float:
        """Single prediction from feature vector"""
        return sum(c * f for c, f in zip(self.coefficients, features)) + self.bias

    def compute_cost(self, data: List[List[float]], targets: List[float]) -> float:
        """Mean squared error loss"""
        n = len(targets)
        predictions = [self.compute_output(row) for row in data]
        return sum((p - t) ** 2 for p, t in zip(predictions, targets)) / n

    def train(
        self,
        features: List[List[float]],
        targets: List[float],
        epochs: int = 1000,
        verbose: bool = True,
        log_interval: int = 200
    ) -> 'MultivariateRegressor':
        """Train the model using batch gradient descent"""
        sample_count = len(targets)

        for epoch in range(epochs):
            outputs = [self.compute_output(row) for row in features]
            deviations = [o - t for o, t in zip(outputs, targets)]

            for dim in range(self.feature_count):
                gradient = (2.0 / sample_count) * sum(
                    deviations[i] * features[i][dim] for i in range(sample_count)
                )
                self.coefficients[dim] -= self.learning_rate * gradient

            bias_grad = (2.0 / sample_count) * sum(deviations)
            self.bias -= self.learning_rate * bias_grad

            cost = self.compute_cost(features, targets)
            self.cost_trajectory.append(cost)

            if verbose and epoch % log_interval == 0:
                print(f"  Step {epoch:4d} | Cost: {cost:.4f}")

        return self


class PolynomialTransformer:
    """Converts single feature into polynomial basis"""

    def __init__(self, order: int):
        self.polynomial_order = order
        self.weights = [0.0] * order
        self.bias = 0.0
        self.learning_rate = 0.01

    def generate_terms(self, x: float) -> List[float]:
        """Create polynomial features up to specified order"""
        return [x ** power for power in range(1, self.polynomial_order + 1)]

    def predict(self, x: float) -> float:
        """Apply polynomial regression"""
        terms = self.generate_terms(x)
        return sum(w * t for w, t in zip(self.weights, terms)) + self.bias

    def fit(self, inputs: List[float], targets: List[float], epochs: int = 1000) -> 'PolynomialTransformer':
        """Learn polynomial coefficients"""
        for _ in range(epochs):
            for x, y_true in zip(inputs, targets):
                terms = self.generate_terms(x)
                prediction = self.predict(x)
                error = prediction - y_true

                for i in range(self.polynomial_order):
                    self.weights[i] -= self.learning_rate * (2.0 * error * terms[i] / len(inputs))
                self.bias -= self.learning_rate * (2.0 * error / len(inputs))

        return self


class RidgeRegularizedModel:
    """Linear regression with L2 regularization to prevent overfitting"""

    def __init__(self, num_features: int, regularization: float = 1.0, learning_rate: float = 0.01):
        self.feature_dim = num_features
        self.alpha = regularization
        self.learning_rate = learning_rate
        self.coeffs = [0.0] * num_features
        self.bias = 0.0

    def evaluate(self, features: List[float]) -> float:
        """Compute model output"""
        return sum(c * f for c, f in zip(self.coeffs, features)) + self.bias

    def train(
        self,
        feature_matrix: List[List[float]],
        targets: List[float],
        epochs: int = 1000,
        verbose: bool = True,
        log_interval: int = 200
    ) -> 'RidgeRegularizedModel':
        """Train with L2 penalty term"""
        n_samples = len(targets)

        for epoch in range(epochs):
            predictions = [self.evaluate(row) for row in feature_matrix]
            errors = [p - t for p, t in zip(predictions, targets)]

            mse = sum(e ** 2 for e in errors) / n_samples
            penalty = self.alpha * sum(w ** 2 for w in self.coeffs)
            total_cost = mse + penalty

            for dim in range(self.feature_dim):
                grad = (2.0 / n_samples) * sum(errors[i] * feature_matrix[i][dim] for i in range(n_samples))
                grad += 2.0 * self.alpha * self.coeffs[dim]
                self.coeffs[dim] -= self.learning_rate * grad

            bias_grad = (2.0 / n_samples) * sum(errors)
            self.bias -= self.learning_rate * bias_grad

            if verbose and epoch % log_interval == 0:
                print(f"  Epoch {epoch:4d} | Cost: {total_cost:.4f} | L2: {penalty:.4f}")

        return self


class ModelEvaluator:
    """Compute various regression metrics"""

    @staticmethod
    def coefficient_of_determination(
        actual: List[float],
        predicted: List[float]
    ) -> float:
        """Calculate R-squared metric"""
        mean_actual = sum(actual) / len(actual)
        ss_residual = sum((a - p) ** 2 for a, p in zip(actual, predicted))
        ss_total = sum((a - mean_actual) ** 2 for a in actual)

        if ss_total == 0:
            return 0.0

        return 1.0 - (ss_residual / ss_total)


class DataNormalizer:
    """Standardize features for better convergence"""

    @staticmethod
    def standardize(dataset: List[List[float]]) -> Tuple[List[List[float]], List[float], List[float]]:
        """Z-score normalization"""
        num_features = len(dataset[0])
        num_samples = len(dataset)

        feature_means = [
            sum(dataset[i][j] for i in range(num_samples)) / num_samples
            for j in range(num_features)
        ]

        feature_stds = []
        for j in range(num_features):
            variance = sum((dataset[i][j] - feature_means[j]) ** 2 for i in range(num_samples)) / num_samples
            feature_stds.append(math.sqrt(variance) if variance > 0 else 1.0)

        normalized = []
        for i in range(num_samples):
            row = [
                (dataset[i][j] - feature_means[j]) / feature_stds[j]
                if feature_stds[j] > 0 else 0.0
                for j in range(num_features)
            ]
            normalized.append(row)

        return normalized, feature_means, feature_stds

    @staticmethod
    def denormalize_target(values: List[float], mean: float, std: float) -> List[float]:
        """Reverse standardization for target variable"""
        return [v * std + mean for v in values]


def create_synthetic_regression_data(
    true_slope: float,
    true_intercept: float,
    n_samples: int,
    noise_std: float = 2.0,
    seed: int = 42
) -> Tuple[List[float], List[float]]:
    """Generate synthetic 1D regression data"""
    random.seed(seed)
    inputs = [random.uniform(0, 10) for _ in range(n_samples)]
    targets = [
        true_slope * x + true_intercept + random.gauss(0, noise_std)
        for x in inputs
    ]
    return inputs, targets


def create_multivariate_housing_data(n_samples: int = 100, seed: int = 42) -> Tuple[List[List[float]], List[float]]:
    """Generate synthetic housing price data with multiple features"""
    random.seed(seed)
    features = []
    prices = []

    for _ in range(n_samples):
        sqft = random.uniform(500, 3000)
        rooms = random.randint(1, 5)
        age = random.uniform(0, 50)
        price = 50 * sqft + 10000 * rooms - 1000 * age + 50000 + random.gauss(0, 20000)

        features.append([sqft, rooms, age])
        prices.append(price)

    return features, prices


def demonstrate_learning():
    """Main demonstration of regression implementations"""
    print("=" * 60)
    print("  FELIX LINEAR REGRESSION DEMONSTRATION")
    print("=" * 60)

    # Simple linear regression with gradient descent
    print("\n[1] Gradient Descent Linear Regression")
    print("-" * 40)
    inputs, targets = create_synthetic_regression_data(3.0, 7.0, 100)
    print(f"Generated {len(targets)} samples")
    print(f"True relationship: y = 3.0x + 7.0 (+ noise)")
    print(f"Sample data: {[(round(inputs[i], 2), round(targets[i], 2)) for i in range(5)]}")

    solver = GradientDescentSolver(step_size=0.005)
    learned_w, learned_b = solver.optimize(inputs, targets, 0.0, 0.0, iterations=1000)

    model = RegressionModel(learned_w, learned_b)
    predictions = [model.apply(x) for x in inputs]
    r2 = ModelEvaluator.coefficient_of_determination(targets, predictions)

    print(f"Learned: y = {learned_w:.4f}x + {learned_b:.4f}")
    print(f"R-squared: {r2:.4f}")

    # Normal equation method
    print("\n[2] Closed-Form Normal Equation")
    print("-" * 40)
    w_closed, b_closed = DirectSolutionFinder.solve(inputs, targets)
    print(f"Solution: y = {w_closed:.4f}x + {b_closed:.4f}")

    # Multivariate regression
    print("\n[3] Multivariate Housing Price Model")
    print("-" * 40)
    X_multi, y_multi = create_multivariate_housing_data(100)
    print(f"Features: sqft, bedrooms, age")
    print(f"Samples: {len(y_multi)}")

    X_norm, x_mean, x_std = DataNormalizer.standardize(X_multi)
    y_mean = sum(y_multi) / len(y_multi)
    y_std = math.sqrt(sum((yi - y_mean) ** 2 for yi in y_multi) / len(y_multi))
    y_norm = [(yi - y_mean) / y_std for yi in y_multi]

    multi_model = MultivariateRegressor(num_features=3, learning_rate=0.01)
    multi_model.train(X_norm, y_norm, epochs=1000, log_interval=200)

    pred_norm = [multi_model.compute_output(row) for row in X_norm]
    r2_multi = ModelEvaluator.coefficient_of_determination(y_norm, pred_norm)

    print(f"Learned coefficients (standardized): {[round(w, 4) for w in multi_model.coeffs]}")
    print(f"Bias (standardized): {multi_model.bias:.4f}")
    print(f"R-squared: {r2_multi:.4f}")

    # Polynomial regression
    print("\n[4] Polynomial Regression")
    print("-" * 40)
    X_poly = [x / 10.0 for x in range(0, 50)]
    y_poly = [0.5 * x ** 2 - 2 * x + 3 + random.gauss(0, 1.0) for x in X_poly]

    x_max = max(abs(x) for x in X_poly)
    X_norm_poly = [x / x_max for x in X_poly]
    y_mean_poly = sum(y_poly) / len(y_poly)
    y_std_poly = math.sqrt(sum((yi - y_mean_poly) ** 2 for yi in y_poly) / len(y_poly))
    y_norm_poly = [(yi - y_mean_poly) / y_std_poly for yi in y_poly]

    print("True: y = 0.5x^2 - 2x + 3")

    for degree in [2, 5]:
        poly_model = PolynomialTransformer(order=degree)
        poly_model.fit(X_norm_poly, y_norm_poly, epochs=2000)

        preds = [poly_model.predict(x) for x in X_norm_poly]
        r2_poly = ModelEvaluator.coefficient_of_determination(y_norm_poly, preds)
        print(f"  Degree {degree}: R-squared = {r2_poly:.4f}")

    # Ridge regression comparison
    print("\n[5] Ridge Regression (L2 Regularization)")
    print("-" * 40)
    print("Comparing regularized vs unregularized coefficients")

    plain = MultivariateRegressor(num_features=3, learning_rate=0.01)
    plain.train(X_norm, y_norm, epochs=1000, verbose=False)

    regularized = RidgeRegularizedModel(num_features=3, regularization=0.1, learning_rate=0.01)
    regularized.train(X_norm, y_norm, epochs=1000, verbose=False)

    print(f"Plain coefficients:    {[round(w, 4) for w in plain.coeffs]}")
    print(f"Ridge coefficients:    {[round(w, 4) for w in regularized.coeffs]}")
    print("Ridge produces smaller coefficients due to L2 penalty")

    # Train/test split evaluation
    print("\n[6] Train/Test Split Evaluation")
    print("-" * 40)
    split_point = int(0.8 * len(inputs))
    X_train, X_test = inputs[:split_point], inputs[split_point:]
    y_train, y_test = targets[:split_point], targets[split_point:]

    gd_solver = GradientDescentSolver(step_size=0.005)
    w_train, b_train = gd_solver.optimize(X_train, y_train, 0.0, 0.0, iterations=1000)

    train_model = RegressionModel(w_train, b_train)
    train_preds = [train_model.apply(x) for x in X_train]
    test_preds = [train_model.apply(x) for x in X_test]

    r2_train = ModelEvaluator.coefficient_of_determination(y_train, train_preds)
    r2_test = ModelEvaluator.coefficient_of_determination(y_test, test_preds)

    print(f"Train R-squared: {r2_train:.4f}")
    print(f"Test R-squared:  {r2_test:.4f}")
    print(f"Learned: y = {w_train:.4f}x + {b_train:.4f}")
    print(f"True:    y = 3.0x + 7.0")

    print("\n" + "=" * 60)
    print("  Regression demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_learning()