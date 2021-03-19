from app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    environments = db.relationship('Environment', backref='env_user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    env_status = db.Column(db.Integer, index=True)
    status_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    approval_status = db.Column(db.Integer, index=True)
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    timing = (db.Column(db.DateTime))
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    servers = db.relationship('Server', backref='server_in_env', lazy='dynamic')

    def __repr__(self):
        return '<Environment {}>'.format(self.body)


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
        return '<Server {}>'.format(self.body)


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
        return '<Command {}>'.format(self.body)