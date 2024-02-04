from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_AUTH: str

    YANDEX_S3_BUCKET_NAME: str
    YANDEX_S3_ACCESS_KEY_ID: str
    YANDEX_S3_SECRET_ACCESS_KEY: str
    
    @property
    def SUPPORTED_FILE_TYPES(self):
        return {'image/png': 'png','image/jpeg': 'jpeg'}
     
    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"
    
    model_config = SettingsConfigDict(env_file="../env/dev/.env")
    
settings = Settings()