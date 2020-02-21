from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    BooleanField,
    TextField,
    SubmitField,
    DecimalField,
    DateTimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from TxChange.models import User, Ticket


class RegistrationForm(FlaskForm):
    email = StringField("email address", validators=[Email(), DataRequired()])
    password = StringField("password por favor", validators=[DataRequired()])
    rememberme = BooleanField()
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField("email address", validators=[Email(), DataRequired()])
    password = StringField("password por favor", validators=[DataRequired()])
    rememberme = BooleanField()
    submit = SubmitField()


class NewTicket(FlaskForm):
    artist = StringField("Who's playing?", validators=[DataRequired()])
    venue = StringField("Where's it at?")
    price = DecimalField("How much?", validators=[DataRequired()])
    concert_date_time = DateTimeField("When?", validators=[DataRequired()])
    submit = SubmitField()
