import math
import cmath
import os

def create_complex(r, i=0.0): return complex(r, i)
def magnitude(c): return abs(c)
def phase(c): return cmath.phase(c)
def to_polar(c): return cmath.polar(c)
def from_polar(r, theta): return cmath.rect(r, theta)
def get_roots_of_unity(n): return [cmath.exp(2j * math.pi * k / n) for k in range(n)]

def compute_discrete_fourier_transform(signal_arr):
    n_samples = len(signal_arr)
    return [
        sum(signal_arr[t] * cmath.exp(-2j * math.pi * freq * t / n_samples) for t in range(n_samples))
        for freq in range(n_samples)
    ]

def compute_inverse_dft(spectrum_arr):
    n_samples = len(spectrum_arr)
    return [
        sum(spectrum_arr[freq] * cmath.exp(2j * math.pi * freq * t / n_samples) for freq in range(n_samples)) / n_samples
        for t in range(n_samples)
    ]

def run_demos():
    print("Complex Math Operations Showcase")
    c1, c2 = complex(3, 2), complex(1, 4)
    print("Sum:", c1 + c2)
    print("Product:", c1 * c2)
    print("Magnitude of c1:", magnitude(c1))
    
    print("\nDFT Test")
    sample = [1.0, 0.0, -1.0, 0.0]
    freq_domain = compute_discrete_fourier_transform(sample)
    print("Frequencies:", freq_domain)
    
if __name__ == "__main__":
    run_demos()
