from app import db
from sqlalchemy.dialects.postgresql import JSON


class TrackFeatures(db.Model):
    __tablename__ = 'track_features'

    id = db.Column(db.Integer(), primary_key=True)
    track_id = db.Column(db.String())
    track_name = db.Column(db.String())
    artist_name = db.Column(db.String())
    danceability = db.Column(db.Float())
    energy = db.Column(db.Float())
    key = db.Column(db.Integer())
    loudness = db.Column(db.Float())
    mode = db.Column(db.Integer())
    speechiness = db.Column(db.Float())
    acousticness = db.Column(db.Float())
    instrumentalness = db.Column(db.Float())
    liveness = db.Column(db.Float())
    valence = db.Column(db.Float())
    tempo = db.Column(db.Float())
    duration_ms = db.Column(db.Integer())
    time_signature = db.Column(db.Integer())

    def __init__(self, track_id, track_name, artist_name, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature):
        self.track_id = track_id
        self.track_name = track_name
        self.artist_name = artist_name
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo
        self.duration_ms = duration_ms
        self.time_signature = time_signature
        

    def __repr__(self):
        return '<id {}>'.format(self.id)