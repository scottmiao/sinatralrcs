from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from models import Song


app = Flask(__name__)
TITLE = 'Songs By Sinatra'


@app.route('/')
def home(title=TITLE):
    return render_template('home.html', title=title)


@app.route('/about')
def about(title='All About This Website'):
    return render_template('about.html', title=title)


@app.route('/contact')
def contact(title=TITLE):
    return render_template('contact.html', title=title)


# listing songs
@app.route('/songs')
def show_songs(title=TITLE):
    songs = Song.query.all()
    return render_template('songs.html', songs=songs, title=title)

# showing a song
@app.route('/songs/<int:song_id>')
def show_a_song(song_id, title=TITLE):
    song = Song.query.filter(Song.id == song_id).first()
    return render_template('show_song.html', song=song, title=title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
