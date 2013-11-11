from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html'), 404


if __name__ == '__main__':
    app.run(debug='True')
