from pydantic_settings import BaseSettings
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values

def load_environment():
  
   SECRET_FILE = Path("/etc/secret-xmas/.env.secret")
   CONFIG_FILE = Path("/etc/config-xmas/.env.config")
   LOCAL_ENV_FILE = Path(__file__).parent / ".env"

   
   for env_file in [SECRET_FILE, CONFIG_FILE, LOCAL_ENV_FILE]:
      if env_file.exists():
         load_dotenv(dotenv_path=env_file, override=True)
         env_vars = dotenv_values(dotenv_path=env_file)
         os.environ.update(env_vars)         
      else:
         print(f"@core/load_environment: skipped {env_file} (not found)")

   print("@core/load_environment: DATABASE_URL =", os.getenv("DATABASE_URL"))


load_environment()

class Settings(BaseSettings):   
   DATABASE_URL: str
   ALLOWED_ORIGINS: str
   SECRET_KEY: str
   ALGORITHM: str
   ACCESS_TOKEN_EXPIRE_MINUTES: int
   TICKETMASTER_CONSUMER_KEY: str
   TICKETMASTER_CONSUMER_SECRET: str

   class Config:     
      extra = "ignore"
      
settings = Settings()