"""Конфигурация приложения на основе переменных окружения."""

from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
    app_title: str = Field('Название', validation_alias='APP_TITLE')
    secret: str = Field(..., validation_alias='SECRET')

    # DatdBase
    db_user: str = Field(..., validation_alias='POSTGRES_USER')
    db_password: SecretStr = Field(..., validation_alias='POSTGRES_PASSWORD',)
    db_name: str = Field(..., validation_alias='POSTGRES_DB')
    db_host: str = Field('localhost', validation_alias='POSTGRES_HOST')
    db_port: int = Field(5432, validation_alias='POSTGRES_PORT')

    # Admin
    first_superuser_email: Optional[EmailStr] = Field(
        None,
        validation_alias='FIRST_SUPERUSER_EMAIL'
    )
    first_superuser_username: Optional[str] = Field(
        None,
        validation_alias='FIRST_SUPERUSER_USERNAME'
    )
    first_superuser_password: Optional[SecretStr] = Field(
        None,
        validation_alias='FIRST_SUPERUSER_PASSWORD'
    )

    @property
    def db_url(self) -> str:
        """Возвращает безопасный DSN для SQLAlchemy."""
        return (
            f'postgresql+asyncpg://{self.db_user}:'
            f'{self.db_password.get_secret_value()}'
            f'@{self.db_host}:{self.db_port}/{self.db_name}'
        )


settings = Settings()
