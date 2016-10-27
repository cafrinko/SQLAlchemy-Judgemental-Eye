"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)

@app.route('/register', methods=["GET"])
def register_form():
    """Display form."""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():
    """Submits form and reroutes to homepage."""

    email = request.form.get('useremail')
    password = request.form.get('userpassword')

    user = User.query.filter_by(email=email).first()
    if not user:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You've been added")
    else:
        flash("You already have an account. Try logging in with your email.")

    return redirect("/")

@app.route('/login', methods=["GET"])
def login_form():
    """Display form."""

    return render_template("login_form.html")

@app.route('/login', methods=["POST"])
def login_process():
    """Logs in existing user."""

    email = request.form.get('useremail')
    password = request.form.get('userpassword')

    user = User.query.filter_by(email=email, password=password).first()

    if user:
        session[email] = password
        flash("You are now logged in.")
    else:
        flash("Your username does not match your password. Please try again with a different username password combination.")

    return redirect('/')

@app.route('/logout', methods=["GET"])
def logout_form():
    """Displays logout button"""

    return render_template('logout_form.html')

@app.route('/logout', methods=["POST"])
def logout_process():
    """Logs user out"""
    
    logout = request.form.get('logout')
    session.clear()
    flash('You are now logged out')

    return redirect('/')



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

        # Use the DebugToolbar
    DebugToolbarExtension(app)


        
    app.run()
