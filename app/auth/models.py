from email_validator import EmailNotValidError, validate_email
from sqlalchemy import Boolean, ForeignKey, String, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db.database import BaseModel


class Role(BaseModel):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    users: Mapped[list['User']] = relationship(back_populates='role')

    def __repr__(self):
        return f'Role: id={self.id}, name={self.name})'


class User(BaseModel):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
        )
    first_name: Mapped[str] = mapped_column(
        String(50), nullable=False
        )   
    last_name: Mapped[str] = mapped_column(
        String(50), nullable=False
        )
    password: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
        )
    email: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
        )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True
        )
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'), default=1, server_default=text('1')
        )

    role: Mapped['Role'] = relationship(
        'Role', back_populates='users', lazy='joined')

    @hybrid_property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email не может быть пустым')
        try:
            valid_email = validate_email(email, check_deliverability=False)
            email = valid_email.normalized
        except EmailNotValidError as e:
            raise ValueError(f'Неверный формат email: {e}')
        return email

    def __repr__(self) -> str:
        return f'Username: {self.username}, First_name: {self.first_name}'