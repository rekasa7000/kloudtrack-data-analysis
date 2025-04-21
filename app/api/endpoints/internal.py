from fastapi import APIRouter, Depends, HTTPException, status
from app.models.schemas import ForecastRequest, ForecastResponse
from app.services.forecast_service import generate_forecast

router = APIRouter()

@router.post("/forecast", response_model=ForecastResponse)
async def internal_forecast(
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