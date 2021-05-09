from app import db


class Command(db.Model):
    """
    Model inherits db.Model from SQL Alchemy
    """
    id = db.Column(db.Integer, primary_key=True)
    command = db.Column(db.String(200), index=True)
    expectation = db.Column(db.String(200), index=True)
    actual_output = db.Column(db.String(200), index=True, default=None)
    command_status = db.Column(db.Integer, index=True, default=1)
    status_timestamp = (db.Column(db.DateTime, index=True, default=None))
    approval_status = (db.Column(db.Integer, index=True))
    approval_timestamp = (db.Column(db.DateTime, index=True))
    server_id_fk = db.Column(db.Integer, db.ForeignKey('server.id'))

    def __repr__(self):
        """
        Defines how objects of this Class are printed
        :return: command as dictionary
        """
        command = '{id: ' + str(self.id) + ',' + 'command: ' + self.command + ',' + 'expectation: ' + self.expectation + ',' \
                  + 'actual_output: ' + str(self.actual_output) + ',' + 'command_status: ' \
                 + str(self.command_status) + ',' + 'status_timestamp: ' + str(self.status_timestamp) + ',' + \
                 'approval_status: ' + str(self.approval_status) + ',' + 'approval_timestamp: ' + str(self.approval_timestamp) + '}'
        return command
