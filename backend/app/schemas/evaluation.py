from pydantic import BaseModel
from typing import List, Dict, Optional

class EvaluationRequest(BaseModel):
    test_data: List[Dict]
    evaluation_type: Optional[str] = "full"  # full, quick, custom

class EvaluationResponse(BaseModel):
    message: str
    status: str
    evaluation_id: Optional[str] = None

class TestResult(BaseModel):
    query: str
    response: str
    confidence: float
    response_time: float
    is_correct: bool

class EvaluationResult(BaseModel):
    accuracy: float
    classification_report: Dict
    confusion_matrix: List[List[int]]
    response_quality: Dict
    timestamp: str 