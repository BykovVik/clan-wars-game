from models import Clan, session

class ClanController:
    """
    CRUD operations for the clan table
    """

    def __init__(self, chat_id):
        self.session = session
        self.chat_id = chat_id
    
    def add_clan(self, title, chat_id, wins, losses, rating):
        clan = Clan(
            title = title,
            chat_id = chat_id,
            wins = wins,
            losses = losses,
            rating = rating
        )
        self.session.add(clan)
        self.session.commit()

    def get_clan(self):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        return clan
    
    def update_clan_title(self, title):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        clan.title = title,
        self.session.commit()

    def update_clan_wins(self, wins):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        clan.wins = wins
        self.session.commit()

    def update_clan_losses(self, losses):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        clan.losses = losses
        self.session.commit()

    def update_clan_rating(self, rating):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        clan.rating = rating
        self.session.commit()

    def delete_clan(self):
        clan = self.session.query(Clan).filter_by(chat_id=self.chat_id).first()
        self.session.delete(clan)
        self.session.commit()