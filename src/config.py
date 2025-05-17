from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    spotify_client_id: str = Field(..., env="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str = Field(..., env="SPOTIFY_CLIENT_SECRET")
    perplexity_api_key: str = Field(..., env="PERPLEXITY_API_KEY")
    milvus_host: str = Field("localhost", env="MILVUS_HOST")
    milvus_port: int = Field(19530, env="MILVUS_PORT")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    cache_ttl: int = Field(3600, env="CACHE_TTL")
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()