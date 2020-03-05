from TxChange import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#define interested association table for many-to-many relationship
interested = db.Table("interested", db.Column("user_id", db.ForeignKey("user.id"), primary_key=True), db.Column('ticket_id', db.ForeignKey("ticket.id"), primary_key=True))

class User(db.Model, UserMixin):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(), nullable=False, unique=True)
	password = db.Column(db.String(40), nullable=False)
	profile_pic = db.Column(db.String(), nullable=False, default="default.jpg")
	interested_in = db.relationship('Ticket', secondary=interested, back_populates='users_interested')
	def __repr__(self):
			return f"{self.email}"

class Ticket(db.Model):
	__tablename__ = "ticket"
	id = db.Column(db.Integer, primary_key=True)
	artist = db.Column(db.String(80), nullable=False)
	venue = db.Column(db.String(80))
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	price = db.Column(db.Integer, nullable=False)
	ticket_pic = db.Column(db.String(), nullable=False, default="ticket_default.JPG")
	concert_date_time = db.Column(db.DateTime)
	current_best_bid = db.Column(db.Integer, default=0)
	_owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	_current_best_bidder_id = db.Column(db.Integer, db.ForeignKey("user.id"))
	owner = db.relationship("User", foreign_keys=[_owner_id], backref="tickets", lazy=True)
	current_best_bidder = db.relationship("User",foreign_keys=[_current_best_bidder_id],backref="my_winning_bids", lazy=True)
	users_interested = db.relationship("User", secondary=interested, back_populates='interested_in')

	def __repr__(self):
		return f"Ticket({self.artist} at {self.venue})"
