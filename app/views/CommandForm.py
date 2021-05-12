from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommandForm(FlaskForm):
    """
    Inherits FlaskForm providing additional arguments for validation
    """
    command = StringField('Command', validators=[DataRequired()])
    expectation = StringField('Expectation', validators=[DataRequired()])
    submit = SubmitField('Add Command')
