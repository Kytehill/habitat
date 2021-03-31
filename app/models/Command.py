from app import db
from datetime import datetime


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
