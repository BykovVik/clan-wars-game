from models import create_all_tables
from clans import ClanController
from users import UserController
from bot import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from game import GameController


@app.on_message()
async def text_handler(client, message):

    # сhecking for service message requests
    if message.text[:1] != "/":
        return

    # checking chat type
    if message.chat.type.name == "CHANNEL":
        return

    # create main objects
    clan_controller = ClanController(message.chat.id)
    clan = clan_controller.get_clan()

    user_controller = UserController(message.from_user.id)
    user = user_controller.get_user()

    # start command handler
    if message.text == "/start" and not message.chat.type.name == "PRIVATE":
        # create button
        button = InlineKeyboardButton("Создать клан", callback_data="add_clan")
        keyboard = InlineKeyboardMarkup([[button]])
        # message reply
        await message.reply_text(
            "Это первый бот для социальной игры в Телеграм!\n\nСпециально для"
            "тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме"
            "👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси"
            "дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в"
            "телеграме и стань первым!👊🏻 ",
            reply_markup=keyboard
        )

    if message.text == "/start" and message.chat.type.name == "PRIVATE":
        await message.reply_text(
            "Это первый бот для социальной игры в Телеграм!\n\nСпециально для"
            "тебя, мы дали возможность бросить вызов любому чату⚔️ в Телеграме"
            "👊\n\nИнтересно? Чтобы начать, ДОБАВЬ меня в любой ЧАТ и попроси"
            "дать мне права АДМИНИСТРАТОРА.\n\n Создай свою тусовку в"
            "телеграме и стань первым!👊🏻 "
        )

    # help command handler
    if message.text == "/help" and not message.chat.type.name == "PRIVATE":

        if clan is None:
            return await message.reply_text(
                "В вашем чате НЕ создан клан, нажмите команду `/start` и"
                "следуйте дальнейшим инструкциям"
            )

        if user is None:
            # create button
            button = InlineKeyboardButton(
                "Играть за этот ЧАТ",
                callback_data="add_player"
            )
            keyboard = InlineKeyboardMarkup([[button]])
            # message reply
            await message.reply_text(
                "Это первый бот для социальной игры в Телеграм!\n\nСпециально"
                "для тебя, мы дали возможность бросить вызов любому чату⚔️ в"
                "Телеграме 👊\n\nИнтересно? Чтобы начать, зарегистрируйся как"
                "игрок в чате, за который ты хочешь играть 👊🏻 ",
                reply_markup=keyboard
            )
        else:
            # create button
            button = InlineKeyboardButton(
                "Удалить аккаунт",
                callback_data="delete_player"
            )
            keyboard = InlineKeyboardMarkup([[button]])
            # message reply
            await message.reply_text(
                "Вы уже зарегистрированы как игрок. Для подробной информации о"
                "вашем аккаунте игрока, вы можите обратится к нашему боту в"
                "личные сообщения, запросив комманду `/info`",
                reply_markup=keyboard
            )

    # info command hendler
    if message.text == "/info" and message.chat.type.name == "PRIVATE":
        # create button
        button_rules = InlineKeyboardButton(
            "Прочитать правила игры",
            callback_data="rules_of_the_game"
        )
        button_account = InlineKeyboardButton(
            "Аккаунт",
            callback_data="account"
        )
        keyboard = InlineKeyboardMarkup([[button_rules, button_account]])
        # message reply
        await message.reply_text(
            "В этом разделе вы можите ознакомиться с правилами игры, а так же"
            "с текущими данными своего игрового аккаунта 👊🏻 ",
            reply_markup=keyboard
        )

    # ckeck other clans command hendler
    if message.text[:6] == "/check" and message.chat.type.name != "PRIVATE":
        if len(message.text) == 6:
            # message reply
            return await message.reply_text(
                "Введите команду `/check`, а за"
                "ней впишите название чата, с которым вы хотите сразиться. "
                "Если такой чат зарегистрировал свой КЛАН в игре, то "
                "произойдет приглашение выбранного КЛАНА для игры с КЛАНом, в "
                "котором состоите вы"
            )

        if clan is None:
            # message reply
            return await message.reply_text(
                "КЛАН с таким именем найден"
                "зарегестрирован в игре, однако в вашем чате НЕ создан клан, "
                "нажмите команду `/start` и следуйте дальнейшим инструкциям"
            )

        title = message.text[7:]

        if title == clan.title:
            # message reply
            return await message.reply_text(
                "Нельзя вызвать на бой, свой же КЛАН."
            )

        # Checking if the selected clan is busy playing
        check_war = clan_controller.get_clan_by_title(title)

        if check_war is None:
            # message reply
            await message.reply_text(
                "Клан с подобным именем не найден, возможно вы допустили"
                "ошибку."
            )
        else:
            # create button
            button = InlineKeyboardButton(
                "Вызвать КЛАН",
                callback_data="battle_{}".format(check_war.chat_id)
            )
            keyboard = InlineKeyboardMarkup([[button]])
            # message reply`
            await message.reply_text(
                "КЛАН с таким именем найден зарегестрирован в игре, хотите"
                "бросить ему вызов? 👊🏻 ",
                reply_markup=keyboard
            )


@app.on_callback_query()
async def callback_answers(client, callback_query):

    # create main objects
    clan_controller = ClanController(callback_query.message.chat.id)
    clan = clan_controller.get_clan()
    user_controller = UserController(callback_query.from_user.id)
    user = user_controller.get_user()

    # add clan query
    if callback_query.data == 'add_clan':
        if clan is None:
            clan_controller.add_clan(
                title=callback_query.message.chat.title,
                chat_id=callback_query.message.chat.id,
                wins=0,
                losses=0,
                rating=0
            )
            await callback_query.answer("Клан вашего чата успешно создан")
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )
        else:
            await callback_query.answer("У вас уже зарегестрирован КЛАН")
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )

    # add player query
    if callback_query.data == 'add_player':
        if user is None:
            user_controller.add_user(
                name=callback_query.from_user.first_name,
                user_id=callback_query.from_user.id,
                clan_id=clan.id,
                clan=clan
            )
            await callback_query.answer(
                "Теперь вы играете за чат в котором вы сейчас находитесь"
            )
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )
        else:
            await callback_query.answer(
                "Вы уже являетесь участником КЛАНа"
            )
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )

    # delete player query
    if callback_query.data == 'delete_player' and user is not None:
        if user is not None:
            await callback_query.answer("Удаление игрока")
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )
            user_controller.delete_user()
        else:
            await callback_query.answer(
                "Ваш аккаунт не зарегистрирован в игре"
            )
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )

    # rules of the game query
    if callback_query.data == 'rules_of_the_game':
        await callback_query.answer("Правила игры")
        await client.delete_messages(
            callback_query.message.chat.id,
            callback_query.message.id
        )
        await client.send_message(
            callback_query.message.chat.id,
            "Правила игры"
        )

    # rules of the game query
    if callback_query.data == 'account':
        if user is None:
            await callback_query.answer("Вы не зарегистрированы в игре")
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )
            await client.send_message(
                callback_query.message.chat.id,
                "Для того что бы заркгистрироваться в игре, вам необходимо"
                "выбрать чат за который вы хотите играть, вызвать в нём "
                "команду `/help`, и зарегистрировать своего юзера в игре."
            )
        else:
            await callback_query.answer("Информация о игроке")
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )
            await client.send_message(
                callback_query.message.chat.id,
                "Юзер инфо"
            )

    # start battle
    if callback_query.data[:6] == "battle":
        if user is not None:
            if user.clan_id == clan.id:
                # calculating id
                defending_clan_id = callback_query.data[7:]
                attacking_clan_id = callback_query.message.chat.id
                # callback answer
                await callback_query.answer("Запрос на битву")
                await client.delete_messages(
                    callback_query.message.chat.id,
                    callback_query.message.id
                )
                # reate new game
                game = GameController(
                    attacking_clan_id,
                    defending_clan_id,
                    client
                )
                await game.start_game()
            else:
                await callback_query.answer(
                    "Вы не можите проявлять активность в чате, за который вы "
                    "не играете!"
                )
        else:
            await callback_query.answer(
                "Вы не можите проявлять активность. Ваш аккаунт не "
                "зарегистрирован в игре"
            )
            await client.delete_messages(
                callback_query.message.chat.id,
                callback_query.message.id
            )


# check database connect
try:
    create_all_tables()
    print("Tables created successfully")
except Exception as e:
    print(e)

app.run()
