import os
from dotenv import load_dotenv

load_dotenv()

API_V1_STR = "/api/data-analysis-v1"
PROJECT_NAME = "Heat Index Forecast API"

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")
DB_NAME = os.getenv("DB_NAME", "heat_index_db")
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

MODEL_PATH = os.getenv("MODEL_PATH", "models/heat_index_model.pkl")
HISTORY_DAYS = int(os.getenv("HISTORY_DAYS", "90"))