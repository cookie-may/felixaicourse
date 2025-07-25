import numpy as np

class LinearClassifier:
    def __init__(self, num_features, step_size=0.1):
        self.w = np.zeros(num_features)
        self.b = 0.0
        self.step_size = step_size
        
    def forward(self, x):
        return 1 if (np.dot(self.w, x) + self.b) >= 0 else 0
        
    def fit(self, X, Y, max_iter=100):
        for _ in range(max_iter):
            mistakes = 0
            for x_i, y_i in zip(X, Y):
                pred = self.forward(x_i)
                err = y_i - pred
                if err != 0:
                    self.w += self.step_size * err * x_i
                    self.b += self.step_size * err
                    mistakes += 1
            if mistakes == 0:
                break

def execute_logic_gates():
    print("Testing logical gates with Linear Classifier")
    X_and = np.array([[0,0],[0,1],[1,0],[1,1]])
    Y_and = np.array([0,0,0,1])
    model = LinearClassifier(2)
    model.fit(X_and, Y_and)
    print("AND Gate predictions:", [model.forward(x) for x in X_and])
    
    Y_or = np.array([0,1,1,1])
    model_or = LinearClassifier(2)
    model_or.fit(X_and, Y_or)
    print("OR Gate predictions:", [model_or.forward(x) for x in X_and])

if __name__ == '__main__':
    execute_logic_gates()
