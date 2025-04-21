import os
import pandas as pd
import numpy as np
from prophet import Prophet
import joblib
from typing import Tuple, List, Dict

from app.services.data_service import get_heat_index_data
from app.config import MODEL_PATH

def train_forecast_model(data: pd.DataFrame) -> Prophet:
    prophet_df = data.rename(columns={'date': 'ds', 'heat_index': 'y'})
    
    model = Prophet(daily_seasonality=True)
    
    if 'temperature' in data.columns:
        model.add_regressor('temperature')
    
    if 'humidity' in data.columns:
        model.add_regressor('humidity')
        
    model.fit(prophet_df)
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    
    joblib.dump(model, MODEL_PATH)
    
    return model

def generate_forecast(days: int = 7, include_history: bool = False) -> Tuple[List[Dict], Dict]:
    data = get_heat_index_data()
    
    if data.empty:
        raise Exception("Failed to retrieve historical data")
    
    try:
        model = joblib.load(MODEL_PATH)
    except:
        model = train_forecast_model(data)
    
    future = model.make_future_dataframe(periods=days, freq='D')
    
    if 'temperature' in data.columns:
        avg_temp = data['temperature'].mean()
        future['temperature'] = avg_temp
        
    if 'humidity' in data.columns:
        avg_humidity = data['humidity'].mean()
        future['humidity'] = avg_humidity
    
    forecast = model.predict(future)
    
    test_size = min(7, len(data))
    train_data = data.iloc[:-test_size]
    test_data = data.iloc[-test_size:]
    
    train_model = Prophet(daily_seasonality=True)
    prophet_train = train_data.rename(columns={'date': 'ds', 'heat_index': 'y'})
    
    if 'temperature' in train_data.columns:
        train_model.add_regressor('temperature')
    
    if 'humidity' in train_data.columns:
        train_model.add_regressor('humidity')
    
    train_model.fit(prophet_train)
    
    test_future = train_model.make_future_dataframe(periods=test_size, freq='D')
    
    if 'temperature' in data.columns:
        for i, row in test_data.iterrows():
            idx = test_future[test_future['ds'] == row['date']].index
            if len(idx) > 0:
                test_future.loc[idx, 'temperature'] = row['temperature']
    
    if 'humidity' in data.columns:
        for i, row in test_data.iterrows():
            idx = test_future[test_future['ds'] == row['date']].index
            if len(idx) > 0:
                test_future.loc[idx, 'humidity'] = row['humidity']
    
    test_forecast = train_model.predict(test_future)
    test_forecast = test_forecast.iloc[-test_size:]
    
    mse = np.mean((test_forecast['yhat'].values - test_data['heat_index'].values) ** 2)
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(test_forecast['yhat'].values - test_data['heat_index'].values))
    
    accuracy_metrics = {
        'mse': float(mse),
        'rmse': float(rmse),
        'mae': float(mae)
    }
    
    if include_history:
        result_df = forecast
    else:
        result_df = forecast.iloc[-days:]
    
    result = []
    for _, row in result_df.iterrows():
        result.append({
            'date': row['ds'].strftime('%Y-%m-%d'),
            'heat_index': round(row['yhat'], 2),
            'heat_index_lower': round(row['yhat_lower'], 2),
            'heat_index_upper': round(row['yhat_upper'], 2)
        })
    
    return result, accuracy_metrics