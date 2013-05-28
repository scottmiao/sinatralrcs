from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from models import Song, db
from datetime import date


TITLE = 'Songs By Sinatra'
SECRET_KEY = 'development key'
USERNAME = 'frank'
PASSWORD = 'sinatra'
app = Flask(__name__)
app.config.from_object(__name__)


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
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        lst = (request.form['released_on']).split('/')
        released_on = date(int(lst[2]), int(lst[0]), int(lst[1]))
        song = Song(request.form['title'],
                    request.form['lyrics'],
                    request.form['length'],
                    released_on)
        db.session.add(song)
        db.session.commit()
        flash('Song succsessfully added')
        return redirect(url_for('show_songs'))
    else:
        return render_template('new_song.html', title=title)


# delete a song
@app.route('/songs/<int:song_id>/delete', methods=['POST', 'DELETE'])
def delete_song(song_id, title=TITLE):
    if not session.get('logged_in'):
        abort(401)
    song = Song.query.filter(Song.id == song_id).first()
    db.session.delete(song)
    db.session.commit()
    flash('Song succsessfully deleted')
    return redirect(url_for('show_songs'))


# edit and update a song
@app.route('/songs/<int:song_id>/edit', methods=['GET', 'POST', 'PUT'])
def edit_song(song_id, title=TITLE):
    if not session.get('logged_in'):
        abort(401)
    song = Song.query.filter(Song.id == song_id).first()
    if request.method == 'GET':
        return render_template('edit_song.html', song=song, title=title)
    song.title = request.form['title']
    song.lyrics = request.form['lyrics']
    song.length = request.form['length']
    lst = (request.form['released_on']).split('/')
    song.released_on = date(int(lst[2]), int(lst[0]), int(lst[1]))
    db.session.commit()
    flash('Song succsessfully updated')
    return redirect(url_for('show_songs'))


# admin login
@app.route('/login', methods=['GET', 'POST'])
def login(title=TITLE):
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_songs'))
    return render_template('login.html', error=error, title=title)


# admin logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
