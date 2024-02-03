from models import session
from clans import ClanController
import asyncio
import requests
import json


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
        # http://localhost:8000/messages/-1001414907164/34193
        a_url = f"http://localhost:8000/messages/{self.a_clan.chat_id}/{a_chat_message.id}"
        d_url = f"http://localhost:8000/messages/{self.d_clan.chat_id}/{d_chat_message.id}"
        a_count = requests.get(a_url)
        b_count = requests.get(d_url)
        a = json.loads(a_count.text)['reactions_count']
        b = json.loads(b_count.text)['reactions_count']
        await self.end_game(a_chat_message.id, d_chat_message.id)

    async def end_game(self, a_id, d_id):
        await self.bot.delete_messages(self.a_clan.chat_id, a_id)
        await self.bot.delete_messages(self.d_clan.chat_id, d_id)
