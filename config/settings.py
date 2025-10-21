from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.4
    openai_max_tokens: int = 4000

    # API Configuration
    api_title: str = "Product Photo Agent API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered product photo shoot planning agent"

    # File Upload Configuration
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_types: set[str] = {".jpg", ".jpeg", ".png", ".webp"}

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
