from flask import render_template, flash, redirect, url_for, request
from TxChange import app, db, bcrypt
from TxChange.forms import RegistrationForm, LoginForm, NewTicket
from TxChange.models import User, Ticket
from flask_login import current_user, login_user, logout_user, login_required


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="this is the about page")


@app.route("/discover")
def discover():
    return render_template("discover.html", title="Discover")


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register")
def register():
    return render_template("register.html", title="Register")


# need to update to spontaneously create url for each unique user
@app.route("/profile")
def profile():
    return render_template("profile.html", title="My Profile Page")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
