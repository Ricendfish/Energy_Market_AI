from pydantic import BaseModel

class PredictionRequest(BaseModel):
    temperature: float
    wind_speed: float
    electricity_demand: float
    day_of_week: int
    month: int
    day_of_year: int
