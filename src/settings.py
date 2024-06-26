from pydantic import Field
from pydantic_settings import BaseSettings
import logging

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "mikelv702-terraform backend"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Storage settings
    STORAGE_TYPE: str = Field(default="file", 
                              env="STORAGE_TYPE")  # Options: "file", "database"
    FILE_STORAGE_PATH: str = Field(default="terraform_states",
                                   env="FILE_STORAGE_PATH")
    # TODO: Implment Database backend
    # DATABASE_URL: Optional[str] = Field(default=None, env="DATABASE_URL")

    # Lock settings
    LOCK_TIMEOUT: int = Field(default=300, env="LOCK_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def configure_logging(self):
        logging.basicConfig(
            level=getattr(logging, self.LOG_LEVEL),
            format=self.LOG_FORMAT
        )

settings = Settings()