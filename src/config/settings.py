from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL:str
       # modifying the base model settings
    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
Config=Settings()
print(Config.DATABASE_URL)