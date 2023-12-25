from models import session
from bot import BOT
from telethon import events, Button
from clans import ClanController

bot = BOT

class Game:

    def __init__(self, attacking_clan_id, defending_clan_id) -> None:
        self.session = session
        self.a_clan_controller = ClanController(attacking_clan_id)
        self.d_clan_controller = ClanController(defending_clan_id)
        self.a_clan = self.a_clan_controller.get_clan()
        self.d_clan = self.d_clan_controller.get_clan()
    