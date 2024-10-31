from prometheus_client import Counter, Histogram, Gauge
import psutil
import time
from typing import Dict
import logging

# Metrics collectors
REQUEST_COUNT = Counter(
    'chatbot_request_total',
    'Total number of requests received',
    ['endpoint', 'method', 'status']
)

RESPONSE_TIME = Histogram(
    'chatbot_response_time_seconds',
    'Response time in seconds',
    ['endpoint']
)

MODEL_PREDICTION_TIME = Histogram(
    'model_prediction_time_seconds',
    'Time taken for model predictions',
    ['model_type']
)

MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def collect_metrics(self) -> Dict:
        """Thu thập metrics hệ thống"""
        try:
            metrics = {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': psutil.net_io_counters()._asdict()
            }
            
            # Update Prometheus metrics
            CPU_USAGE.set(metrics['cpu_percent'])
            MEMORY_USAGE.set(psutil.virtual_memory().used)
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting metrics: {str(e)}")
            return {}

class ModelMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.performance_metrics = {
            'total_requests': 0,
            'successful_predictions': 0,
            'failed_predictions': 0,
            'average_response_time': 0
        }
        
    def track_prediction(self, start_time: float, success: bool):
        """Track model prediction performance"""
        try:
            duration = time.time() - start_time
            
            self.performance_metrics['total_requests'] += 1
            if success:
                self.performance_metrics['successful_predictions'] += 1
            else:
                self.performance_metrics['failed_predictions'] += 1
                
            # Update average response time
            prev_avg = self.performance_metrics['average_response_time']
            n = self.performance_metrics['total_requests']
            self.performance_metrics['average_response_time'] = (
                (prev_avg * (n-1) + duration) / n
            )
            
            # Record in Prometheus
            MODEL_PREDICTION_TIME.observe(duration)
            
        except Exception as e:
            self.logger.error(f"Error tracking prediction: {str(e)}")

    def get_metrics(self) -> Dict:
        """Get current performance metrics"""
        return {
            **self.performance_metrics,
            'success_rate': (
                self.performance_metrics['successful_predictions'] /
                max(self.performance_metrics['total_requests'], 1)
            )
        } 