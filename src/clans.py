from models import get_session, Clan

Session = get_session()

class ClanController:
    """
    CRUD operations for the clan table
    """
    
    def add_clan(self, title, chat_id, wins, losses, rating):
        clan = Clan(
            title = title,
            chat_id = chat_id,
            wins = wins,
            losses = losses,
            rating = rating
        )
        Session.add(clan)
        Session.commit()

    def get_clan(self, chat_id):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        return clan
    
    def update_clan(self, title, chat_id, wins, losses, rating):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        clan.title = title,
        chat_id=chat_id
        clan.wins = wins,
        clan.losses = losses,
        clan.rating = rating
        Session.commit()

    def delete_clan(self, chat_id):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        Session.delete(clan)
        Session.commit()