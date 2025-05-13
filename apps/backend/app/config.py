from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "local"
    project_name: str = "Gibsey"

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

@lru_cache
def get_settings() -> Settings:  # dependency‑friendly
    return Settings()