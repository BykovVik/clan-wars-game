from telethon import TelegramClient, events
from dotenv import load_dotenv
import os

load_dotenv()
bot = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))


@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    await event.reply('Hello world')

bot.run_until_disconnected()