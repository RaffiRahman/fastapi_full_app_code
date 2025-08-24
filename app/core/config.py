from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    #Database settings
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SQL_DEBUG: bool = False
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800
    SECRET_KEY: str = "change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"
    # Add other settings here, e.g., for email server
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    # CORS and Security Settings
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://frontend:3000,http://example.com"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1,testserver,backend,frontend"
    ADMIN_ALLOWED_IPS_STR: str = ""

    # File upload settings
    UPLOAD_DIR: str = "uploads"
    REDIS_URL: str = "redis://localhost:6379/0"
    TESTING: bool = False

    @property
    def ALLOWED_ORIGINS_LIST(self) -> list[str]:  # noqa: N802
        return [item.strip() for item in self.ALLOWED_ORIGINS.split(",") if item.strip()]

    @property
    def ALLOWED_HOSTS_LIST(self) -> list[str]:  # noqa: N802
        return [item.strip() for item in self.ALLOWED_HOSTS.split(",") if item.strip()]

    @property
    def ADMIN_ALLOWED_IPS(self) -> list[str]:  # noqa: N802
        return [item.strip() for item in self.ADMIN_ALLOWED_IPS_STR.split(",") if item.strip()]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
