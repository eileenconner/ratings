"""Utility file to seed ratings database from MovieLens data in seed_data/"""
from datetime import datetime

from model import User
from model import Rating
from model import Movie

from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movie"

    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip().split('|')
        movie_id = row[0]
        title = row[1]
        # make sure data doesn't suck
        try:
            released_at = datetime.strptime(row[2], "%d-%b-%Y")
        except: 
            released_at = datetime.strptime('01-Jan-1900', "%d-%b-%Y")
        imdb_url = row[3]

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()

def load_ratings():
    """Load ratings from u.data into database."""

    print "Rating"

    Rating.query.delete()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        user_id, movie_id, score, rating_id = row.split('|')

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)
        
        db.session.add(rating)

    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
