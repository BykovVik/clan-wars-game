from ..models import get_session, Clan

Session = get_session()

class ClanController:
    """
    CRUD operations for the clan table
    """
    
    def add_clan(self, title, score, rating):
        clan = Clan(
            title = title,
            score = score,
            rating = rating
        )
        Session.add(clan)
        Session.commit()

    def get_clan(self, chat_id):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        return clan
    
    def update_clan(self, title, chat_id, score, rating):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        clan.title = title,
        chat_id=chat_id
        clan.score = score,
        clan.rating = rating
        Session.commit()

    def delete_clan(self, chat_id):
        clan = Session.query(Clan).filter_by(chat_id=chat_id)
        Session.delete(clan)
        Session.commit()