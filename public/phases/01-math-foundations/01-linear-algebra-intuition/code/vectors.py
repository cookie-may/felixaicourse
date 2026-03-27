#!/usr/bin/env python3
"""
Felix Learning Platform - Vectors Module
Fundamental vector operations and linear algebra concepts
Author: Felix Learning
License: MIT

This module implements vector operations with custom class-based
architecture for Felix's ML curriculum.
"""

import math
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class VectorCoordinates:
    """Container for vector component data"""
    components: List[float]
    dimension: int


class VectorArithmetic:
    """Basic arithmetic operations for vectors"""

    @staticmethod
    def add(vec_a: VectorCoordinates, vec_b: VectorCoordinates) -> VectorCoordinates:
        """Add two vectors component-wise"""
        return VectorCoordinates(
            components=[a + b for a, b in zip(vec_a.components, vec_b.components)],
            dimension=vec_a.dimension
        )

    @staticmethod
    def subtract(vec_a: VectorCoordinates, vec_b: VectorCoordinates) -> VectorCoordinates:
        """Subtract vectors component-wise"""
        return VectorCoordinates(
            components=[a - b for a, b in zip(vec_a.components, vec_b.components)],
            dimension=vec_a.dimension
        )

    @staticmethod
    def scale(vec: VectorCoordinates, scalar: float) -> VectorCoordinates:
        """Multiply vector by scalar"""
        return VectorCoordinates(
            components=[x * scalar for x in vec.components],
            dimension=vec.dimension
        )


class VectorMetric:
    """Compute various vector metrics"""

    @staticmethod
    def magnitude(vec: VectorCoordinates) -> float:
        """Compute L2 norm/magnitude of vector"""
        return math.sqrt(sum(x ** 2 for x in vec.components))

    @staticmethod
    def dot_product(vec_a: VectorCoordinates, vec_b: VectorCoordinates) -> float:
        """Compute dot product of two vectors"""
        return sum(a * b for a, b in zip(vec_a.components, vec_b.components))

    @staticmethod
    def normalize(vec: VectorCoordinates) -> VectorCoordinates:
        """Normalize vector to unit length"""
        mag = VectorMetric.magnitude(vec)
        if mag < 1e-10:
            return vec
        return VectorCoordinates(
            components=[x / mag for x in vec.components],
            dimension=vec.dimension
        )


class SimilarityCalculator:
    """Compute similarity measures between vectors"""

    @staticmethod
    def cosine_similarity(vec_a: VectorCoordinates, vec_b: VectorCoordinates) -> float:
        """Compute cosine similarity between vectors"""
        mag_a = VectorMetric.magnitude(vec_a)
        mag_b = VectorMetric.magnitude(vec_b)
        if mag_a < 1e-10 or mag_b < 1e-10:
            return 0.0
        return VectorMetric.dot_product(vec_a, vec_b) / (mag_a * mag_b)

    @staticmethod
    def angle_between(vec_a: VectorCoordinates, vec_b: VectorCoordinates) -> float:
        """Compute angle between vectors in degrees"""
        cos_sim = SimilarityCalculator.cosine_similarity(vec_a, vec_b)
        cos_sim = max(-1.0, min(1.0, cos_sim))
        return math.degrees(math.acos(cos_sim))


class ProjectionEngine:
    """Vector projection operations"""

    @staticmethod
    def project_onto(source: VectorCoordinates, target: VectorCoordinates) -> VectorCoordinates:
        """Project source vector onto target vector"""
        dot_ss = VectorMetric.dot_product(source, source)
        if dot_ss < 1e-10:
            return VectorCoordinates(components=[0.0] * source.dimension, dimension=source.dimension)

        dot_ts = VectorMetric.dot_product(target, source)
        scalar = dot_ts / dot_ss
        return VectorCoordinates(
            components=[scalar * x for x in source.components],
            dimension=source.dimension
        )

    @staticmethod
    def decompose(source: VectorCoordinates, target: VectorCoordinates) -> Tuple[VectorCoordinates, VectorCoordinates]:
        """Decompose source into parallel and perpendicular components relative to target"""
        parallel = ProjectionEngine.project_onto(source, target)
        perpendicular = VectorArithmetic.subtract(source, parallel)
        return parallel, perpendicular


class IndependenceChecker:
    """Check linear independence of vector sets"""

    @staticmethod
    def is_independent(vectors: List[VectorCoordinates]) -> bool:
        """Determine if set of vectors is linearly independent"""
        n = len(vectors)
        if n == 0:
            return True

        dim = vectors[0].dimension
        rows = [vec.components[:] for vec in vectors]
        rank = 0

        for col in range(dim):
            pivot = None
            for row in range(rank, len(rows)):
                if abs(rows[row][col]) > 1e-10:
                    pivot = row
                    break
            if pivot is None:
                continue

            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            scale = rows[rank][col]
            rows[rank] = [x / scale for x in rows[rank]]

            for row in range(len(rows)):
                if row != rank and abs(rows[row][col]) > 1e-10:
                    factor = rows[row][col]
                    rows[row] = [rows[row][j] - factor * rows[rank][j] for j in range(dim)]
            rank += 1

        return rank == n


class OrthogonalizationEngine:
    """Gram-Schmidt orthogonalization process"""

    @staticmethod
    def gram_schmidt(vectors: List[VectorCoordinates]) -> List[VectorCoordinates]:
        """Orthogonalize set of vectors using Gram-Schmidt process"""
        orthonormal = []

        for v in vectors:
            w_comp = v.components[:]
            w = VectorCoordinates(components=w_comp, dimension=v.dimension)

            for u in orthonormal:
                u_vec = VectorCoordinates(components=u.components, dimension=u.dimension)
                proj = ProjectionEngine.project_onto(w, u_vec)
                w = VectorArithmetic.subtract(w, proj)

            mag = VectorMetric.magnitude(w)
            if mag < 1e-10:
                continue

            normalized = VectorMetric.normalize(w)
            orthonormal.append(normalized)

        return orthonormal


class FelixVector:
    """Main vector class with full functionality"""

    def __init__(self, components: List[float]):
        self.components = list(components)
        self.dimension = len(self.components)

    def __add__(self, other: 'FelixVector') -> 'FelixVector':
        result = VectorArithmetic.add(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )
        return FelixVector(result.components)

    def __sub__(self, other: 'FelixVector') -> 'FelixVector':
        result = VectorArithmetic.subtract(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )
        return FelixVector(result.components)

    def __mul__(self, scalar: float) -> 'FelixVector':
        result = VectorArithmetic.scale(
            VectorCoordinates(self.components, self.dimension),
            scalar
        )
        return FelixVector(result.components)

    def dot(self, other: 'FelixVector') -> float:
        return VectorMetric.dot_product(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )

    def magnitude(self) -> float:
        return VectorMetric.magnitude(
            VectorCoordinates(self.components, self.dimension)
        )

    def normalize(self) -> 'FelixVector':
        result = VectorMetric.normalize(
            VectorCoordinates(self.components, self.dimension)
        )
        return FelixVector(result.components)

    def cosine_similarity(self, other: 'FelixVector') -> float:
        return SimilarityCalculator.cosine_similarity(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )

    def angle_between(self, other: 'FelixVector') -> float:
        return SimilarityCalculator.angle_between(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )

    def project_onto(self, other: 'FelixVector') -> 'FelixVector':
        result = ProjectionEngine.project_onto(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )
        return FelixVector(result.components)

    def decompose(self, other: 'FelixVector') -> Tuple['FelixVector', 'FelixVector']:
        parallel, perp = ProjectionEngine.decompose(
            VectorCoordinates(self.components, self.dimension),
            VectorCoordinates(other.components, other.dimension)
        )
        return FelixVector(parallel.components), FelixVector(perp.components)

    def __repr__(self) -> str:
        return f"FelixVector({self.components})"


class FelixMatrix:
    """Basic matrix operations for neural network layers"""

    def __init__(self, rows: List[List[float]]):
        self.rows = [list(row) for row in rows]
        self.shape = (len(self.rows), len(self.rows[0]))

    def __matmul__(self, other):
        if isinstance(other, FelixVector):
            return FelixVector([
                sum(self.rows[i][j] * other.components[j] for j in range(self.shape[1]))
                for i in range(self.shape[0])
            ])
        rows = []
        for i in range(self.shape[0]):
            row = []
            for j in range(other.shape[1]):
                row.append(sum(
                    self.rows[i][k] * other.rows[k][j]
                    for k in range(self.shape[1])
                ))
            rows.append(row)
        return FelixMatrix(rows)

    def transpose(self):
        return FelixMatrix([
            [self.rows[j][i] for j in range(self.shape[0])]
            for i in range(self.shape[1])
        ])

    def rank(self) -> int:
        rows = [row[:] for row in self.rows]
        m, n = self.shape
        r = 0
        for col in range(n):
            pivot = None
            for row in range(r, m):
                if abs(rows[row][col]) > 1e-10:
                    pivot = row
                    break
            if pivot is None:
                continue
            rows[r], rows[pivot] = rows[pivot], rows[r]
            scale = rows[r][col]
            rows[r] = [x / scale for x in rows[r]]
            for row in range(m):
                if row != r and abs(rows[row][col]) > 1e-10:
                    factor = rows[row][col]
                    rows[row] = [rows[row][j] - factor * rows[r][j] for j in range(n)]
            r += 1
        return r

    def __repr__(self) -> str:
        return f"FelixMatrix({self.rows})"


def demonstrate_vector_operations():
    """Demo: Basic vector operations"""
    print("=" * 60)
    print("  FELIX VECTOR OPERATIONS")
    print("=" * 60)

    a = FelixVector([1, 2, 3])
    b = FelixVector([4, 5, 6])
    print(f"\na = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * 3 = {a * 3}")
    print(f"a · b = {a.dot(b)}")
    print(f"|a| = {a.magnitude():.4f}")
    print(f"â (normalized) = {a.normalize()}")
    print(f"cosine_similarity(a, b) = {a.cosine_similarity(b):.4f}")


def demonstrate_angle_projection():
    """Demo: Angles and projections"""
    print("\n" + "=" * 60)
    print("  FELIX ANGLE AND PROJECTION")
    print("=" * 60)

    v1 = FelixVector([1, 0])
    v2 = FelixVector([0, 1])
    v3 = FelixVector([1, 1])
    print(f"\nAngle between {v1} and {v2}: {v1.angle_between(v2):.1f} degrees")
    print(f"Angle between {v1} and {v3}: {v1.angle_between(v3):.1f} degrees")

    a = FelixVector([3, 4])
    b = FelixVector([1, 0])
    proj = a.project_onto(b)
    parallel, residual = a.decompose(b)
    print(f"\na = {a}")
    print(f"b = {b}")
    print(f"proj_b(a) = {proj}")
    print(f"parallel = {parallel}, residual = {residual}")
    print(f"residual dot b = {residual.dot(b):.6f}")


def demonstrate_linear_independence():
    """Demo: Linear independence and Gram-Schmidt"""
    print("\n" + "=" * 60)
    print("  FELIX LINEAR INDEPENDENCE")
    print("=" * 60)

    e1 = FelixVector([1, 0, 0])
    e2 = FelixVector([0, 1, 0])
    e3 = FelixVector([0, 0, 1])
    dep = FelixVector([2, 1, 0])

    vectors_ind = [VectorCoordinates(e1.components, e1.dimension),
                  VectorCoordinates(e2.components, e2.dimension),
                  VectorCoordinates(e3.components, e3.dimension)]
    vectors_dep = [VectorCoordinates(e1.components, e1.dimension),
                   VectorCoordinates(e2.components, e2.dimension),
                   VectorCoordinates(dep.components, dep.dimension)]

    print(f"{{e1, e2, e3}} independent: {IndependenceChecker.is_independent(vectors_ind)}")
    print(f"{{e1, e2, 2*e1+e2}} independent: {IndependenceChecker.is_independent(vectors_dep)}")

    u1 = FelixVector([1, 1, 0])
    u2 = FelixVector([1, 0, 1])
    u3 = FelixVector([0, 1, 1])

    basis_input = [VectorCoordinates(v.components, v.dimension) for v in [u1, u2, u3]]
    basis = OrthogonalizationEngine.gram_schmidt(basis_input)

    print(f"\nGram-Schmidt orthogonalization:")
    for i, vec in enumerate(basis):
        print(f"u{i+1} = {vec}")
    print(f"u1 dot u2 = {basis[0].dot(FelixVector(basis[1].components)):.6f}")


def demonstrate_neural_network_layer():
    """Demo: Matrix-vector multiplication in neural networks"""
    print("\n" + "=" * 60)
    print("  FELIX NEURAL NETWORK LAYER")
    print("=" * 60)

    import random
    random.seed(42)

    weights = FelixMatrix([[random.gauss(0, 0.1) for _ in range(3)] for _ in range(2)])
    input_vec = FelixVector([1.0, 0.5, -0.3])
    output = weights @ input_vec

    print(f"\nInput (3D):  {input_vec}")
    print(f"Output (2D): {output}")
    print("^ This is literally what a neural network layer does.")


if __name__ == "__main__":
    demonstrate_vector_operations()
    demonstrate_angle_projection()
    demonstrate_linear_independence()
    demonstrate_neural_network_layer()
