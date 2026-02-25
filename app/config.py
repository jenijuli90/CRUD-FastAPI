from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    database_hostname: str
    secret_key : str
    access_token_expire_minutes : int
    algorithm : str

    #read from .env
    model_config = SettingsConfigDict(env_file= ".env")


settings = Settings()

