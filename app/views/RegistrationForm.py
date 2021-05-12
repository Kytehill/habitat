from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,  ValidationError, Email, EqualTo
from app.models import User


class RegistrationForm(FlaskForm):
    """
    Inherits FlaskForm providing additional arguments for validation

    The code associated with the Login has been derived from a Flask tutorial
    provided by Miguel Grinberg

    Grinberg, M., 2017. The Flask Mega Tutorial [Online Programming Tutorial]. Available
        from: https://miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms
        [Accessed 22 Match 2021]
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')