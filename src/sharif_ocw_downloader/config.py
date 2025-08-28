"""Environment configuration - ALL from .env."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment Detection
    ENVIRONMENT: str = Field(...)  # ... means REQUIRED
    APP_VERSION: str = Field(
        ...,
        description="Application version",
    )
    # Application Settings (prefixed)
    OCW_BOT_NAME: str = Field(...)
    OCW_BASE_URL: str = Field(...)
    OCW_API_TIMEOUT: float = Field(..., ge=1.0, le=600.0)
    OCW_OUTPUT_PATH: str = Field(...)
    OCW_USE_ORDINALS: bool = Field(...)
    OCW_OVERWRITE_EXISTING: bool = Field(...)
    OCW_MAX_FILENAME_LENGTH: int = Field(..., ge=1, le=255)

    # Concurrency Settings
    CONCURRENT_REQUESTS: int = Field(..., ge=1, le=100)
    CONCURRENT_REQUESTS_PER_DOMAIN: int = Field(..., ge=1, le=50)
    DOWNLOAD_DELAY: float = Field(..., ge=0.0, le=60.0)
    RANDOMIZE_DOWNLOAD_DELAY: bool = Field(...)

    # Download Settings
    DOWNLOAD_TIMEOUT: int = Field(..., ge=1, le=600)
    DOWNLOAD_MAXSIZE: int = Field(..., gt=0)
    DOWNLOAD_WARNSIZE: int = Field(..., gt=0)

    # Retry Settings
    RETRY_ENABLED: bool = Field(...)
    RETRY_TIMES: int = Field(..., ge=0, le=10)
    OCW_RETRY_HTTP_CODES: str = Field(...)  # Comma-separated

    # Logging
    LOG_ENABLED: bool = Field(...)
    LOG_LEVEL: str = Field(...)
    LOG_STDOUT: bool = Field(...)
    LOG_ENCODING: str = Field(...)

    # Monitoring
    STATS_DUMP: bool = Field(...)
    OCW_STATS_ENABLED: bool = Field(...)
    OCW_PROGRESS_ENABLED: bool = Field(...)

    # Security Settings
    TELNETCONSOLE_ENABLED: bool = Field(...)
    COOKIES_ENABLED: bool = Field(...)
    ROBOTSTXT_OBEY: bool = Field(...)

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level against Scrapy standards."""
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid:
            raise ValueError(f"Invalid log level: {v}")
        return v.upper()

    def get_retry_codes(self) -> list:
        """Parse comma-separated retry codes into a list of integers."""
        return [
            int(x.strip())
            for x in self.OCW_RETRY_HTTP_CODES.split(",")
        ]


# Single instance
config = EnvConfig()
