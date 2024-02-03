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
        # creating a message for the attacking clan
        a_chat_message = await self.bot.send_message(
            self.a_clan.chat_id,
            "Лукасай этот пост для того что б обыграть своих опонетов АТАКА"
        )
        # creating a message for the protecting clan
        d_chat_message = await self.bot.send_message(
            self.d_clan.chat_id,
            "Лукасай этот пост для того что б обыграть своих опонетов"
        )
        # add timer
        await asyncio.sleep(10)
        # creaye URLs
        a_url = "http://localhost:8000/messages/{}/{}".format(self.a_clan.chat_id, a_chat_message.id)
        d_url = "http://localhost:8000/messages/{}/{}".format(self.d_clan.chat_id, d_chat_message.id)
        # get reactions objects
        a = requests.get(a_url)
        b = requests.get(d_url)
        # get reactions count
        a_count = json.loads(a.text)['reactions_count']
        b_count = json.loads(b.text)['reactions_count']
        # end game content
        await self.end_game(a_chat_message.id, d_chat_message.id, a_count, b_count)

    async def end_game(self, a_id, d_id, a_count, b_count):
        # delete game messages
        await self.bot.delete_messages(self.a_clan.chat_id, a_id)
        await self.bot.delete_messages(self.d_clan.chat_id, d_id)
        # calculate the winner
        if a_count > b_count:
            self.a_clan_controller.update_clan_wins(self.a_clan.wins + 1)
            self.d_clan_controller.update_clan_losses(self.d_clan.losses + 1)
            #add rating
            self.a_clan_controller.update_clan_rating(self.a_clan.rating + 1)
            if self.d_clan.rating != 0:
                self.d_clan_controller.update_clan_rating(self.d_clan.rating - 1)
        elif a_count < b_count:
            self.a_clan_controller.update_clan_losses(self.a_clan.losses + 1)
            self.d_clan_controller.update_clan_wins(self.d_clan.wins + 1)
            #add rating
            self.d_clan_controller.update_clan_rating(self.d_clan.rating + 1)
            if self.a_clan.rating != 0:
                self.a_clan_controller.update_clan_rating(self.a_clan.rating - 1)
        elif a_count == b_count:
            self.a_clan_controller.update_clan_wins(self.a_clan.wins + 1)
            self.d_clan_controller.update_clan_wins(self.d_clan.wins + 1)

