from bot import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from pyrogram import filters
from game import GameController
import requests


# start command handler
@app.on_message(filters.command(["start"]))
async def start_command(client, message):
    # check chat status
    if message.chat.type.name == "PRIVATE":
        web_app_url = "https://bykovvik.github.io/clan-wars-twa-gitpage"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Open Web App", 
                        web_app=WebAppInfo(url=web_app_url)
                    )
                ]
            ]
        )
        await message.reply("Click the button below to open the Web App:", reply_markup=keyboard)
    else:
        button_reg_clan = InlineKeyboardButton(
            "Зарегистрировать чат в игре",
            callback_data="clan_reg"
        )
        keyboard = InlineKeyboardMarkup([
            
            [button_reg_clan]
        ])
        # message reply
        await message.reply_text(
            "После регистрации в игре, ваш чат становится полноценным участником сражений и вас могут вызвать на битву в любое время суток.👊🏻 ",
            reply_markup=keyboard
        )


# help command handler
@app.on_message(filters.command(["help"]))
async def help_command(client, message):

    if not message.chat.type.name == "PRIVATE":
        pass
    else:
        pass


@app.on_callback_query()
async def callback_answers(client, callback_query):
    if callback_query.data == 'clan_reg':
        chat_id = int(callback_query.message.chat.id)
        chat_title = str(callback_query.message.chat.title)
        requests.post("http://127.0.0.1:8000/clan/", json={
            "title": chat_title,
            "chat_id": chat_id,
            "wins": 0,
            "losses": 0,
        })
        await callback_query.answer("Клан вашего чата успешно создан")
        await client.delete_messages(
            callback_query.message.chat.id,
            callback_query.message.id
        )

    if callback_query.data.split(":")[0] == 'no_battle':
        await callback_query.answer("Вам отказали")
        await client.delete_messages(
            callback_query.message.chat.id,
            callback_query.message.id
        )
        await client.send_message(callback_query.from_user.id,
            "Клан, который вы вызывали, отказал вам в битве")
        




    """game = GameController(
        attacking_clan_id,
        defending_clan_id,
        client
        )
    await game.start_game()"""
        


# info command handler
"""@app.on_message(filters.command(["info"]))
async def info_command(client, message):
    # check chat status
    if not message.chat.type.name == "PRIVATE":
        # create button
        button_rules = InlineKeyboardButton(
            "Прочитать правила игры",
            callback_data="rules_of_the_game"
        )
        button_account = InlineKeyboardButton(
            "Аккаунт",
            callback_data="account"
        )
        button_clan_info = InlineKeyboardButton(
            "Наш клан",
            callback_data="clan"
        )
        button_clan_rate = InlineKeyboardButton(
            "Рейтинг кланов",
            callback_data="clan_rate"
        )
        keyboard = InlineKeyboardMarkup([
            [button_rules], 
            [button_account], 
            [button_clan_info],
            [button_clan_rate]
        ])
        # message reply
        await message.reply_text(
            "В этом разделе вы можите ознакомиться с правилами игры, а так же"
            "с текущими данными своего игрового аккаунта 👊🏻 ",
            reply_markup=keyboard
        )
        

@app.on_message(filters.regex(r"^/check"))
async def text_handler(client, message):
    # ckeck other clans command hendler
    if message.chat.type.name != "PRIVATE":
        # create main objects
        clan_controller = ClanController(message.chat.id)
        clan = clan_controller.get_clan()
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
        
    # clan query
    if callback_query.data == 'clan':
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
            if clan:
                await callback_query.answer("Информация о КЛАНЕ")
                await client.delete_messages(
                    callback_query.message.chat.id,
                    callback_query.message.id
                )
                await client.send_message(
                    callback_query.message.chat.id,
                    "Название: {} \n"
                    "Победы: {} \n"
                    "Поражения: {} \n"
                    "Рейтинг: {} \n"
                    .format(clan.title, clan.wins, clan.losses, clan.rating)
                )
            else:
                await callback_query.answer("КЛАН не зареган")

    # clan rating query
    if callback_query.data == 'clan_rate':
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
            if clan:
                await callback_query.answer("Рейтинг кланов")
                await client.delete_messages(
                    callback_query.message.chat.id,
                    callback_query.message.id
                )
                # create rating
                clans = clan_controller.get_all_clans()
                rating = sorted(clans, key=lambda clan: clan.rating)
                message_text = ""
                count = 0
                for c in reversed(rating):
                    if count <= 10:
                        message_text += "{} : {} \n".format(c.title, c.rating)
                        count += 1

                await client.send_message(
                    callback_query.message.chat.id,
                    message_text
                )
            else:
                await callback_query.answer("КЛАН не зареган")
    
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
            )"""

app.run()
