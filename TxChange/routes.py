from flask import render_template, flash, redirect, url_for, request
from TxChange import app, db, bcrypt
from TxChange.forms import RegistrationForm, LoginForm, NewTicket
from TxChange.models import User, Ticket
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="this is the about page")


@app.route("/discover")
def discover():
    return render_template("discover.html", title="Discover")


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
def profile():
    return render_template("profile.html", title="My Profile Page")


@app.route("/NewTicket", methods=["GET", "POST"])
@login_required
def new_ticket():
    form = NewTicket()
    if form.validate_on_submit():
        ticket = Ticket(
            artist=form.artist.data,
            venue=form.venue.data,
            price=form.price.data,
            concert_date_time=form.concert_date_time.data,
            owner=current_user,
        )
        db.session.add(ticket)
        db.session.commit()
        flash(
            f"A concert ticket for {form.artist.data} at {form.venue.data} on {form.concert_date_time.data} has been created!",
            "success",
        )
        return redirect(url_for("home"))
    return render_template("new_ticket.html", title="Post a New Ticket", form=form)
