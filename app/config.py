import os
from dotenv import load_dotenv

load_dotenv()

email_from = os.getenv("EMAIL_FROM")
brevo_api_key = os.getenv("BREVO_API_KEY")
secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
database_url = os.getenv("DATABASE_URL")