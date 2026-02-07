#!/usr/bin/env python3
"""
Felix Learning Platform - Algebraic Structures Module
Advanced topics connecting linear algebra to machine learning
Author: Felix Learning
License: MIT

This module explores advanced algebraic concepts essential for ML,
including tensor operations, Kronecker products, and matrix decompositions.
"""

import random
import math
from typing import List, Tuple, Callable, Optional, Dict, Any
from dataclasses import dataclass


class Tensor:
    """Multi-dimensional array operations for neural networks"""

    def __init__(self, data: Any):
        if isinstance(data, list):
            self.data = data
            self.shape = self._compute_shape(data)
        else:
            self.data = [[data]]
            self.shape = (1, 1)

    def _compute_shape(self, arr: List) -> Tuple[int, ...]:
        """Recursively compute tensor shape"""
        if not isinstance(arr[0], list):
            return (len(arr),)
        return (len(arr),) + self._compute_shape(arr[0])

    def transpose(self) -> 'Tensor':
        """Matrix transpose for 2D tensors"""
        if len(self.shape) != 2:
            raise ValueError("Transpose only defined for 2D tensors")

        rows, cols = self.shape
        transposed = [[self.data[r][c] for r in range(rows)] for c in range(cols)]
        result = Tensor.__new__(Tensor)
        result.data = transposed
        result.shape = (cols, rows)
        return result

    def flatten(self) -> List[float]:
        """Flatten tensor to 1D array"""
        if len(self.shape) == 2:
            return [elem for row in self.data for elem in row]
        return self.data

    def reshape(self, target_shape: Tuple[int, ...]) -> 'Tensor':
        """Reshape tensor to new dimensions"""
        flat = self.flatten()
        result = Tensor.__new__(Tensor)
        result.shape = target_shape

        if len(target_shape) == 2:
            rows, cols = target_shape
            result.data = [[flat[r * cols + c] if r * cols + c < len(flat) else 0
                           for c in range(cols)] for r in range(rows)]
        else:
            result.data = flat

        return result

    def multiply(self, other: 'Tensor') -> 'Tensor':
        """Matrix multiplication"""
        if len(self.shape) != 2 or len(other.shape) != 2:
            raise ValueError("Matrix multiplication requires 2D tensors")

        if self.shape[1] != other.shape[0]:
            raise ValueError(f"Incompatible shapes: {self.shape} x {other.shape}")

        result = Tensor.__new__(Tensor)
        result.shape = (self.shape[0], other.shape[1])
        result.data = [
            [
                sum(self.data[i][k] * other.data[k][j] for k in range(self.shape[1]))
                for j in range(other.shape[1])
            ]
            for i in range(self.shape[0])
        ]
        return result

    def add(self, other: 'Tensor') -> 'Tensor':
        """Element-wise addition"""
        if self.shape != other.shape:
            raise ValueError(f"Shape mismatch: {self.shape} vs {other.shape}")

        result = Tensor.__new__(Tensor)
        result.shape = self.shape

        if len(self.shape) == 2:
            result.data = [
                [self.data[i][j] + other.data[i][j] for j in range(self.shape[1])]
                for i in range(self.shape[0])
            ]
        else:
            result.data = [self.data[i] + other.data[i] for i in range(self.shape[0])]

        return result

    def scalar_multiply(self, scalar: float) -> 'Tensor':
        """Multiply tensor by scalar"""
        result = Tensor.__new__(Tensor)
        result.shape = self.shape

        if len(self.shape) == 2:
            result.data = [
                [self.data[i][j] * scalar for j in range(self.shape[1])]
                for i in range(self.shape[0])
            ]
        else:
            result.data = [self.data[i] * scalar for i in range(self.shape[0])]

        return result

    def sum(self) -> float:
        """Sum all elements"""
        return sum(self.flatten())

    def mean(self) -> float:
        """Mean of all elements"""
        flat = self.flatten()
        return sum(flat) / len(flat)

    def variance(self) -> float:
        """Variance of all elements"""
        m = self.mean()
        flat = self.flatten()
        return sum((x - m) ** 2 for x in flat) / len(flat)

    def std(self) -> float:
        """Standard deviation"""
        return math.sqrt(self.variance())


class MatrixDecomposer:
    """Matrix decomposition utilities"""

    @staticmethod
    def lu_decomposition(matrix: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """LU decomposition without pivoting"""
        n = len(matrix)

        L = [[0.0] * n for _ in range(n)]
        U = [[0.0] * n for _ in range(n)]

        for i in range(n):
            L[i][i] = 1.0

        for k in range(n):
            U[k][k:] = [matrix[k][j] - sum(L[k][m] * U[m][j] for m in range(k)) for j in range(k, n)]

            for i in range(k + 1, n):
                if abs(U[k][k]) > 1e-10:
                    L[i][k] = (matrix[i][k] - sum(L[i][m] * U[m][k] for m in range(k))) / U[k][k]

        return L, U

    @staticmethod
    def qr_decomposition(matrix: List[List[float]]) -> Tuple[List[List[float]], List[List[float]]]:
        """QR decomposition using Gram-Schmidt"""
        m, n = len(matrix), len(matrix[0])

        Q = [[0.0] * n for _ in range(m)]
        R = [[0.0] * n for _ in range(n)]

        for j in range(n):
            v = [matrix[i][j] for i in range(m)]

            for i in range(j):
                q_i = [Q[i][k] for k in range(m)]
                proj = sum(q_i[k] * v[k] for k in range(m)) / sum(q_i[k] ** 2 for k in range(m))
                v = [v[k] - proj * q_i[k] for k in range(m)]

            norm = math.sqrt(sum(v[k] ** 2 for k in range(m)))
            if norm > 1e-10:
                for i in range(m):
                    Q[i][j] = v[i] / norm

            for i in range(j, n):
                R[j][i] = sum(Q[k][j] * matrix[k][i] for k in range(m))

        return Q, R

    @staticmethod
    def eigendecomposition_2x2(matrix: List[List[float]]) -> Tuple[List[float], List[List[float]]]:
        """Eigenvalues and eigenvectors for 2x2 matrix"""
        a, b = matrix[0][0], matrix[0][1]
        c, d = matrix[1][0], matrix[1][1]

        trace = a + d
        det = a * d - b * c

        discriminant = trace ** 2 - 4 * det

        if discriminant < 0:
            return [], []

        sqrt_disc = math.sqrt(discriminant)
        lambda1 = (trace + sqrt_disc) / 2
        lambda2 = (trace - sqrt_disc) / 2

        eigvals = [lambda1, lambda2]
        eigvecs = []

        for lam in eigvals:
            if abs(b) > 1e-10:
                vec = [1.0, (lam - a) / b]
            elif abs(c) > 1e-10:
                vec = [(lam - d) / c, 1.0]
            else:
                vec = [1.0, 0.0] if lam == a else [0.0, 1.0]

            norm = math.sqrt(sum(x ** 2 for x in vec))
            vec = [x / norm for x in vec]
            eigvecs.append(vec)

        return eigvals, eigvecs


class KroneckerProduct:
    """Kronecker product operations for tensor computations"""

    @staticmethod
    def compute(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Compute Kronecker product A ⊗ B"""
        rows_a, cols_a = len(A), len(A[0])
        rows_b, cols_b = len(B), len(B[0])

        result_rows = rows_a * rows_b
        result_cols = cols_a * cols_b

        result = [[0.0] * result_cols for _ in range(result_rows)]

        for i in range(rows_a):
            for j in range(cols_a):
                for k in range(rows_b):
                    for l in range(cols_b):
                        result[i * rows_b + k][j * cols_b + l] = A[i][j] * B[k][l]

        return result


class HadamardProduct:
    """Element-wise matrix multiplication"""

    @staticmethod
    def compute(A: List[List[float]], B: List[List[float]]) -> List[List[float]]:
        """Compute element-wise product A ∘ B"""
        if len(A) != len(B) or len(A[0]) != len(B[0]):
            raise ValueError("Matrices must have same dimensions")

        rows, cols = len(A), len(A[0])
        return [[A[i][j] * B[i][j] for j in range(cols)] for i in range(rows)]


class MatrixNormCalculator:
    """Compute various matrix norms"""

    @staticmethod
    def frobenius(A: List[List[float]]) -> float:
        """Frobenius norm = sqrt(sum of squared elements)"""
        total = 0.0
        for row in A:
            for elem in row:
                total += elem ** 2
        return math.sqrt(total)

    @staticmethod
    def nuclear(A: List[List[float]]) -> float:
        """Nuclear norm = sum of singular values (approximation)"""
        eigenvalues = []
        n = len(A)

        for i in range(n):
            for j in range(n):
                pass

        trace = sum(A[i][i] for i in range(n))
        frob = MatrixNormCalculator.frobenius(A)

        return (frob + trace) / 2

    @staticmethod
    def spectral(A: List[List[float]]) -> float:
        """Spectral norm = largest singular value"""
        eigenvalues, _ = MatrixDecomposer.eigendecomposition_2x2(A)

        if not eigenvalues:
            return MatrixNormCalculator.frobenius(A)

        return max(abs(e) for e in eigenvalues)


class VectorSpace:
    """Vector space operations and concepts"""

    @staticmethod
    def dot_product(u: List[float], v: List[float]) -> float:
        """Compute dot product of two vectors"""
        if len(u) != len(v):
            raise ValueError("Vectors must have same dimension")
        return sum(ui * vi for ui, vi in zip(u, v))

    @staticmethod
    def cross_product(u: List[float], v: List[float]) -> List[float]:
        """Compute cross product (3D vectors only)"""
        if len(u) != 3 or len(v) != 3:
            raise ValueError("Cross product only defined for 3D vectors")

        return [
            u[1] * v[2] - u[2] * v[1],
            u[2] * v[0] - u[0] * v[2],
            u[0] * v[1] - u[1] * v[0]
        ]

    @staticmethod
    def magnitude(v: List[float]) -> float:
        """Compute vector magnitude/L2 norm"""
        return math.sqrt(sum(x ** 2 for x in v))

    @staticmethod
    def normalize(v: List[float]) -> List[float]:
        """Normalize vector to unit length"""
        mag = VectorSpace.magnitude(v)
        if mag < 1e-10:
            return v
        return [x / mag for x in v]

    @staticmethod
    def angle_between(u: List[float], v: List[float]) -> float:
        """Compute angle between two vectors in radians"""
        dot = VectorSpace.dot_product(u, v)
        mag_u = VectorSpace.magnitude(u)
        mag_v = VectorSpace.magnitude(v)

        if mag_u < 1e-10 or mag_v < 1e-10:
            return 0.0

        cos_angle = max(-1.0, min(1.0, dot / (mag_u * mag_v)))
        return math.acos(cos_angle)

    @staticmethod
    def projection(u: List[float], v: List[float]) -> List[float]:
        """Project vector u onto vector v"""
        dot_uv = VectorSpace.dot_product(u, v)
        dot_vv = VectorSpace.dot_product(v, v)

        if abs(dot_vv) < 1e-10:
            return [0.0] * len(v)

        scalar = dot_uv / dot_vv
        return [scalar * vi for vi in v]

    @staticmethod
    def is_orthogonal(u: List[float], v: List[float], tol: float = 1e-10) -> bool:
        """Check if two vectors are orthogonal"""
        return abs(VectorSpace.dot_product(u, v)) < tol


class LinearTransformation:
    """Represent and apply linear transformations"""

    def __init__(self, matrix: List[List[float]]):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def apply(self, vector: List[float]) -> List[float]:
        """Apply transformation to vector"""
        if len(vector) != self.cols:
            raise ValueError(f"Vector dimension {len(vector)} != matrix columns {self.cols}")

        result = []
        for i in range(self.rows):
            row_sum = sum(self.matrix[i][j] * vector[j] for j in range(self.cols))
            result.append(row_sum)
        return result

    def compose(self, other: 'LinearTransformation') -> 'LinearTransformation':
        """Compose with another transformation (self ∘ other)"""
        if self.cols != other.rows:
            raise ValueError("Incompatible transformations")

        result = [[0.0] * other.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(other.cols):
                result[i][j] = sum(
                    self.matrix[i][k] * other.matrix[k][j]
                    for k in range(self.cols)
                )

        return LinearTransformation(result)


def demonstrate_algebraic_topics():
    """Main demonstration of algebraic structure concepts"""
    print("=" * 60)
    print("  FELIX ALGEBRAIC STRUCTURES DEMONSTRATION")
    print("=" * 60)

    # Tensor operations
    print("\n[1] Tensor Operations")
    print("-" * 40)
    data_2x3 = [[1, 2, 3], [4, 5, 6]]
    tensor = Tensor(data_2x3)
    print(f"Original tensor shape: {tensor.shape}")
    print(f"Elements: {tensor.flatten()}")

    transposed = tensor.transpose()
    print(f"Transposed shape: {transposed.shape}")
    print(f"Transposed data: {transposed.data}")

    reshaped = tensor.reshape((3, 2))
    print(f"Reshaped to (3, 2): {reshaped.data}")

    # Matrix multiplication
    print("\n[2] Matrix Multiplication")
    print("-" * 40)
    A = Tensor([[1, 2], [3, 4]])
    B = Tensor([[5, 6], [7, 8]])
    C = A.multiply(B)
    print(f"A = {A.data}")
    print(f"B = {B.data}")
    print(f"A × B = {C.data}")

    # LU decomposition
    print("\n[3] LU Decomposition")
    print("-" * 40)
    M = [[2, 1], [1, 3]]
    print(f"Matrix: {M}")
    L, U = MatrixDecomposer.lu_decomposition(M)
    print(f"L (lower): {L}")
    print(f"U (upper): {U}")

    reconstructed = Tensor(L).multiply(Tensor(U))
    print(f"Reconstructed L×U: {reconstructed.data}")

    # QR decomposition
    print("\n[4] QR Decomposition")
    print("-" * 40)
    M2 = [[1, 1], [1, 2]]
    print(f"Matrix: {M2}")
    Q, R = MatrixDecomposer.qr_decomposition(M2)
    print(f"Q (orthogonal): {[row for row in Q]}")
    print(f"R (upper triangular): {[row for row in R]}")

    # Eigenvalues for 2x2
    print("\n[5] Eigenvalue Decomposition (2x2)")
    print("-" * 40)
    M3 = [[4, 2], [1, 3]]
    print(f"Matrix: {M3}")
    eigvals, eigvecs = MatrixDecomposer.eigendecomposition_2x2(M3)
    print(f"Eigenvalues: {[round(v, 4) for v in eigvals]}")
    print(f"Eigenvectors: {[round(v, 4) for vec in eigvecs for v in vec]}")

    # Kronecker product
    print("\n[6] Kronecker Product")
    print("-" * 40)
    K1 = [[1, 2], [3, 4]]
    K2 = [[0, 5], [6, 7]]
    print(f"A = {K1}")
    print(f"B = {K2}")
    kron_result = KroneckerProduct.compute(K1, K2)
    print(f"A ⊗ B = {kron_result}")

    # Matrix norms
    print("\n[7] Matrix Norms")
    print("-" * 40)
    N = [[3, 4], [4, 9]]
    print(f"Matrix: {N}")
    print(f"Frobenius norm: {MatrixNormCalculator.frobenius(N):.4f}")
    print(f"Spectral norm: {MatrixNormCalculator.spectral(N):.4f}")

    # Vector space operations
    print("\n[8] Vector Space Operations")
    print("-" * 40)
    u = [1, 0, 0]
    v = [0, 1, 0]
    w = [1, 1, 0]

    print(f"u = {u}, v = {v}, w = {w}")
    print(f"u · v = {VectorSpace.dot_product(u, v)}")
    print(f"u × v = {VectorSpace.cross_product(u, v)}")
    print(f"|w| = {VectorSpace.magnitude(w):.4f}")
    print(f"Normalize w = {VectorSpace.normalize(w)}")
    print(f"Angle u-v: {VectorSpace.angle_between(u, v):.4f} rad")
    print(f"u proj w = {VectorSpace.projection(u, w)}")
    print(f"u ⟂ v? {VectorSpace.is_orthogonal(u, v)}")

    # Linear transformation
    print("\n[9] Linear Transformations")
    print("-" * 40)
    rot_matrix = [[0, -1], [1, 0]]  # 90 degree rotation
    transform = LinearTransformation(rot_matrix)

    test_vec = [1, 0]
    transformed = transform.apply(test_vec)
    print(f"90° rotation applied to {test_vec}: {transformed}")

    scale = LinearTransformation([[2, 0], [0, 2]])
    scaled = scale.apply(test_vec)
    print(f"Scale 2x applied to {test_vec}: {scaled}")

    composed = transform.compose(scale)
    composed_result = composed.apply(test_vec)
    print(f"Scale then rotate: {composed_result}")

    # Tensor scalar operations
    print("\n[10] Tensor Scalar Operations")
    print("-" * 40)
    T = Tensor([[1, 2, 3], [4, 5, 6]])
    doubled = T.scalar_multiply(2)
    print(f"Original: {T.data}")
    print(f"Doubled: {doubled.data}")
    print(f"Sum: {T.sum()}, Mean: {T.mean():.2f}, Std: {T.std():.2f}")

    print("\n" + "=" * 60)
    print("  Algebraic structures demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_algebraic_topics()