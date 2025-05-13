from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "local"
    project_name: str = "Gibsey"
    supabase_url: str
    supabase_key: str = ""  # Will be populated from SUPABASE_ANON_KEY

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
        "env_mapping": {
            "supabase_url": "SUPABASE_URL",
            "supabase_key": "SUPABASE_ANON_KEY"
        }
    }

@lru_cache
def get_settings() -> Settings:  # dependency‑friendly
    return Settings()