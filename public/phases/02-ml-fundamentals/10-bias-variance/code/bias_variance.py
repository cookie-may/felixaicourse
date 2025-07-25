import numpy as np

def generate_synthetic(n, variance):
    x = np.random.uniform(-3, 3, n)
    y = np.sin(1.5 * x) + 0.5 * x + np.random.normal(0, np.sqrt(variance), n)
    return x, y

def poly_features(x, degree):
    return np.vander(x, degree + 1, increasing=True)

def train_ridge(X, y, alpha=0.0):
    if alpha == 0:
        return np.linalg.pinv(X) @ y
    I = np.eye(X.shape[1])
    I[0, 0] = 0
    return np.linalg.inv(X.T @ X + alpha * I) @ X.T @ y

def evaluate_bias_variance(degrees_list, iterations=100):
    test_x = np.linspace(-3, 3, 200)
    true_y = np.sin(1.5 * test_x) + 0.5 * test_x
    
    for d in degrees_list:
        preds = []
        for _ in range(iterations):
            tx, ty = generate_synthetic(40, 0.25)
            X_train = poly_features(tx, d)
            w = train_ridge(X_train, ty)
            preds.append(poly_features(test_x, d) @ w)
            
        preds = np.array(preds)
        mean_p = preds.mean(axis=0)
        bias2 = np.mean((mean_p - true_y)**2)
        var = np.mean(preds.var(axis=0))
        print(f"Degree {d} | Bias^2: {bias2:.4f} | Variance: {var:.4f}")

def run_bv_analysis():
    print("Running Bias-Variance Analysis...")
    evaluate_bias_variance([1, 3, 5, 9])

if __name__ == '__main__':
    run_bv_analysis()
