import logging
import sys
from typing import Optional

from pydantic import BaseSettings, EmailStr

logging.basicConfig(
    handlers=[logging.StreamHandler(sys.stdout)],
    format=(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    ),
    level=logging.INFO
)


class Settings(BaseSettings):
    app_title: str = 'Приложения для сбора пожертвований'
    app_description: str = 'Приложение для сбора пожертвований на любые цели,'\
                           ' связанные с поддержкой  кошачьей популяции'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'vaniamaksimov'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
logger = logging.getLogger(__name__)
