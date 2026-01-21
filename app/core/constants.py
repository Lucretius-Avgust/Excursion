import os
from app.core.config import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
"""Дериктория корня."""

LOG_DIR = os.path.join(BASE_DIR, "logs")
"""Дериктория для логирования."""

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
"""Формат для логов."""

USERNAME_LEN = 50
"""Длина имени."""

EMAIL_LEN = 128
"""Длина электронной почты."""

PHONE_LEN = 12
"""Длина телефона."""

HASHED_PASSWORD_LEN = 128
"""Длина хэшированного пароля."""

PASSWORD_LEN_MIN = 8
"""Длина пароля минимальное."""

PASSWORD_LEN_MAX = 255
"""Длина пароля максимальное."""

SECRET_KEY = settings.secret
"""Секретный ключ."""

ALGORITHM = "HS256"
"""Алгоритм."""

ACCESS_TOKEN_EXPIRE_MINUTES = 30
"""Время жизни токена короткого токена."""

REFRESH_TOKEN_EXPIRE_DAYS = 30
"""Время жизни токена длинного токена."""
