import numpy as np

class ImageProcessor:
    def __init__(self):
        self.mean_stats = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        self.std_stats = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def to_grayscale(self, image_tensor):
        coeffs = np.array([0.299, 0.587, 0.114], dtype=np.float32)
        return np.dot(image_tensor[..., :3].astype(np.float32), coeffs).astype(np.uint8)

    def layout_to_channel_first(self, image_tensor):
        return np.transpose(image_tensor, (2, 0, 1))

    def normalize_for_resnet(self, image_tensor):
        float_img = image_tensor.astype(np.float32) / 255.0
        normalized = (float_img - self.mean_stats) / self.std_stats
        return self.layout_to_channel_first(normalized)

def demo_image_ops():
    print("Executing Image Processing Operations...")
    proc = ImageProcessor()
    np.random.seed(42)
    mock_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    gray = proc.to_grayscale(mock_img)
    print(f"Grayscale shape: {gray.shape} | Mean pixel val: {np.mean(gray):.2f}")
    
    norm = proc.normalize_for_resnet(mock_img)
    print(f"Normalized CHW shape: {norm.shape} | Normalized mean: {np.mean(norm):.2f}")

if __name__ == '__main__':
    demo_image_ops()
