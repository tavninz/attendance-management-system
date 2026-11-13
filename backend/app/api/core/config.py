from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Attendance Management System"
    VERSION: str = "1.0.0"
    
    # Database URL (e.g., PostgreSQL or SQLite)
    DATABASE_URL: str = "sqlite:///./sql_app.db"  # Change to postgresql://user:pass@localhost/db for production
    
    # Security / JWT
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()