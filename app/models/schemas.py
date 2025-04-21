from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class HeatIndexData(BaseModel):
    date: datetime
    temperature: float
    humidity: float
    heat_index: float

class HeatIndexRecord(BaseModel):
    date: str
    temperature: float
    humidity: float
    heat_index: float

class HeatIndexResponse(BaseModel):
    data: List[HeatIndexRecord]

class ForecastRequest(BaseModel):
    days: int = 7
    include_history: bool = False

class ForecastItem(BaseModel):
    date: str
    heat_index: float
    heat_index_lower: float
    heat_index_upper: float

class AccuracyMetrics(BaseModel):
    mse: float
    rmse: float
    mae: float

class ForecastResponse(BaseModel):
    forecast: List[ForecastItem]
    model_accuracy: Optional[AccuracyMetrics] = None

class HealthCheck(BaseModel):
    status: str
    timestamp: str