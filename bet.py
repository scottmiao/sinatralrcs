from flask import Flask
import random

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/bet/<int:stake>/on/<int:number>')
def betting_game(stake, number):
    roll = random.randrange(6) + 1
    if number == roll:
        return "It landed on %d. Well done, you win %d chips." \
            % (roll, 6 * stake)
    else:
        return "It landed on %d. You lose your stake of %d chips." \
            % (roll, stake)


if __name__ == '__main__':
    app.run(debug="True")
