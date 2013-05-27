from models import Song, db
from datetime import date


songs = [Song('My Way', 'And now the end is near ... ',
              435, date(1969, 1, 1)),
         Song('Come Fly With Me',
              "Come fly with me, let's fly, let's fly away ... .",
              199, date(1958, 1, 6))]


for song in songs:
    db.session.add(song)

db.session.commit()
