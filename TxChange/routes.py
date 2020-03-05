import secrets
import os
from flask import render_template, flash, redirect, url_for, request
from TxChange import app, db, bcrypt
from TxChange.forms import RegistrationForm, LoginForm, NewTicket, Ticketbid, Test
from TxChange.models import User, Ticket
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    print(type)
    return render_template("about.html", title="this is the about page")


@app.route("/discover")
def discover():
    tickets = Ticket.query.all()
    return render_template("discover.html", title="Discover", tickets=tickets)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.rememberme.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.email.data}!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


# need to update to spontaneously create url for each unique user
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    t_sell = Ticket.query.filter_by(owner=current_user).all()
    t_interest = User.query.filter_by(id=current_user.id).first().interested_in
    return render_template(
        "profile.html",
        title="Profile Page",
        tickets=t_sell,
        interestingtickets=t_interest,
    )

def save_ticket_picture(form_ticket_pic):
	#don't want user's picture name to collide with other ticket file names
	#random hex for base of file name
	random_name = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_ticket_pic.filename)
	ticket_name = random_name+f_ext
	ticket_path = os.path.join(app.root_path, 'static/ticket_pics', ticket_name)
	form_ticket_pic.save(ticket_path)

	return ticket_name

@app.route("/NewTicket", methods=["GET", "POST"])
@login_required
def new_ticket():
	form = NewTicket()
	if form.validate_on_submit():
		if form.ticket_file.data:
			ticket_file = save_ticket_picture(form.ticket_file.data)
			ticket = Ticket(artist=form.artist.data,venue=form.venue.data,price=form.price.data,concert_date_time=form.concert_date_time.data, owner=current_user,ticket_pic =ticket_file)
			db.session.add(ticket)
			db.session.commit()
			flash(f"A concert ticket for {form.artist.data} at {form.venue.data} on{form.concert_date_time.data} has been created!","success",)
			return redirect(url_for("home"))
	return render_template("create_ticket.html", title="Post a New Ticket", form=form)


@app.route("/ticket/<ticket_id>/bid", methods=["GET", "POST"])
@login_required
def ticket(ticket_id):
    form = Test()
    ticket = Ticket.query.get_or_404(ticket_id)
    if form.validate_on_submit():
        if form.amount.data <= ticket.current_best_bid:
            flash("Not high enough!", "danger")
            return redirect(url_for("discover"))
        ticket.current_best_bid = form.amount.data
        ticket.current_best_bidder = current_user
        db.session.add(ticket)
        db.session.commit()
        flash("Bid Entered", "success")
        return redirect(url_for("home"))
    return render_template("ticket.html", title="Bid", form=form, ticket=ticket)


@app.route("/interestedin/<ticket_id>/", methods=["GET", "POST"])
@login_required
def interested(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    ticket.users_interested.append(current_user)
    db.session.add(ticket)
    db.session.commit()
    flash(f"You saved ticket for {ticket.artist} at {ticket.venue}.", "success")
    return redirect(url_for("profile"))


@app.route("/test", methods=["GET", "POST"])
def test():
    form = Test()
    if form.validate_on_submit():
        flash("test worked")
        return redirect(url_for("home"))
    return render_template("test.html", title="test", form=form)

