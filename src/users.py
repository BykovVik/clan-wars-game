from .models import get_session, User

class UserController:
    """
    CRUD operations for the user table
    """
    def __init__(self, user_id):
        self.session = get_session()
        self.user_id = user_id
    
    def add_user(self, name, user_id, chat_id):
        player = User(
            name = name,
            user_id = user_id,
            score = 0,
            penalties = 0,
            rating = 0,
            clan_id = chat_id
        )
        self.session.add(player)
        self.session.commit()

    def get_user(self):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        return user
    
    def update_user_name(self, name):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        user.name = name
        self.session.commit()

    def update_user_score(self, score):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        user.score = score
        self.session.commit()

    def update_user_penalties(self, penalties):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        user.penalties = penalties
        self.session.commit()

    def update_user_rating(self, rating):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        user.rating = rating
        self.session.commit()

    def update_user_clan_id(self, chat_id):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        user.clan_id = chat_id
        self.session.commit()

    def delete_user(self, user_id):
        user = self.session.query(User).filter_by(user_id=self.user_id).first()
        self.session.delete(user)
        self.session.commit()