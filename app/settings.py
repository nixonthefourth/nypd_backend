from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MYSQL_HOST: str
    MYSQL_USER: str
    MYSQL_DATABASE: str
    MYSQL_PASSWORD: str

settings = Settings() # pyright: ignore[reportCallIssue]
