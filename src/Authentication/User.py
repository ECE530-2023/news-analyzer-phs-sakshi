from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email):
        self.id = email

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
