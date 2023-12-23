from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from models import create_all_tables

load_dotenv()
bot = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))


@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.reply('Hello world')

try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

bot.run_until_disconnected()