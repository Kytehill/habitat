from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime
from flask_login import UserMixin


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
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    env_status = db.Column(db.Integer, index=True)
    status_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    approval_status = db.Column(db.Integer, index=True)
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    timing = (db.Column(db.DateTime, default=datetime.utcnow()))
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    servers = db.relationship('Server', backref='server_in_env', lazy='dynamic')

    def __repr__(self):
        environment = '{id: ' + self.id + 'name: ' + self.name + ',' + 'env_status: ' + str(self.env_status) + ',' + 'status_timestamp: ' \
                      + str(self.status_timestamp) + ',' + 'approval_status: ' + str(self.approval_status) + ',' + \
                      'approval_timestamp: ' + str(self.approval_timestamp) + ',' + 'timing: ' + str(self.timing) + '}'
        return environment


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(20), index=True)
    username = db.Column(db.String(64))
    server_status = db.Column(db.Integer, index=True)
    status_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    approval_status = (db.Column(db.Integer, index=True))
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    env_id_fk = db.Column(db.Integer, db.ForeignKey('environment.id'))
    servers = db.relationship('Command', backref='command_in_server', lazy='dynamic')

    def __repr__(self):
        server = '{id: ' + str(self.id) + 'ip_address: ' + self.ip_address + ',' + 'username: ' + self.username + ',' + 'server_status: ' \
                      + str(self.server_status) + ',' + 'status_timestamp: ' + str(self.status_timestamp) + ',' + \
                      'approval_status: ' + str(self.approval_status) + ',' + 'approval_timestamp: ' + str(self.approval_timestamp)
        return server


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(200), index=True)
    expectation = db.Column(db.String(200), index=True)
    command_status = db.Column(db.Integer, index=True)
    status_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    approval_status = (db.Column(db.Integer, index=True))
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    server_id_fk = db.Column(db.Integer, db.ForeignKey('server.id'))

    def __repr__(self):
        command = '{id: ' + str(self.id) + 'command: ' + self.command + ',' + 'expectation: ' + self.expectation + ',' + 'command_status: ' \
                 + str(self.command_status) + ',' + 'status_timestamp: ' + str(self.status_timestamp) + ',' + \
                 'approval_status: ' + str(self.approval_status) + ',' + 'approval_timestamp: ' + str(self.approval_timestamp) + '}'
        return command