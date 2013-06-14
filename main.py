from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from flask.ext.wtf import (Form, TextField, TextAreaField,
                           PasswordField, SubmitField,
                           Required, ValidationError,
                           IntegerField, DateTimeField)
from models import Song, db
from datetime import date
from flask_mail import Mail
from flask_mail import Message

from helpers import is_current, set_title


SECRET_KEY = 'development key'
USERNAME = 'frank'
PASSWORD = 'sinatra'
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 994
MAIL_USE_SSL = True
MAIL_USERNAME = 'jazzymiao'
MAIL_PASSWORD = '********'
app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)


class SongForm(Form):

    title = TextField("Title", validators=[Required()])
    lyrics = TextAreaField("Lyrics")
    length = IntegerField("Lenth")
    released_on = DateTimeField("Released on", format='%m/%d/%Y')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about(title='All About This Website'):
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    send_message()
    flash('Thank you for your message. We\'ll be in touch soon.')
    return redirect(url_for('show_songs'))


# email helper for '/contact'
def send_message():
    msg = Message('A message frome ' + request.form['name'] + ': '
                  + request.form['email'],
                  sender="jazzymiao@163.com",
                  recipients=["jazzymiao@163.com"])
    msg.body = request.form['message']
    mail.send(msg)


# listing songs
@app.route('/songs')
def show_songs():
    songs = Song.query.all()
    return render_template('songs.html', songs=songs)


# showing a song
@app.route('/songs/<int:song_id>')
def show_a_song(song_id):
    song = Song.query.get_or_404(song_id)
    return render_template('show_song.html', song=song)


# add a new song
@app.route('/songs/new', methods=['GET', 'POST'])
def new_song():
    if not session.get('logged_in'):
        abort(401)

    form = SongForm()

    if request.method == 'POST':
        if form.validate():
            song = Song()
            form.populate_obj(song)
            db.session.add(song)
            db.session.commit()
            flash('Song succsessfully added')
            return redirect(url_for('show_songs'))
        else:
            flash("Your form contained errors")
            return render_template('new_song.html', form=form)
    else:
        return render_template('new_song.html', form=form)


# delete a song
@app.route('/songs/<int:song_id>/delete', methods=['POST', 'DELETE'])
def delete_song(song_id):
    if not session.get('logged_in'):
        abort(401)

    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    flash('Song succsessfully deleted')
    return redirect(url_for('show_songs'))


# edit and update a song
@app.route('/songs/<int:song_id>/edit', methods=['GET', 'POST', 'PUT'])
def edit_song(song_id):
    if not session.get('logged_in'):
        abort(401)

    song = Song.query.get_or_404(song_id)
    form = SongForm(obj=song)

    if request.method == 'GET':
        return render_template('edit_song.html', form=form, song=song)
    # request.method == 'POST' or 'PUT'
    if form.validate():
        form.populate_obj(song)
        db.session.commit()
        flash('Song succsessfully updated')
        return render_template('show_song.html', song=song)
    else:
        flash("Your form contained errors")
        return redirect("/songs/" + str(song.id) + "/edit")


# admin login
@app.route('/login', methods=['GET', 'POST'])
def login():
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
    return render_template('login.html', error=error)


# admin logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


# @app.route('/songs/<int:song_id>/like', methods=['POST'])
# def like(song_id):
#     song = Song.query.filter(Song.id == song_id).first()
#     song.likes = song.likes + 1
#     db.session.commit()
#     return redirect("/songs/" + str(song.id))


# Ajax edition
@app.route('/songs/<int:song_id>/like', methods=['POST'])
def like(song_id):
    song = Song.query.get_or_404(song_id)
    song.likes = song.likes + 1
    db.session.commit()
    if not request.is_xhr:
        return redirect("/songs/" + str(song.id))
    return render_template('like.html', song=song)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


app.jinja_env.globals.update(is_current=is_current)
app.jinja_env.globals.update(set_title=set_title)

if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
