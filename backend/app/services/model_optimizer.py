import torch
import numpy as np
from typing import List, Tuple

class ModelOptimizer:
    def __init__(self, model):
        self.model = model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
        # Quantization
        if self.device.type == 'cpu':
            self.model = torch.quantization.quantize_dynamic(
                self.model,
                {torch.nn.Linear},
                dtype=torch.qint8
            )
            
    def optimize_batch_size(self, inputs: List[str]) -> int:
        """Tìm batch size tối ưu"""
        memory = torch.cuda.get_device_properties(0).total_memory if self.device.type == 'cuda' else psutil.virtual_memory().total
        input_size = sum(len(x) for x in inputs)
        return min(32, max(1, memory // (input_size * 4)))

    @torch.no_grad()
    def batch_predict(self, inputs: List[str]) -> List[str]:
        """Dự đoán theo batch"""
        batch_size = self.optimize_batch_size(inputs)
        results = []
        
        for i in range(0, len(inputs), batch_size):
            batch = inputs[i:i + batch_size]
            batch_tensor = self.preprocess(batch).to(self.device)
            outputs = self.model(batch_tensor)
            results.extend(self.postprocess(outputs))
            
        return results

    def preprocess(self, texts: List[str]) -> torch.Tensor:
        """Tiền xử lý input theo batch"""
        # Implement preprocessing logic
        pass

    def postprocess(self, outputs: torch.Tensor) -> List[str]:
        """Hậu xử lý output theo batch"""
        # Implement postprocessing logic
        pass 