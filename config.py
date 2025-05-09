from dotenv import load_dotenv

import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
SYMBOLS = list(os.getenv("SYMBOLS").split(","))