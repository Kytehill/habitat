from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class EnvironmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    timing = IntegerField('Timing', validators=[DataRequired()])
    submit = SubmitField('Submit')