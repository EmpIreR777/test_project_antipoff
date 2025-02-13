from typing import List
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.database import BaseModel


class Query(BaseModel):
    __tablename__ = 'queries'

    cadastral_number: Mapped[str] = mapped_column(
        String(14), nullable=False
        )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    history: Mapped[List['History']] = relationship('History', back_populates='query')

    @validates('cadastral_number')
    def validate_cadastral_number(cls, key, value):
        if not value.isdigit() or len(value) not in (13, 14):
            raise ValueError('Кадастровый номер должен содержать 13 или 14 цифр')
        return value

    def __repr__(self) -> str:
        return f'Cadastral number: {self.cadastral_number}, History: {self.history}'


class History(BaseModel):
    __tablename__ = 'histories'

    query_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('queries.id'), index=True
        )
    history: Mapped[bool] = mapped_column(
        Boolean, nullable=False)

    query: Mapped['Query'] = relationship('Query', back_populates='history')

    def __repr__(self) -> str:
        return f'Query id: {self.query_id}, History: {self.history}'
