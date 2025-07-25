import numpy as np

def detect_outliers_zscore(dataset, limit=3.0):
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    sigma[sigma == 0] = 1e-6
    z = np.abs((dataset - mu) / sigma)
    max_z = np.max(z, axis=1)
    return max_z > limit, max_z

def detect_outliers_iqr(dataset, multiplier=1.5):
    pct25, pct75 = np.percentile(dataset, [25, 75], axis=0)
    iqr_val = pct75 - pct25
    iqr_val[iqr_val == 0] = 1e-6
    lower_bound = pct25 - multiplier * iqr_val
    upper_bound = pct75 + multiplier * iqr_val
    is_outlier = np.any((dataset < lower_bound) | (dataset > upper_bound), axis=1)
    return is_outlier

def isolation_forest_mock(dataset, num_trees=50):
    n_samples, n_feats = dataset.shape
    scores = np.zeros(n_samples)
    
    for _ in range(num_trees):
        feature = np.random.randint(n_feats)
        split_val = np.random.uniform(np.min(dataset[:, feature]), np.max(dataset[:, feature]))
        
        for i in range(n_samples):
            if dataset[i, feature] > split_val:
                scores[i] += 1
                
    return scores / num_trees

def execute_anomaly_demos():
    print("Anomaly Detection Toolkit")
    data = np.random.randn(1000, 3)
    data[0] = [10, 10, 10]
    
    z_mask, z_vals = detect_outliers_zscore(data)
    print("Found via Z-Score:", np.sum(z_mask))
    
    iqr_mask = detect_outliers_iqr(data)
    print("Found via IQR:", np.sum(iqr_mask))

if __name__ == '__main__':
    execute_anomaly_demos()
