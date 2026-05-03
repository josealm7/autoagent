from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # LLM
    groq_api_key: str = Field("", env="GROQ_API_KEY")
    llm_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.1
    max_tokens: int = 8000

    # Email
    email_sender: str = Field("", env="EMAIL_SENDER")
    email_password: str = Field("", env="EMAIL_PASSWORD")

    # Vector store
    vector_store: str = Field("chroma", env="VECTOR_STORE")
    chroma_persist_dir: str = Field("./data/chroma_db", env="CHROMA_PERSIST_DIR")
    similarity_threshold: float = Field(0.1, env="SIMILARITY_THRESHOLD")
    retrieval_k: int = 4

    # App
    app_env: str = Field("development", env="APP_ENV")
    allowed_origins: str = Field("http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500,null", env="ALLOWED_ORIGINS")

    # Agent
    max_iterations: int = Field(8, env="MAX_AGENT_ITERATIONS")
    agent_timeout: int = Field(60, env="AGENT_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    return Settings()
