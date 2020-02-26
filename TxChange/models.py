from TxChange import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


interested = db.Table(
    "interested",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("ticket_id", db.Integer, db.ForeignKey("ticket.id")),
)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    profile_pic = db.Column(db.String(), nullable=False, default="default.jpg")
    tickets_id = db.Column(db.Integer, db.ForeignKey("ticket.id"))
    my_winning_bid_id = db.Column(db.Integer, db.ForeignKey("ticket.id"))
    tickets = db.relationship(
        "Ticket", foreign_keys=[tickets_id], backref="owner", lazy=True
    )
    my_winning_bids = db.relationship(
        "Ticket",
        foreign_keys=[my_winning_bid_id],
        backref="current_best_bidder",
        lazy=True,
    )
    interested_in = db.relationship(
        "Ticket", secondary=interested, backref="users_interested", lazy="dynamic"
    )

    def __repr__(self):
        return f"{self.email}"


class Ticket(db.Model):
    __tablename__ = "ticket"
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(80), nullable=False)
    venue = db.Column(db.String(80))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    price = db.Column(db.Integer, nullable=False)
    concert_date_time = db.Column(db.DateTime)
    interest_by = db.relationship(
        "User", secondary=interested, backref="tickets_interested_in", lazy="dynamic"
    )

    def __repr__(self):
        return f"Ticket({self.artist} at {self.venue})"

