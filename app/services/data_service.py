import pandas as pd
from app.database import engine
from app.config import HISTORY_DAYS

def get_heat_index_data(days=HISTORY_DAYS):
    query = f"""
    SELECT recordedAt, temperature, humidity, heatIndex 
    FROM heat_index_measurements
    WHERE recordedAt >= DATE_SUB(NOW(), INTERVAL {days} DAY)
    ORDER BY recordedAt
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()