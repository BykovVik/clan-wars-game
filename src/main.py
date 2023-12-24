from telethon import TelegramClient, events, Button
from dotenv import load_dotenv
import os
from models import create_all_tables
from clans import ClanController
from telethon.tl.functions.messages import DeleteMessagesRequest

load_dotenv()
bot = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))


@bot.on(events.NewMessage(pattern='/start'))
async def start_command(event):

    if event.is_private:
        return

    controller = ClanController(event.chat.id)
    clan = controller.get_clan()

    if clan is None:
        await event.respond(
            "Это первый бот для социальной игры в Телеграм!\n\nСпециально для тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме 👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в телеграме и стань первым!👊🏻 ",
            buttons = [
                [Button.inline('Создать свой КЛАН', b'add_clan')]
            ]
        )
    else:
        await event.reply('Клан уже создан')


@bot.on(events.NewMessage(pattern='/help'))
async def help_command(event):

    if event.is_private:
        return
    
    controller = ClanController(event.chat.id)
    clan = controller.get_clan()

    if clan is None:
        await event.reply("В вашем чате НЕ создан клан, нажмите команду `/start` и следуйте дальнейшим инструкциям")
    else:
        await event.reply("Вспомогательная информация")

@bot.on(events.CallbackQuery)
async def callback_answers(event):

    #delete button afyer click
    await bot.delete_messages(event.chat.id, event.message_id)

    #add clan query
    if event.data == b'add_clan':
        controller = ClanController(event.chat.id)
        controller.add_clan(
            title = event.chat.title,
            chat_id = event.chat.id,
            wins = 0,
            losses = 0,
            rating = 0
        )
        await event.answer("Клан вашего чата успешно создан")

#check database connect
try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

bot.run_until_disconnected()