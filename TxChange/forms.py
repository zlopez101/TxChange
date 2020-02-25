from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from TxChange.models import Ticket, User


class RegistrationForm(FlaskForm):
    email = StringField("email address", validators=[Email(), DataRequired()])
    password = StringField("password por favor", validators=[DataRequired()])
    confirm_password = StringField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )
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


class BidOnTicket(FlaskForm):
    def __init__(self, ticket_id):
        self.ticket_id = ticket_id
        super().__init__()

    amount = IntegerField(
        "I'll pay this amount", validators=[IntegerField(), DataRequired()]
    )
    submit = SubmitField("Make your bid!")

    def is_higher(self, amount):
        ticket = Ticket.query.filter_by(id=self.ticket_id).first()
        if ticket.current_best_bid > amount:
            raise ValidationError(
                f"Your bid must be larger than current bid of {ticket.current_best_bid}."
            )

