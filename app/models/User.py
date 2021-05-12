from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """
    The code associated with the Login has been derived from a Flask tutorial
    provided by Miguel Grinberg

    Grinberg, M., 2017. The Flask Mega Tutorial [Online Programming Tutorial]. Available
        from: https://miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
        [Accessed 22 Match 2021]
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    environments = db.relationship('Environment', backref='env_user', lazy='dynamic')

    def __repr__(self):
        """
        Defines how user object is printed
        :return: Formatted User
        """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        Generates password hash
        :param password: User password
        :return: Hashed password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verfies hashed password
        :param password: User password
        :return: True if password match and false if no match
        """
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        """
        Loads user based on user id
        :return:User
        """
        return User.query.get(int(id))