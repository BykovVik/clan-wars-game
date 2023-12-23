from telethon import TelegramClient, events
from dotenv import load_dotenv
import os
from models import create_all_tables

load_dotenv()
bot = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))


@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):
    
    if not event.is_private:
        await event.reply('Это первый бот для социальной игры в Телеграм!\n" "\n" "Специально для тебя мы прикрутили лайки❤️, дали возможность стать лидером клана👑 и бросить вызов любому чату⚔️ в Телеграме 👊" "\n" "\n" "Интересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси дать мне права АДМИНИСТРАТОРА. " "\n" "\n" "Создай свою тусовку в телеграме и стань первым!👊🏻 ')

try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

bot.run_until_disconnected()