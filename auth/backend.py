import firebase_admin
from firebase_admin import credentials, auth
import os
from logger import logger

# Path to your service account key
# We look for the file in the secrets folder
SECRETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "secrets")
# Find the json file that looks like the firebase key
try:
    cred_files = [f for f in os.listdir(SECRETS_DIR) if f.startswith("telegram-kato") and f.endswith(".json")]
    if cred_files:
        CRED_PATH = os.path.join(SECRETS_DIR, cred_files[0])
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred)
        logger.info(f"Firebase Admin Initialized with {cred_files[0]}")
    else:
        logger.warning("No Firebase Admin SDK key found in secrets folder.")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin: {e}")

def verify_token(id_token):
    """
    Verifies the ID token sent from the client.
    Returns the decoded token (dict) if valid, None otherwise.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return None
