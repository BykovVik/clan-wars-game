from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()
BOT = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))