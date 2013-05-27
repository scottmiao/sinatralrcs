from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from models import Song, db
from datetime import date


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


# add a new song
@app.route('/songs/new', methods=['GET', 'POST'])
def new_song(title=TITLE):
    if request.method == 'POST':
        lst = (request.form['released_on']).split('/')
        released_on = date(int(lst[2]), int(lst[1]), int(lst[0]))
        song = Song(request.form['title'],
                    request.form['lyrics'],
                    request.form['length'],
                    released_on)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('show_songs'))
    else:
        return render_template('new_song.html', title=title)


# delete a song
@app.route('/songs/<int:song_id>/delete', methods=['POST', 'DELETE'])
def delete_song(song_id, title=TITLE):
    song = Song.query.filter(Song.id == song_id).first()
    db.session.delete(song)
    db.session.commit()
    return redirect(url_for('show_songs'))


# edit and update a song
@app.route('/songs/<int:song_id>/edit')
def edit_song(song_id, title=TITLE):
    song = Song.query.filter(Song.id == song_id).first()
    return render_template('edit_song.html', song=song, title=title)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
