# ================= IMPORTS =================
import sys
from dotenv import load_dotenv
from .logics import os
from google import genai
from google.genai import errors
from .configs import logger
from .logics import types, wait



def load_gmni():
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    return API_KEY

def load_tg():
    load_dotenv()
    TOKEN = os.getenv("TG_TOKEN")
    BOT_USERNAME = os.getenv("TG_BOT_USERNAME")

    return TOKEN, BOT_USERNAME

def get_env_data():
    """gets api key from .env file"""
    try:
        API_KEY = load_gmni()
        client = genai.Client(api_key=API_KEY)
        client.models.generate_content(
            model="gemini-3-flash-preview",
            contents="",
            config = types.GenerateContentConfig(
                max_output_tokens=1
            ),
        )
        wait(1)
        logger.info("API-key successfully loaded")

    except errors.ClientError as e:
        wait(1)
        logger.error(f"error while loading API-Key: {e.message}")
        sys.exit(1)
    return client
