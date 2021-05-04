from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ServerForm(FlaskForm):
    ip_address = StringField('Server IP Address', validators=[DataRequired()])
    username = StringField('Server Username', validators=[DataRequired()])
    submit = SubmitField('Add Server')
