"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

# Login routes
@app.route("/show_login_form")
def show_login_form():
    """Shows login form"""
    return render_template("show_login_form.html")

@app.route("/verify_login")
def verify_login():
    """verifies if user is in the db already, if not, add user to db and add to session"""

    email = request.args.get("email")
    password = request.args.get("password")
    
    # check if user is in db; if not, add to db
    try:
        user = User.query.filter(User.email == email).one()
    except: 
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
    # add user to session upon login
    session["user"]=user.user_id
    
    flash("You successfully logged in!")
    return render_template("user_info.html", user=user)

@app.route("/logout")
def logout():
    """log out of the movie rating system"""
    try:
        del session["user"]
        flash("You successfully logged out!")
  
    except:
        flash("You aren't logged in!")
    
    return render_template("homepage.html")


# User routes
@app.route("/users")
def user_list():
    """Show list of users"""

    users= User.query.all()
    return render_template("user_list.html", users=users)

@app.route("/users/<int:user_id>")
def show_user_info(user_id):
    """Display user info and list of ratings for rated movies."""
    
    user = User.query.get(user_id)
    return render_template("user_info.html", user=user)


#Movie routes
@app.route("/movies")
def movie():
    """Show list of movies"""
    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>")
def show_movie_info(movie_id):
    """Display movie info and id for all movies."""
    
    movie = Movie.query.get(movie_id)
    ratings = Rating.query.filter(Rating.movie_id == movie_id).all()
    return render_template("movie_info.html", movie=movie, ratings=ratings)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True)