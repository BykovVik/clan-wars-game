from models import session
from clans import ClanController
import asyncio


class GameController:

    def __init__(self, attacking_clan_id, defending_clan_id, client) -> None:
        self.session = session
        self.bot = client
        self.a_clan_controller = ClanController(attacking_clan_id)
        self.d_clan_controller = ClanController(defending_clan_id)
        self.a_clan = self.a_clan_controller.get_clan()
        self.d_clan = self.d_clan_controller.get_clan()

    async def start_game(self):

        a_chat_message = await self.bot.send_message(
            self.a_clan.chat_id,
            "Лукасай этот пост для того что б обыграть своих опонетов АТАКА"
        )
        d_chat_message = await self.bot.send_message(
            self.d_clan.chat_id,
            "Лукасай этот пост для того что б обыграть своих опонетов"
        )

        await asyncio.sleep(10)
        message = await self.bot.get_messages(
            self.a_clan.chat_id,
            a_chat_message.id
        )
        await self.end_game(message.id, d_chat_message.id)

    async def end_game(self, a_id, d_id):
        await self.bot.delete_messages(self.a_clan.chat_id, a_id)
        await self.bot.delete_messages(self.d_clan.chat_id, d_id)
