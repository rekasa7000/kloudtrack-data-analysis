from fastapi import APIRouter, HTTPException

from app.models.schemas import ForecastRequest, ForecastResponse
from app.services.forecast_service import generate_forecast

router = APIRouter()

@router.post("", response_model=ForecastResponse)
async def create_forecast(
    request: ForecastRequest,
):
    try:
        forecast_data, accuracy = generate_forecast(
            days=request.days,
            include_history=request.include_history
        )
        return {"forecast": forecast_data, "model_accuracy": accuracy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Forecast error: {str(e)}")

@router.get("/health")
async def health_check():
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}