from typing import Dict, List, Tuple
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from .ai_model import AIModel
import logging
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class ModelEvaluator:
    def __init__(self, model: AIModel):
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.metrics_history = []
        
    def evaluate_model(self, test_data: List[Dict]) -> Dict:
        """Đánh giá model với test dataset"""
        try:
            # Chuẩn bị dữ liệu test
            X_test = [item['text'] for item in test_data]
            y_true = [item['intent'] for item in test_data]
            
            # Dự đoán
            y_pred = [self.model.predict_intent(text) for text in X_test]
            
            # Tính toán các metrics
            metrics = {
                'accuracy': accuracy_score(y_true, y_pred),
                'classification_report': classification_report(y_true, y_pred, output_dict=True),
                'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
                'timestamp': datetime.now().isoformat()
            }
            
            # Lưu metrics
            self._save_metrics(metrics)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error evaluating model: {str(e)}")
            raise

    def test_response_quality(self, test_queries: List[Dict]) -> Dict:
        """Kiểm tra chất lượng câu trả lời"""
        results = {
            'total_queries': len(test_queries),
            'successful_responses': 0,
            'failed_responses': 0,
            'average_confidence': 0.0,
            'response_times': [],
            'detailed_results': []
        }
        
        try:
            for query in test_queries:
                start_time = datetime.now()
                
                # Lấy response từ model
                response, confidence = self.model.get_response(query['text'])
                
                # Tính thời gian phản hồi
                response_time = (datetime.now() - start_time).total_seconds()
                
                # Đánh giá kết quả
                is_correct = self._evaluate_response(
                    response, 
                    query.get('expected_response'),
                    query.get('expected_intent')
                )
                
                # Cập nhật kết quả
                if is_correct:
                    results['successful_responses'] += 1
                else:
                    results['failed_responses'] += 1
                    
                results['response_times'].append(response_time)
                results['detailed_results'].append({
                    'query': query['text'],
                    'response': response,
                    'confidence': confidence,
                    'response_time': response_time,
                    'is_correct': is_correct
                })
            
            # Tính toán metrics tổng hợp
            results['success_rate'] = results['successful_responses'] / results['total_queries']
            results['average_response_time'] = np.mean(results['response_times'])
            results['average_confidence'] = np.mean([r['confidence'] for r in results['detailed_results']])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error testing responses: {str(e)}")
            raise

    def _evaluate_response(self, 
                         response: str, 
                         expected_response: str = None,
                         expected_intent: str = None) -> bool:
        """Đánh giá một câu trả lời cụ thể"""
        if expected_response:
            # So sánh với câu trả lời mong đợi
            similarity = self.model.calculate_similarity(response, expected_response)
            return similarity > 0.8
        elif expected_intent:
            # Kiểm tra intent
            predicted_intent = self.model.predict_intent(response)
            return predicted_intent == expected_intent
        return True

    def generate_evaluation_report(self, 
                                 metrics: Dict, 
                                 response_results: Dict,
                                 output_dir: str = 'reports') -> str:
        """Tạo báo cáo đánh giá chi tiết"""
        try:
            report = {
                'model_performance': {
                    'accuracy': metrics['accuracy'],
                    'classification_report': metrics['classification_report'],
                },
                'response_quality': {
                    'success_rate': response_results['success_rate'],
                    'average_response_time': response_results['average_response_time'],
                    'average_confidence': response_results['average_confidence']
                },
                'timestamp': datetime.now().isoformat()
            }
            
            # Tạo visualizations
            self._create_confusion_matrix_plot(
                metrics['confusion_matrix'],
                f"{output_dir}/confusion_matrix.png"
            )
            
            self._create_response_time_plot(
                response_results['response_times'],
                f"{output_dir}/response_times.png"
            )
            
            # Lưu báo cáo
            report_path = f"{output_dir}/evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
                
            return report_path
            
        except Exception as e:
            self.logger.error(f"Error generating report: {str(e)}")
            raise

    def _create_confusion_matrix_plot(self, conf_matrix: List[List[int]], output_path: str):
        """Tạo biểu đồ confusion matrix"""
        plt.figure(figsize=(10, 8))
        sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig(output_path)
        plt.close()

    def _create_response_time_plot(self, response_times: List[float], output_path: str):
        """Tạo biểu đồ thời gian phản hồi"""
        plt.figure(figsize=(10, 6))
        plt.hist(response_times, bins=20)
        plt.title('Response Time Distribution')
        plt.xlabel('Response Time (seconds)')
        plt.ylabel('Frequency')
        plt.savefig(output_path)
        plt.close()

    def _save_metrics(self, metrics: Dict):
        """Lưu metrics để theo dõi"""
        self.metrics_history.append(metrics)
        
        # Lưu history
        with open('data/metrics_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.metrics_history, f, ensure_ascii=False, indent=2) 