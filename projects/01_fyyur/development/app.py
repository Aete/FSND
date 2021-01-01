#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from datetime import datetime
from copy import deepcopy

from config import SQLALCHEMY_DATABASE_URI
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    city = db.Column(db.String(30), nullable = False)
    state = db.Column(db.String(30), nullable = False)
    address = db.Column(db.String(120), nullable = False)
    genres = db.Column(db.ARRAY(db.String(20)), nullable = False)
    phone = db.Column(db.String(30))
    website = db.Column(db.String(100))
    image_link = db.Column(db.String(100))
    facebook_link = db.Column(db.String(50))
    seeking_talent = db.Column(db.Boolean, nullable = False, default = True)
    seeking_description = db.Column(db.String(500), default = 'We are looking for an artist who want to play in here')
    show = db.relationship('Show', backref='venue', cascade="all, delete-orphan" ,  lazy=True)
    
    @property
    def get_show(self):
      past_show = Show.query.filter((Show.start_time<datetime.now())&(Show.venue_id==self.id)).all()
      upcoming_show = Show.query.filter((Show.start_time>datetime.now())&(Show.venue_id==self.id)).all()
      return {
            "past_shows": past_show,
            "upcoming_shows": upcoming_show
      }
    
    @property
    def get_attribute(self):
      show_info = self.get_show
      past_shows = show_info['past_shows']
      upcoming_shows = show_info['upcoming_shows']
      past_shows_count = len(past_shows)
      upcoming_shows_count = len(upcoming_shows)
      return {
        'id' : self.id,
        'name' : self.name,
        'city' : self.city,
        'state' : self.state,
        'address' : self.address,
        'genres' : self.genres,
        'phone' : self.phone,
        'website': self.website,
        'image_link': self.image_link,
        'facebook_link' : self.facebook_link,
        'seeking_talent': self.seeking_talent,
        'seeking_description': self.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
      }


class Artist(db.Model):
    __tablename__ = 'Artist'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(30))
    genres = db.Column(db.ARRAY(db.String(20)), nullable = False)
    website = db.Column(db.String(100)) 
    image_link = db.Column(db.String(100))
    facebook_link = db.Column(db.String(100))
    seeking_venue = db.Column(db.Boolean, nullable=False, default = True)
    seeking_description = db.Column(db.String(500), default = 'I am looking for a place where I can play')
    show = db.relationship('Show', backref='artist', cascade="all, delete-orphan", lazy=True)

    @property
    def get_show(self):
      past_show = Show.query.filter((Show.start_time<datetime.now())&(Show.artist_id==self.id)).all()
      past_show_venue = []
      for show in past_show:
        venue = Venue.query.get(show.venue_id).get_attribute
        show_venue_info = {"venue_id": venue.id,
                            "venue_name": venue.name,
                            "venue_image_link": venue.image_link,
                            "start_time": show.start_time}
        past_show_venue.append(show_venue_info)
      upcoming_show_venue = []
      upcoming_show = Show.query.filter((Show.start_time>datetime.now())&(Show.artist_id==self.id)).all()
      for show in upcoming_show:
        venue = Venue.query.get(show.venue_id).get_attribute
        show_venue_info = {"venue_id": venue['id'],
                            "venue_name": venue['name'],
                            "venue_image_link": venue['image_link'],
                            "start_time": show.start_time}
        upcoming_show_venue.append(show_venue_info)
      print(past_show, upcoming_show)
      return {
            "past_shows": past_show_venue,
            "upcoming_shows": upcoming_show_venue
      }
    
    @property
    def get_attribute(self):
      show_info = self.get_show
      past_shows = show_info['past_shows']
      upcoming_shows = show_info['upcoming_shows']
      past_shows_count = len(past_shows)
      upcoming_shows_count = len(upcoming_shows)
      return {
        'id' : self.id,
        'name' : self.name,
        'city' : self.city,
        'state' : self.state,
        'genres' : self.genres,
        'phone' : self.phone,
        'website': self.website,
        'image_link': self.image_link,
        'facebook_link' : self.facebook_link,
        'seeking_venue': self.seeking_venue,
        'seeking_description': self.seeking_description,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
      }

class Show(db.Model):
  __tablename__= 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.TIMESTAMP(timezone=False))
  title = db.Column(db.String(30), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, dd, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  cities = set([(venue.get_attribute['city'], venue.get_attribute['state']) for venue in Venue.query.all()])
  data = []
  for city,state in cities:
    venues = Venue.query.filter((Venue.city==city)&(Venue.state==state)).all()
    venues_info = [{"id":venue.id, "name":venue.name, "num_upcoming_shows": venue.get_attribute['upcoming_shows_count']} for venue in Venue.query.all()]
    city_info = {
    "city": city,
    "state": state,
    "venues": venues_info
    }
    data.append(city_info)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id).get_attribute
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    error = False
    body = {}
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        address = request.form['address']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website = request.form['web_link']
        seeking_talent = True if 'seeking_talent' in request.form else False  
        seeking_description = request.form['seeking_description']
        venue = Venue(name=name, 
                      city=city,
                      state=state,
                      address=address,
                      phone=phone,
                      genres=genres,
                      image_link=image_link,
                      facebook_link = facebook_link,
                      website = website,
                      seeking_talent = seeking_talent,
                      seeking_description = seeking_description)
        db.session.add(venue)
        db.session.commit()
        body['name'] = venue.name
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if ~error:
      flash('Venue ' + body['name'] + ' was successfully listed!')
    else:
      flash('An error is occured to save the Venue')
    return redirect(url_for('index')) 


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = [ {"id": artist.id, "name":artist.name} for artist in Artist.query.all()]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  return render_template('pages/show_artist.html', artist=Artist.query.get(artist_id).get_attribute)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    error = False
    body = {}
    try:
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        genres = request.form.getlist('genres')
        image_link = request.form['image_link']
        facebook_link = request.form['facebook_link']
        website = request.form['web_link']
        seeking_venue = True if 'seeking_venue' in request.form else False  
        seeking_description = request.form['seeking_description']
        artist = Artist(name=name, 
                      city=city,
                      state=state,
                      phone=phone,
                      genres=genres,
                      image_link=image_link,
                      facebook_link = facebook_link,
                      website = website,
                      seeking_venue = seeking_venue,
                      seeking_description = seeking_description)
        db.session.add(artist)
        db.session.commit()
        body['name'] = artist.name
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if ~error:
      flash('Artist' + body['name'] + ' was successfully listed!')
    else:
      flash('An error is occured to save the Artist')
    return redirect(url_for('index')) 


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    body = {}
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        title = request.form['title']
        start_time = request.form['start_time']
        show = Show(artist_id=artist_id,
                    venue_id = venue_id,
                    title = title,
                    start_time = start_time)
        db.session.add(show)
        db.session.commit()
        body['title'] = show.title
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
    if ~error:
      flash('Show' + body['title'] + ' was successfully listed!')
    else:
      flash('An error is occured to save the Artist')
    return redirect(url_for('index')) 

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
