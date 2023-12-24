from telethon import TelegramClient, events, Button
from dotenv import load_dotenv
import os
from models import create_all_tables
from clans import ClanController
from users import UserController

load_dotenv()
bot = TelegramClient('bot', os.getenv("API_ID"), os.getenv("API_HASH")).start(bot_token=os.getenv("TOKEN"))


@bot.on(events.NewMessage())
async def start_command(event):

    #сhecking for service message requests
    if event.message.message[:1] != "/":
        return

    #create main objects
    clan_controller = ClanController(event.chat.id)
    clan = clan_controller.get_clan()

    user_controller = UserController(event.message.sender.id)
    user = user_controller.get_user()



    #start command handler
    if event.message.message == "/start" and not event.is_private:

        if clan is None:
            await event.respond(
                "Это первый бот для социальной игры в Телеграм!\n\nСпециально для тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме 👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в телеграме и стань первым!👊🏻 ",
                buttons = [
                    [Button.inline('Создать свой КЛАН', b'add_clan')]
                ]
            )
        else:
            await event.reply('Клан уже создан')

    if event.message.message == "/start" and event.is_private:
        await event.reply('"Это первый бот для социальной игры в Телеграм!\n\nСпециально для тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме 👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в телеграме и стань первым!👊🏻 ')



    #help command handler
    if event.message.message == "/help" and not event.is_private:

        if clan is None:
            await event.reply("В вашем чате НЕ создан клан, нажмите команду `/start` и следуйте дальнейшим инструкциям")
        else:
            if user is None:
                await event.respond(
                    "Это первый бот для социальной игры в Телеграм!\n\nСпециально для тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме 👊\n\nИнтересно? Чтобы начать, зарегистрируйся как игрок в чате, за который ты хочешь играть 👊🏻 ",
                    buttons = [
                        [Button.inline('Играть за этот ЧАТ', b'add_player')]
                    ]
                )
            else:
                await event.respond(
                    "Вы уже зарегистрированы как игрок. Для подробной информации о вашем аккаунте игрока, вы можите обратится к нашему боту в личные сообщения, запросив комманду `/info`",
                    buttons = [
                        [Button.inline('Удалить аккаунт', b'delete_player')]
                    ]
                )



    #info command hendler
    if event.message.message == "/info" and event.is_private:
        await event.respond(
                "В этом разделе вы можите ознакомиться с правилами игры, а так же с текущими данными своего игрового аккаунта 👊🏻 ",
                buttons = [
                    [Button.inline('Прочитать правила игры', b'rules_of_the_game')],
                    [Button.inline('Аккаунт', b'account')]
                ]
            )

@bot.on(events.CallbackQuery)
async def callback_answers(event):

    #create main objects
    clan_controller = ClanController(event.chat.id)
    clan = clan_controller.get_clan()
    user_controller = UserController(event.sender_id)
    user = user_controller.get_user()

    #add clan query
    if event.data == b'add_clan':
        clan_controller.add_clan(
            title = event.chat.title,
            chat_id = event.chat.id,
            wins = 0,
            losses = 0,
            rating = 0
        )
        await event.answer("Клан вашего чата успешно создан")
        await bot.delete_messages(event.chat.id, event.message_id)

    #add player query
    if event.data == b'add_player':
        user_controller.add_user(
            name = event.sender_id,
            user_id = event.sender_id,
            clan_id = clan.id,
            clan = clan
        )
        await event.answer("Теперь вы играете за чат в котором вы сейчас находитесь")
        await bot.delete_messages(event.chat.id, event.message_id)

    #delete player query
    if event.data == b'delete_player':
        await event.answer("Удаление игрока")
        await bot.delete_messages(event.chat.id, event.message_id)
        user_controller.delete_user()

    #rules of the game query
    if event.data == b'rules_of_the_game':
        await event.answer("Правила игры")
        await bot.delete_messages(event.chat.id, event.message_id)
        await bot.send_message(event.chat.id, "Правила игры")

    #rules of the game query
    if event.data == b'account':
        if user is None:
            await event.answer("Вы не зарегистрированы в игре")
            await bot.delete_messages(event.chat.id, event.message_id)
            await bot.send_message(event.chat.id, "Для того что бы заркгистрироваться в игре, вам необходимо выбрать чат за который вы хотите играть, вызвать в нём команду `/help`, и зарегистрировать своего юзера в игре.")
        else:
            await event.answer("Информация о игроке")
            await bot.delete_messages(event.chat.id, event.message_id)
            await bot.send_message(event.chat.id, "Юзер инфо")

    

#check database connect
try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

bot.run_until_disconnected()