from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length


class EditEnvironmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    timing = DateTimeField('Timing', validators=[DataRequired()])
    servers = StringField('Servers')
    submit = SubmitField('Submit')