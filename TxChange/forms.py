from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo

class Ticketbid(FlaskForm):
	amount = IntegerField("I'll pay this amount", validators=[DataRequired(), IntegerField()])
	submit = SubmitField('Make the bid')

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
	ticket_file = FileField('Ticket File', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
	submit = SubmitField("Create Ticket")


class Test(FlaskForm):
	amount = IntegerField('Bid Amount', validators=[DataRequired()])
	submit = SubmitField("Enter Bid")