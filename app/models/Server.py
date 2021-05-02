from app import db
from datetime import datetime


class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(20), index=True)
    username = db.Column(db.String(64))
    server_status = db.Column(db.Integer, index=True)
    status_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    approval_status = (db.Column(db.Integer, index=True))
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    connection_status = (db.Column(db.Integer))
    env_id_fk = db.Column(db.Integer, db.ForeignKey('environment.id'))
    servers = db.relationship('Command', backref='command_in_server', lazy='dynamic')

    def __repr__(self):
        server = '{id: ' + str(self.id) + 'ip_address: ' + self.ip_address + ',' + 'username: ' + self.username + ',' + 'server_status: ' \
                      + str(self.server_status) + ',' + 'status_timestamp: ' + str(self.status_timestamp) + ',' + \
                      'approval_status: ' + str(self.approval_status) + ',' + 'approval_timestamp: ' + str(self.approval_timestamp)
        return server
