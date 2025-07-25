import numpy as np

def principal_component_analysis(data, num_components):
    mu = np.mean(data, axis=0)
    centered_data = data - mu
    u, s, vh = np.linalg.svd(centered_data, full_matrices=False)
    components = vh[:num_components]
    projected = centered_data @ components.T
    return projected, components, mu

def inverse_pca(projected_data, components, mu):
    return (projected_data @ components) + mu

def rbf_kernel_pca(data, num_components, gamma=1.0):
    sq_dists = np.sum(data**2, axis=1).reshape(-1, 1) + np.sum(data**2, axis=1) - 2 * np.dot(data, data.T)
    K = np.exp(-gamma * sq_dists)
    n = K.shape[0]
    one_mat = np.ones((n, n)) / n
    K_centered = K - one_mat.dot(K) - K.dot(one_mat) + one_mat.dot(K).dot(one_mat)
    evals, evecs = np.linalg.eigh(K_centered)
    
    idx = np.argsort(evals)[::-1]
    top_evals = evals[idx][:num_components]
    top_evecs = evecs[:, idx][:num_components]
    
    return top_evecs * np.sqrt(np.maximum(top_evals, 0))

def showcase_dimensionality_reduction():
    print("Executing dimensionality reduction techniques...")
    synth_data = np.random.randn(100, 5)
    reduced, comps, mu = principal_component_analysis(synth_data, 2)
    print("Reduced shape:", reduced.shape)
    reconstructed = inverse_pca(reduced, comps, mu)
    print("Reconstruction error:", np.mean((synth_data - reconstructed)**2))

if __name__ == '__main__':
    showcase_dimensionality_reduction()
