from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"  # Default model, can be overridden by user selection
    openai_temperature: float = 0.4
    openai_max_tokens: int = 4000

    # Available models for user selection
    available_models: dict[str, dict[str, str]] = {
        "gpt-4o-mini": {
            "name": "GPT-4o Mini",
            "description": "⚡ ÖNERİLEN - Güvenilir ve hızlı",
            "speed": "Orta",
            "cost": "Düşük",
            "release": "2024",
            "status": "✓ Kullanılabilir"
        },
        "gpt-4.1-mini": {
            "name": "GPT-4.1 Mini",
            "description": "🔥 Güçlü ve ekonomik",
            "speed": "Hızlı",
            "cost": "Düşük",
            "release": "Nisan 2025",
            "status": "✓ Kullanılabilir"
        },
        "gpt-5-mini": {
            "name": "gpt-5-mini",
            "description": "🧪 DENEYSEL - Henüz API'de olmayabilir",
            "speed": "Hızlı",
            "cost": "Düşük",
            "release": "Ağustos 2025",
            "status": "⚠ Deneysel"
        },
        "gpt-5": {
            "name": "GPT-5",
            "description": "🧪 DENEYSEL - En yeni model (API'de olmayabilir)",
            "speed": "Orta",
            "cost": "Yüksek",
            "release": "Ağustos 2025",
            "status": "⚠ Deneysel"
        },
        "gpt-5-nano": {
            "name": "gpt-5-nano",
            "description": "🧪 DENEYSEL - Henüz API'de olmayabilir",
            "speed": "Çok Hızlı",
            "cost": "Çok Düşük",
            "release": "Ağustos 2025",
            "status": "⚠ Deneysel"
        },
        "o4-mini": {
            "name": "o4-mini (Reasoning)",
            "description": "🧪 DENEYSEL - Akıl yürütme modeli",
            "speed": "Yavaş",
            "cost": "Orta",
            "release": "İlkbahar 2025",
            "status": "⚠ Deneysel"
        }
    }

    # API Configuration
    api_title: str = "Product Photo Agent API"
    api_version: str = "1.0.0"
    api_description: str = "AI-powered product photo shoot planning agent"

    # File Upload Configuration
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_types: set[str] = {".jpg", ".jpeg", ".png", ".webp"}

    # CORS Configuration
    # Use "*" for development, specific origins for production
    # Example: "http://localhost:3000,https://yourdomain.com"
    cors_origins: str = "*"
    cors_allow_credentials: bool = True

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        if self.cors_origins == "*":
            return ["*"]
        # Split by comma and strip whitespace
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


# Global settings instance
settings = Settings()
