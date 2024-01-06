import os

from dotenv import load_dotenv

load_dotenv()
PRIVATE_APP_CREDENTIALS = os.getenv('HS_PRIVATE_APP_CREDENTIALS')