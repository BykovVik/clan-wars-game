from .models import get_session, User

Session = get_session()

class UserController:
    """
    CRUD operations for the user table
    """
    
    def add_user(self, name, user_id, chat_id):
        player = User(
            name = name,
            user_id = user_id,
            score = 0,
            penalties = 0,
            rating = 0,
            clan_id = chat_id
        )
        Session.add(player)
        Session.commit()

    def get_user(self, user_id):
        user = Session.query(User).filter_by(user_id=user_id)
        return user
    
    def update_user(self, name, user_id, score, penalties, rating, chat_id):
        user = Session.query(User).filter_by(user_id=user_id)
        user.name = name,
        user.user_id = user_id,
        user.score = score,
        user.penalties = penalties,
        user.rating = rating,
        user.clan_id = chat_id
        Session.commit()

    def delete_user(self, user_id):
        user = Session.query(User).filter_by(user_id=user_id)
        Session.delete(user)
        Session.commit()