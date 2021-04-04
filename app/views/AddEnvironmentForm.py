from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length


class AddEnvironmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    timing = DateTimeField('Timing', validators=[DataRequired()])
    submit = SubmitField('Submit')