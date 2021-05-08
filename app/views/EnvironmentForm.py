from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class EnvironmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    timing = IntegerField('Timing', validators=[DataRequired(message='Please proved a time interval between 0 and 120 '
                                                                     'seconds'), NumberRange(0, 120, message='Please provide a time interval between 0 and 120 seconds')])
    submit = SubmitField('Add Environment')
