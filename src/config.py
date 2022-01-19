import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_API_ID = os.getenv('CLIENT_ID')
CLIENT_API_HASH = os.getenv('CLIENT_HASH')


BOT_TOKEN = os.getenv('BOT_TOKEN')


SERVER_DOMAIN_OR_IP = 'https://1d1c-212-112-122-110.ngrok.io'

SERVER_PORT = 5000

SERVER_HOST = '0.0.0.0'