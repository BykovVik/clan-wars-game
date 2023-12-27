from models import session
from bot import BOT
from telethon import events, Button, types
from clans import ClanController
import asyncio
from telethon.tl.types import InputPeerChat
from telethon.tl.functions.messages import GetMessageReactionsListRequest

#bot 
bot = BOT

class GameController:

    def __init__(self, attacking_clan_id, defending_clan_id) -> None:
        self.session = session
        self.a_clan_controller = ClanController(attacking_clan_id)
        self.d_clan_controller = ClanController(defending_clan_id)
        self.a_clan = self.a_clan_controller.get_clan()
        self.d_clan = self.d_clan_controller.get_clan()

    async def start_game(self):

        a_chat_message = await bot.send_message(self.a_clan.chat_id, "Лукасай этот пост для того что б обыграть своих опонетов")
        d_chat_message = await bot.send_message(self.d_clan.chat_id, "Лукасай этот пост для того что б обыграть своих опонетов")

        await asyncio.sleep(10)
        
        await self.end_game(a_chat_message.id, d_chat_message.id)

    async def end_game(self, a_id, d_id):
        await bot.delete_messages(self.a_clan.chat_id, a_id)
        await bot.delete_messages(self.d_clan.chat_id, d_id)