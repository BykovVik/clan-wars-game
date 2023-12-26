from models import create_all_tables
from clans import ClanController
from users import UserController
from bot import BOT
from telethon import events, Button
from game import GameController

bot = BOT


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
        await event.reply('Это первый бот для социальной игры в Телеграм!\n\nСпециально для тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме 👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в телеграме и стань первым!👊🏻 ')


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


    #ckeck other clans command hendler
    if event.message.message[:6] == "/check" and not event.is_private:
        if len(event.message.message) == 6:
            await event.reply("Введите команду `/check`, а за ней впишите название чата, с которым вы хотите сразиться. Если такой чат зарегистрировал свой КЛАН в игре, то произойдет приглашение выбранного КЛАНА для игры с КЛАНом, в котором состоите вы")
        else:
            if clan is None:
                await event.reply("КЛАН с таким именем найден зарегестрирован в игре, однако в вашем чате НЕ создан клан, нажмите команду `/start` и следуйте дальнейшим инструкциям")
            else:
                title = event.message.message[7:]
                if title == clan.title:
                    await event.reply("Нельзя вызвать на бой, свой же КЛАН.")
                    return

                check_war = clan_controller.get_clan_by_title(title)
                if check_war is None:
                    await event.reply("Клан с подобным именем не найден, возможно вы допустили ошибку.")
                else:
                    await event.respond(
                    "КЛАН с таким именем найден зарегестрирован в игре, хотите бросить ему вызов? 👊🏻 ",
                    buttons = [
                        [Button.inline('Вызвать КЛАН', "battle_{}".format(check_war.chat_id))]
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
        if clan is None:
            clan_controller.add_clan(
                title = event.chat.title,
                chat_id = event.chat.id,
                wins = 0,
                losses = 0,
                rating = 0
            )
            await event.answer("Клан вашего чата успешно создан")
            await bot.delete_messages(event.chat.id, event.message_id)
        else:
            await event.answer("У вас уже зарегестрирован КЛАН")
            await bot.delete_messages(event.chat.id, event.message_id)

    #add player query
    if event.data == b'add_player':
        if user is None:
            user_controller.add_user(
                name = event.sender_id,
                user_id = event.sender_id,
                clan_id = clan.id,
                clan = clan
            )
            await event.answer("Теперь вы играете за чат в котором вы сейчас находитесь")
            await bot.delete_messages(event.chat.id, event.message_id)
        else:
            await event.answer("Вы уже являетесь участником КЛАНа")
            await bot.delete_messages(event.chat.id, event.message_id)

    #delete player query
    if event.data == b'delete_player' and user is not None:
        if user is not None:
            await event.answer("Удаление игрока")
            await bot.delete_messages(event.chat.id, event.message_id)
            user_controller.delete_user()
        else:
            await event.answer("Ваш аккаунт не зарегистрирован в игре")
            await bot.delete_messages(event.chat.id, event.message_id)

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

    #start battle
    if event.data[:6] == b"battle":
        if user is not None:
            #calculating id
            defending_clan_id = event.data[7:].decode('utf-8')
            attacking_clan_id = event.chat.id
            #callback answer
            await event.answer("Запрос на битву")
            await bot.delete_messages(event.chat.id, event.message_id)
            #create new game
            game = GameController(attacking_clan_id, defending_clan_id)
            await game.start_game()
        else:
            await event.answer("Вы не можите проявлять активность. Ваш аккаунт не зарегистрирован в игре")
            await bot.delete_messages(event.chat.id, event.message_id)

#check database connect
try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

bot.run_until_disconnected()