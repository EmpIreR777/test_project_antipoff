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

#         from pydantic import BaseModel, Field, field_validator


# class QueryCreate(BaseModel):
#     cadastral_number: str = Field(..., description='Кадастровый номер')
#     latitude: float = Field(..., description='Широта')
#     longitude: float = Field(..., description='Долгота')

#     @field_validator('cadastral_number')
#     def validate_cadastral_number(cls, value):
#         if not value.isdigit():
#             raise ValueError('Кадастровый номер должен содержать только цифры')
#         if len(value) not in (13, 14):
#             raise ValueError('Кадастровый номер должен содержать 13 или 14 цифр')
#         return value

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             'example': {
#                 'cadastral_number': '12345678901011',
#                 'latitude': 55.7558,
#                 'longitude': 37.6173,
#             }
#         }

# class QueryResponse(QueryCreate):
#     id: int = Field(..., description='ID запроса')

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             'example': {
#                 'id': 1,
#                 'cadastral_number': '12345678901011',
#                 'latitude': 55.7558,
#                 'longitude': 37.6173,
#             }
#         }

# class ResultCreate(BaseModel):
#     query_id: int = Field(..., description='ID запроса')
#     history: bool = Field(..., description='Результат запроса')

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             'example': {
#                 'query_id': 1,
#                 'history': True,
#             }
#         }

# class ResultResponse(ResultCreate):
#     id: int = Field(..., description='ID результата')
#     query_id: int = Field(..., description='ID запроса')
#     history: bool = Field(..., description='Результат Rtue либо False')

#     class Config:
#         orm_mode = True
#         schema_extra = {
#             'example': {
#                 'id': 1,
#                 'query_id': 1,
#                 'history': True,
#             }
#         }