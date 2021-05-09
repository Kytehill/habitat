from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, IPAddress


class ServerForm(FlaskForm):
    """
    Inherits FlaskForm providing additional arguments for validation
    """
    ip_address = StringField('Server IP Address', validators=[DataRequired(),
                             IPAddress(ipv4=True, ipv6=True, message='Please provide a valid IP Address')])
    username = StringField('Server Username', validators=[DataRequired()])
    submit = SubmitField('Add Server')
