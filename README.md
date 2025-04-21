# Heat Index Forecast API

A FastAPI application for heat index forecasting with authentication.

## Features

- JWT authentication for user access
- API key authentication for internal service communication
- Heat index forecast using Facebook Prophet
- Historical data access
- Model accuracy metrics

## Project Structure

```
/heat_index_api/
├── .env                   # Environment variables
├── main.py               # Entry point
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── models/               # Saved model files
│   └── __init__.py
├── app/                  # Application code
│   ├── __init__.py
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── dependencies.py   # FastAPI dependencies
│   ├── models/           # Data models
│   │   ├── __init__.py
│   │   └── schemas.py    # Pydantic schemas
│   ├── api/              # API routes
│   │   ├── __init__.py
│   │   ├── api.py        # Main API router
│   │   ├── endpoints/    # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py   # Authentication endpoints
│   │   │   ├── forecast.py # Forecast endpoints
│   │   │   ├── data.py   # Data endpoints
│   │   │   └── internal.py # Internal API endpoints
│   ├── core/             # Core functions
│   │   ├── __init__.py
│   │   ├── auth.py       # Authentication logic
│   │   └── security.py   # Security functions
│   └── services/         # Business logic
│       ├── __init__.py
│       ├── data_service.py # Data access
│       └── forecast_service.py # Forecasting logic
```

## Setup

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure environment variables in `.env` file
5. Run the application:
   ```
   python main.py
   ```

## API Endpoints

### Authentication

- `POST /api/v1/auth/token` - Get JWT token
- `GET /api/v1/auth/users/me` - Get current user info

### Data

- `GET /api/v1/data/historical` - Get historical heat index data

### Forecast

- `POST /api/v1/forecast` - Generate heat index forecast
- `GET /api/v1/forecast/health` - Health check

### Internal API (for service-to-service communication)

- `POST /api/v1/internal/forecast` - Generate forecast (API key auth)

## Environment Variables

- `SECRET_KEY` - JWT secret key
- `INTERNAL_API_KEY` - API key for internal services
- `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME` - Database configuration
- `MODEL_PATH` - Path to save the Prophet model
- `HISTORY_DAYS` - Default number of days for historical data

## Authentication

### User Authentication (JWT)

For regular user access, use JWT authentication:

1. Get a token:

   ```
   curl -X POST "http://localhost:8000/api/v1/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=testpassword"
   ```

2. Use the token in subsequent requests:
   ```
   curl -X POST "http://localhost:8000/api/v1/forecast" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"days": 7}'
   ```

### Service Authentication (API Key)

For service-to-service communication:

```
curl -X POST "http://localhost:8000/api/v1/internal/forecast" \
  -H "X-API-Key: YOUR_INTERNAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"days": 7}'
```
