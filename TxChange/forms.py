from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    SubmitField,
    DateTimeField,
    IntegerField,
)
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    email = StringField("email address", validators=[Email(), DataRequired()])
    password = StringField("password por favor", validators=[DataRequired()])
    confirm_password = StringField("confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[Email(), DataRequired()])
    password = StringField("password por favor", validators=[DataRequired()])
    rememberme = BooleanField("Remember me")
    submit = SubmitField("Login")


class NewTicket(FlaskForm):
    artist = StringField("Who's playing?", validators=[DataRequired()])
    venue = StringField("Where's it at?")
    price = IntegerField("How much?", validators=[DataRequired()])
    concert_date_time = DateTimeField("When?", format="%m/%d/%Y")
    submit = SubmitField()
'''
class BidOnTicket(FlaskForm):
		amount = IntegerField("I'll pay this amount")
		market_price = BooleanField("I'll pay the asking price")
		submit=SubmitField()
'''