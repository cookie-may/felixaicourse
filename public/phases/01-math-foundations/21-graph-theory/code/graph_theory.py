import numpy as np

class NetworkGraph:
    def __init__(self, size, is_directed=False):
        self.size = size
        self.is_directed = is_directed
        self.matrix = np.zeros((size, size))

    def connect(self, u, v, w=1.0):
        self.matrix[u, v] = w
        if not self.is_directed:
            self.matrix[v, u] = w

    def get_laplacian(self):
        degrees = np.diag(np.sum(self.matrix, axis=1))
        return degrees - self.matrix

def traverse_bfs(net, start_node):
    queue = [start_node]
    seen = {start_node}
    path = []
    while queue:
        curr = queue.pop(0)
        path.append(curr)
        for neighbor, weight in enumerate(net.matrix[curr]):
            if weight > 0 and neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return path

def compute_pagerank(net, alpha=0.85, iters=100):
    n = net.size
    p = np.ones(n) / n
    out_degree = np.sum(net.matrix, axis=1)
    
    transition = np.zeros_like(net.matrix)
    for i in range(n):
        if out_degree[i] > 0:
            transition[i] = net.matrix[i] / out_degree[i]
            
    for _ in range(iters):
        p = alpha * (transition.T @ p) + (1 - alpha) / n
    return p

def run_graph_showcase():
    print("Graph theory algorithms initialized.")
    g = NetworkGraph(5)
    g.connect(0, 1)
    g.connect(1, 2)
    g.connect(2, 3)
    g.connect(3, 4)
    print("BFS Path:", traverse_bfs(g, 0))
    print("PageRank:", compute_pagerank(g))

if __name__ == '__main__':
    run_graph_showcase()
