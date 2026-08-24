from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Python Computer Vision API Kit"
    app_env: str = "development"
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    cors_allowed_origins: str = "http://127.0.0.1:3000,http://localhost:3000"
    max_upload_size_mb: int = 8
    sample_max_detections: int = 8

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            value.strip()
            for value in self.cors_allowed_origins.split(",")
            if value.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
