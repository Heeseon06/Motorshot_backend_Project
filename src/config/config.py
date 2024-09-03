from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    db_uri: str = Field(..., env='DB_URI')
    db_name: str = Field(..., env='DB_NAME')
    
    # JWT settings
    jwt_secret_key: str = Field(..., env='JWT_SECRET_KEY')
    jwt_expires_in_sec: int = Field(default=172800, env='JWT_EXPIRES_IN_SEC')
    
    # Bcrypt settings
    bcrypt_salt_rounds: int = Field(default=10, env='BCRYPT_SALT_ROUNDS')
    
    # Host settings
    host_port: int = Field(default=8080, env='HOST_PORT')

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 설정 인스턴스 생성
settings = Settings()
