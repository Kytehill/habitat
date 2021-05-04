from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EnvironmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    timing = IntegerField('Timing', validators=[DataRequired(message='Please proved a number between 0 and 120'),
                                                NumberRange(0, 120, message='Please proved a number between 0 and 120')])
    submit = SubmitField('Add Environment')
