from TxChange import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    profile_pic = db.Column(db.String(), nullable=False, default="default.jpg")
    tickets = db.relationship("Ticket", backref="gg", lazy=True)

    def __repr__(self):
        return f"{self.email}"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80), nullable=False)
    venue = db.Column(db.String(80))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False)
    concert_date_time = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Ticket({self.artist} at {self.venue} on {self.concert_date_time})"

