from app import db
from datetime import datetime


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    env_status = db.Column(db.Integer, index=True, default=1)
    status_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    approval_status = db.Column(db.Integer, index=True, default=1)
    approval_timestamp = (db.Column(db.DateTime, index=True, default=datetime.utcnow))
    timing = (db.Column(db.Integer, default=30))
    connection_status = (db.Column(db.Integer))
    user_id_fk = db.Column(db.Integer, db.ForeignKey('user.id'))
    servers = db.relationship('Server', backref='server_in_env', lazy='dynamic')

    def __repr__(self):
        environment = '{id: ' + str(self.id) + 'name: ' + self.name + ',' + 'env_status: ' + str(self.env_status) + ',' + 'status_timestamp: ' \
                      + str(self.status_timestamp) + ',' + 'approval_status: ' + str(self.approval_status) + ',' + \
                      'approval_timestamp: ' + str(self.approval_timestamp) + ',' + 'timing: ' + str(self.timing) + 'connection_status: ' + str(self.connection_status) + '}'
        return environment
