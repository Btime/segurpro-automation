import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_GPT = os.getenv('API_KEY_GPT')
AUTHORIZATION = os.getenv('AUTHORIZATION')
CONNECTION_STRING = os.getenv('CONNECTION_STRING')
STATUS_OPEN = [1, 2, 5, 6]
