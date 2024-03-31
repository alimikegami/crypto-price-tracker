from dotenv import load_dotenv
import os

load_dotenv()
class EnvironmentVariables:
    def __init__(self):
        self.db_name = os.getenv("DB_NAME")
        self.currency_api_key = os.getenv("CURRENCY_API_KEY")
        self.crypto_api_url = os.getenv("CRYPTO_API_URL")
        self.currency_api_url = os.getenv("CURRENCY_API_URL")
        self.jwt_secret_key = os.getenv("JWT_SECRET_KEY")
    
def get_environment_variables() -> EnvironmentVariables:
    return EnvironmentVariables()