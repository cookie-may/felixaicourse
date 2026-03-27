#!/usr/bin/env python3
"""
Felix Learning Platform - Matrix Operations Module
Matrix arithmetic, transformations, and neural network applications
Author: Felix Learning
License: MIT

This module implements matrix operations with custom class-based
architecture for Felix's ML curriculum.
"""

import random
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class MatrixData:
    """Container for matrix row data"""
    data: List[List[float]]
    rows: int
    cols: int


class MatrixBuilder:
    """Build matrices with various initialization strategies"""

    @staticmethod
    def create(data: List[List[float]]) -> 'FelixMatrix':
        """Create matrix from 2D list"""
        return FelixMatrix(data)

    @staticmethod
    def identity(size: int) -> 'FelixMatrix':
        """Create identity matrix"""
        return FelixMatrix([
            [1 if i == j else 0 for j in range(size)]
            for i in range(size)
        ])

    @staticmethod
    def zeros(rows: int, cols: int) -> 'FelixMatrix':
        """Create matrix of zeros"""
        return FelixMatrix([[0] * cols for _ in range(rows)])

    @staticmethod
    def random(rows: int, cols: int, low: float = -1.0, high: float = 1.0) -> 'FelixMatrix':
        """Create matrix with random values"""
        return FelixMatrix([
            [random.uniform(low, high) for _ in range(cols)]
            for _ in range(rows)
        ])


class MatrixArithmetic:
    """Matrix arithmetic operations"""

    @staticmethod
    def add(mat_a: 'FelixMatrix', mat_b: 'FelixMatrix') -> 'FelixMatrix':
        """Add two matrices"""
        if mat_b.shape == mat_a.shape:
            return FelixMatrix([
                [mat_a.data[i][j] + mat_b.data[i][j] for j in range(mat_a.cols)]
                for i in range(mat_a.rows)
            ])
        if mat_b.rows == 1 and mat_b.cols == mat_a.cols:
            return FelixMatrix([
                [mat_a.data[i][j] + mat_b.data[0][j] for j in range(mat_a.cols)]
                for i in range(mat_a.rows)
            ])
        if mat_b.cols == 1 and mat_b.rows == mat_a.rows:
            return FelixMatrix([
                [mat_a.data[i][j] + mat_b.data[i][0] for j in range(mat_a.cols)]
                for i in range(mat_a.rows)
            ])
        raise ValueError(f"Cannot add shapes {mat_a.shape} and {mat_b.shape}")

    @staticmethod
    def subtract(mat_a: 'FelixMatrix', mat_b: 'FelixMatrix') -> 'FelixMatrix':
        """Subtract matrices"""
        return FelixMatrix([
            [mat_a.data[i][j] - mat_b.data[i][j] for j in range(mat_a.cols)]
            for i in range(mat_a.rows)
        ])

    @staticmethod
    def scalar_multiply(mat: 'FelixMatrix', scalar: float) -> 'FelixMatrix':
        """Multiply matrix by scalar"""
        return FelixMatrix([
            [mat.data[i][j] * scalar for j in range(mat.cols)]
            for i in range(mat.rows)
        ])

    @staticmethod
    def element_wise_multiply(mat_a: 'FelixMatrix', mat_b: 'FelixMatrix') -> 'FelixMatrix':
        """Element-wise multiplication (Hadamard product)"""
        return FelixMatrix([
            [mat_a.data[i][j] * mat_b.data[i][j] for j in range(mat_a.cols)]
            for i in range(mat_a.rows)
        ])


class MatrixMultiplier:
    """Matrix multiplication operations"""

    @staticmethod
    def multiply(mat_a: 'FelixMatrix', mat_b: 'FelixMatrix') -> 'FelixMatrix':
        """Matrix-matrix multiplication"""
        if mat_a.cols != mat_b.rows:
            raise ValueError(
                f"Cannot multiply shapes {mat_a.shape} and {mat_b.shape}: "
                f"inner dimensions {mat_a.cols} != {mat_b.rows}"
            )
        return FelixMatrix([
            [
                sum(mat_a.data[i][k] * mat_b.data[k][j] for k in range(mat_a.cols))
                for j in range(mat_b.cols)
            ]
            for i in range(mat_a.rows)
        ])

    @staticmethod
    def multiply_vector(mat: 'FelixMatrix', vec: 'FelixVector') -> 'FelixVector':
        """Matrix-vector multiplication"""
        return FelixVector([
            sum(mat.data[i][j] * vec.components[j] for j in range(mat.cols))
            for i in range(mat.rows)
        ])


class MatrixTransform:
    """Matrix transformation operations"""

    @staticmethod
    def transpose(mat: 'FelixMatrix') -> 'FelixMatrix':
        """Transpose matrix"""
        return FelixMatrix([
            [mat.data[j][i] for j in range(mat.rows)]
            for i in range(mat.cols)
        ])


class DeterminantCalculator:
    """Compute matrix determinants"""

    @staticmethod
    def compute(mat: 'FelixMatrix') -> float:
        """Compute determinant recursively"""
        if mat.rows != mat.cols:
            raise ValueError("Determinant only defined for square matrices")

        if mat.shape == (1, 1):
            return mat.data[0][0]
        if mat.shape == (2, 2):
            return mat.data[0][0] * mat.data[1][1] - mat.data[0][1] * mat.data[1][0]

        det = 0
        for j in range(mat.cols):
            minor_data = [
                [mat.data[i][k] for k in range(mat.cols) if k != j]
                for i in range(1, mat.rows)
            ]
            minor = FelixMatrix(minor_data)
            det += ((-1) ** j) * mat.data[0][j] * DeterminantCalculator.compute(minor)
        return det


class MatrixInverter:
    """Matrix inversion operations"""

    @staticmethod
    def invert_2x2(mat: 'FelixMatrix') -> 'FelixMatrix':
        """Compute 2x2 matrix inverse"""
        if mat.shape != (2, 2):
            raise ValueError("This method only works for 2x2 matrices")

        det = DeterminantCalculator.compute(mat)
        if abs(det) < 1e-10:
            raise ValueError("Matrix is singular, no inverse exists")

        return FelixMatrix([
            [mat.data[1][1] / det, -mat.data[0][1] / det],
            [-mat.data[1][0] / det, mat.data[0][0] / det]
        ])


class ActivationFunctions:
    """Activation functions for neural networks"""

    @staticmethod
    def relu(mat: 'FelixMatrix') -> 'FelixMatrix':
        """ReLU activation: max(0, x)"""
        return FelixMatrix([[max(0, val) for val in row] for row in mat.data])


@dataclass
class LayerConfig:
    """Configuration for neural network layer"""
    input_size: int
    hidden_size: int
    output_size: int


class FelixVector:
    """Vector class for matrix-vector operations"""

    def __init__(self, data: List[float]):
        self.components = list(data)
        self.size = len(self.components)

    def __repr__(self):
        return f"FelixVector({self.components})"

    def __add__(self, other):
        return FelixVector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other):
        return FelixVector([a - b for a, b in zip(self.components, other.components)])

    def __mul__(self, scalar):
        return FelixVector([x * scalar for x in self.components])

    def dot(self, other):
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self):
        return math.sqrt(sum(x ** 2 for x in self.components))

    def normalize(self):
        mag = self.magnitude()
        return FelixVector([x / mag for x in self.components])


class FelixMatrix:
    """Main matrix class with full functionality"""

    def __init__(self, data: List[List[float]]):
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.shape = (self.rows, self.cols)

    def __repr__(self):
        col_widths = []
        for j in range(self.cols):
            width = max(len(f"{self.data[i][j]:.4f}") for i in range(self.rows))
            col_widths.append(width)
        lines = []
        for i in range(self.rows):
            row_str = "  ".join(
                f"{self.data[i][j]:{col_widths[j]}.4f}" for j in range(self.cols)
            )
            bracket_l = "|" if 0 < i < self.rows - 1 else ("/" if i == 0 else "\\")
            bracket_r = "|" if 0 < i < self.rows - 1 else ("\\" if i == 0 else "/")
            lines.append(f"  {bracket_l} {row_str} {bracket_r}")
        header = f"FelixMatrix {self.rows}x{self.cols}:"
        return header + "\n" + "\n".join(lines)

    def __add__(self, other):
        return MatrixArithmetic.add(self, other)

    def __sub__(self, other):
        return MatrixArithmetic.subtract(self, other)

    def scalar_multiply(self, scalar):
        return MatrixArithmetic.scalar_multiply(self, scalar)

    def element_wise_multiply(self, other):
        return MatrixArithmetic.element_wise_multiply(self, other)

    def matmul(self, other):
        return MatrixMultiplier.multiply(self, other)

    def __matmul__(self, other):
        if isinstance(other, FelixVector):
            return MatrixMultiplier.multiply_vector(self, other)
        return MatrixMultiplier.multiply(self, other)

    def transpose(self):
        return MatrixTransform.transpose(self)

    @property
    def T(self):
        return self.transpose()

    def determinant(self):
        return DeterminantCalculator.compute(self)

    def inverse_2x2(self):
        return MatrixInverter.invert_2x2(self)

    @staticmethod
    def identity(n):
        return MatrixBuilder.identity(n)

    @staticmethod
    def zeros(rows, cols):
        return MatrixBuilder.zeros(rows, cols)

    @staticmethod
    def random(rows, cols, low=-1.0, high=1.0):
        return MatrixBuilder.random(rows, cols, low, high)


def demonstrate_basic_operations():
    """Demo: Basic matrix operations"""
    print("=" * 60)
    print("  FELIX BASIC MATRIX OPERATIONS")
    print("=" * 60)

    A = FelixMatrix([[1, 2], [3, 4]])
    B = FelixMatrix([[5, 6], [7, 8]])

    print("\nA =")
    print(A)
    print("\nB =")
    print(B)

    print("\nA + B =")
    print(A + B)

    print("\nA - B =")
    print(A - B)

    print("\nA * 3 (scalar) =")
    print(A.scalar_multiply(3))

    print("\nA * B (element-wise) =")
    print(A.element_wise_multiply(B))

    print("\nA @ B (matrix multiply) =")
    print(A @ B)

    print("\nA^T =")
    print(A.T)


def demonstrate_determinant_inverse():
    """Demo: Determinant and inverse"""
    print("\n" + "=" * 60)
    print("  FELIX DETERMINANT AND INVERSE")
    print("=" * 60)

    A = FelixMatrix([[4, 7], [2, 6]])
    print("\nA =")
    print(A)
    print(f"\ndet(A) = {A.determinant()}")

    A_inv = A.inverse_2x2()
    print("\nA^-1 =")
    print(A_inv)

    print("\nA @ A^-1 (should be identity) =")
    print(A @ A_inv)

    I = FelixMatrix.identity(3)
    print("\nIdentity 3x3 =")
    print(I)


def demonstrate_broadcasting():
    """Demo: Broadcasting operations"""
    print("\n" + "=" * 60)
    print("  FELIX BROADCASTING")
    print("=" * 60)

    output = FelixMatrix([[1, 2, 3], [4, 5, 6]])
    bias = FelixMatrix([[10, 20, 30]])

    print("\nOutput =")
    print(output)
    print("\nBias =")
    print(bias)
    print("\nOutput + Bias (broadcast) =")
    print(output + bias)


def demonstrate_neural_network_layer():
    """Demo: Neural network forward pass"""
    print("\n" + "=" * 60)
    print("  FELIX NEURAL NETWORK FORWARD PASS")
    print("=" * 60)

    random.seed(42)

    input_size = 3
    hidden_size = 4
    output_size = 2

    x = FelixVector([0.5, 0.8, 0.2])
    W1 = MatrixBuilder.random(hidden_size, input_size, -0.5, 0.5)
    b1 = FelixVector([0.0] * hidden_size)
    W2 = MatrixBuilder.random(output_size, hidden_size, -0.5, 0.5)
    b2 = FelixVector([0.0] * output_size)

    print(f"\nInput x: {x.size}D")
    print(f"W1: {W1.shape}")
    print(f"W2: {W2.shape}")

    z1_comps = [sum(W1.data[i][j] * x.components[j] for j in range(input_size)) for i in range(hidden_size)]
    z1 = FelixVector(z1_comps)
    h1_comps = [max(0, val) for val in z1_comps]
    h1 = FelixVector(h1_comps)
    print(f"\nHidden layer pre-activation z1: {z1}")
    print(f"Hidden layer post-ReLU h1: {h1}")

    z2_comps = [sum(W2.data[i][j] * h1.components[j] for j in range(hidden_size)) for i in range(output_size)]
    z2 = FelixVector(z2_comps)
    print(f"\nOutput z2: {z2}")

    print("\nThis is a complete 2-layer neural network forward pass.")
    print("Layer 1: W1 @ x + b1 -> ReLU -> h1")
    print("Layer 2: W2 @ h1 + b2 -> z2")


def demonstrate_weight_matrix_intuition():
    """Demo: Weight matrix intuition"""
    print("\n" + "=" * 60)
    print("  FELIX WEIGHT MATRIX INTUITION")
    print("=" * 60)

    print("\nA weight matrix transforms input features into output features.")
    print("Each row extracts one pattern from the input.\n")

    W = FelixMatrix([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.5, 0.5, 0.0],
    ])
    x = FelixVector([0.8, 0.6, 0.1])

    print("Weight matrix W (3 detectors, 3 inputs):")
    print(W)
    print("\nInput x:")
    print(x)
    print("\nW @ x =")
    result = W @ x
    print(result)
    print("\nRow 0 of W = [1, 0, 0]: copies input feature 0")
    print("Row 1 of W = [0, 1, 0]: copies input feature 1")
    print("Row 2 of W = [0.5, 0.5, 0]: averages features 0 and 1")


if __name__ == "__main__":
    demonstrate_basic_operations()
    demonstrate_determinant_inverse()
    demonstrate_broadcasting()
    demonstrate_weight_matrix_intuition()
    demonstrate_neural_network_layer()
