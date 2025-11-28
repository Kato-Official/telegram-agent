import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# App configuration
# Default values are provided for local testing if .env is missing, 
# but for production, these should be in .env
API_ID = int(os.getenv('TELEGRAM_API_ID', '38605265'))
API_HASH = os.getenv('TELEGRAM_API_HASH', 'e7171b5b7e50d8640aa4d56f0c65f6a2')
SESSION_NAME = os.getenv('TELEGRAM_SESSION_NAME', 'circle_dxb_session')
SERVER_PORT = int(os.getenv('PORT', '8001'))
