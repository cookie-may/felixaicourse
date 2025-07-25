import random
import math

def calculate_factorial(num):
    return math.factorial(num)

def pdf_gaussian(val, mean_val, std_dev):
    return (1.0 / (std_dev * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((val - mean_val) / std_dev) ** 2)

def pmf_poisson(k, lambd):
    return (lambd ** k) * math.exp(-lambd) / calculate_factorial(k)

def draw_bernoulli(prob_success, num_draws=1):
    return [1 if random.random() < prob_success else 0 for _ in range(num_draws)]

def compute_softmax(vector):
    max_v = max(vector)
    exp_v = [math.exp(v - max_v) for v in vector]
    sum_exp = sum(exp_v)
    return [e / sum_exp for e in exp_v]

def demonstrate_probs():
    print("Running probability distributions engine...")
    sm = compute_softmax([1.0, 2.0, 3.0])
    print("Softmax output:", sm)
    print("Gaussian PDF at 0:", pdf_gaussian(0, 0, 1))

if __name__ == '__main__':
    demonstrate_probs()
