from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List
from app.services.model_evaluator import ModelEvaluator
from app.core.logging import logger
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_model(
    request: EvaluationRequest,
    background_tasks: BackgroundTasks
):
    """
    Đánh giá model với test dataset
    """
    try:
        evaluator = ModelEvaluator()
        
        # Chạy đánh giá trong background
        background_tasks.add_task(
            evaluator.evaluate_model,
            request.test_data
        )
        
        return {
            "message": "Model evaluation started",
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error starting evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/evaluation-results/{evaluation_id}")
async def get_evaluation_results(evaluation_id: str):
    """
    Lấy kết quả đánh giá
    """
    try:
        evaluator = ModelEvaluator()
        results = evaluator.get_evaluation_results(evaluation_id)
        
        if not results:
            raise HTTPException(status_code=404, detail="Evaluation not found")
            
        return results
    except Exception as e:
        logger.error(f"Error getting evaluation results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-responses")
async def test_model_responses(
    test_queries: List[Dict],
    background_tasks: BackgroundTasks
):
    """
    Kiểm tra chất lượng câu trả lời của model
    """
    try:
        evaluator = ModelEvaluator()
        
        # Chạy test trong background
        background_tasks.add_task(
            evaluator.test_response_quality,
            test_queries
        )
        
        return {
            "message": "Response testing started",
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error starting response testing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 