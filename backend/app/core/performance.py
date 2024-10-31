from functools import lru_cache
import time
from typing import Any, Callable
import asyncio
from concurrent.futures import ThreadPoolExecutor
import psutil

class PerformanceMonitor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._metrics = {}

    def measure_time(self, func: Callable) -> Callable:
        """Decorator để đo thời gian thực thi"""
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log metrics
            func_name = func.__name__
            if func_name not in self._metrics:
                self._metrics[func_name] = []
            self._metrics[func_name].append(execution_time)
            
            return result
        return wrapper

    def get_system_metrics(self) -> dict:
        """Thu thập metrics hệ thống"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        }

    @lru_cache(maxsize=1000)
    def get_average_response_time(self, func_name: str) -> float:
        """Lấy thời gian phản hồi trung bình"""
        if func_name in self._metrics:
            return sum(self._metrics[func_name]) / len(self._metrics[func_name])
        return 0.0

performance_monitor = PerformanceMonitor() 