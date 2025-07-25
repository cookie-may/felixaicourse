import numpy as np

class DenseNetwork:
    def __init__(self, layers_config):
        self.weights = []
        self.biases = []
        for i in range(len(layers_config)-1):
            self.weights.append(np.random.randn(layers_config[i], layers_config[i+1]) * 0.1)
            self.biases.append(np.zeros((1, layers_config[i+1])))
            
    def _sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        
    def _dsigmoid(self, out):
        return out * (1.0 - out)
        
    def train_step(self, X, Y, lr=0.1):
        # Forward
        activations = [X]
        for w, b in zip(self.weights, self.biases):
            z = np.dot(activations[-1], w) + b
            activations.append(self._sigmoid(z))
            
        # Backward
        error = Y - activations[-1]
        loss = np.mean(error**2)
        
        deltas = [error * self._dsigmoid(activations[-1])]
        for i in reversed(range(len(self.weights) - 1)):
            delta = np.dot(deltas[-1], self.weights[i+1].T) * self._dsigmoid(activations[i+1])
            deltas.append(delta)
        deltas.reverse()
        
        # Update
        for i in range(len(self.weights)):
            self.weights[i] += lr * np.dot(activations[i].T, deltas[i])
            self.biases[i] += lr * np.sum(deltas[i], axis=0, keepdims=True)
            
        return loss

def run_xor():
    X = np.array([[0,0],[0,1],[1,0],[1,1]])
    Y = np.array([[0],[1],[1],[0]])
    nn = DenseNetwork([2, 4, 1])
    print("Training DenseNetwork on XOR...")
    for i in range(5000):
        loss = nn.train_step(X, Y, 0.5)
        if i % 1000 == 0:
            print(f"Iteration {i} Loss: {loss:.4f}")
    
    activations = X
    for w, b in zip(nn.weights, nn.biases):
        activations = nn._sigmoid(np.dot(activations, w) + b)
    print("XOR Predictions:", np.round(activations).flatten())

if __name__ == '__main__':
    run_xor()
