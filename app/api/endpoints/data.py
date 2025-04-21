from fastapi import APIRouter, HTTPException
from app.models.schemas import HeatIndexResponse
from app.services.data_service import get_heat_index_data

router = APIRouter()

@router.get("/historical", response_model=HeatIndexResponse)
async def get_historical_data(
    days: int = 90, 
):
    data = get_heat_index_data(days)
    if data.empty:
        raise HTTPException(status_code=404, detail="No data found")
    
    result = []
    for _, row in data.iterrows():
        result.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'temperature': float(row['temperature']),
            'humidity': float(row['humidity']),
            'heat_index': float(row['heat_index'])
        })
    
    return {"data": result}