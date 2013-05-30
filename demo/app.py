from flask import Flask
from flask_mail import Mail
from flask_mail import Message

MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 994
MAIL_USE_SSL = True
MAIL_USERNAME = 'jazzymiao'
MAIL_PASSWORD = 'secret'
app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)


@app.route("/")
def index():
    msg = Message("Hello",
                  sender="jazzymiao@163.com",
                  recipients=["jazzymiao@gmail.com"])
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug='True', host='0.0.0.0')
