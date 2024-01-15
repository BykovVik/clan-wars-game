from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()
app = Client('bot', os.getenv("API_ID"), os.getenv("API_HASH"), bot_token=os.getenv("TOKEN"))