from pydantic import BaseModel, Field
from datetime import datetime


class QueryCreate(BaseModel):
    cadastral_number: str = Field(..., description='Кадастровый номер')
    latitude: float = Field(..., description='Широта')
    longitude: float = Field(..., description='Долгота')

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'cadastral_number': '1234567890123',
                'latitude': 55.7558,
                'longitude': 37.6173,
            }
        }


class QueryResponse(QueryCreate):
    cadastral_number: str = Field(..., description='Кадастровый номер')
    latitude: float = Field(..., description='Широта')
    longitude: float = Field(..., description='Долгота')
    create_ts: datetime = Field(..., description='Дата и время')

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'id': 1,
                'cadastral_number': '1234567890123',
                'latitude': 55.7558,
                'longitude': 37.6173,
                'create_ts': '2023-10-01 12:34',
            }
        }
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')
        }


class ResultCreate(BaseModel):
    history: bool = Field(..., description='Результат запроса true/false')

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'query_id': 1,
                'history': True,
            }
        }


class ResultResponse(ResultCreate):
    id: int = Field(..., description='ID результата')
    history: bool = Field(..., description='Результат запроса true/false')
    create_ts: datetime = Field(..., description='Дата и время')

    class Config:
        from_attributes=True
        json_schema_extra = {
            'example': {
                'id': 1,
                'query_id': 1,
                'history': True,
                'created_at': '2023-10-01 12:35',
            }
        }
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M')
        }