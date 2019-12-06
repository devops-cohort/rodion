from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

#class Posts(db.Model):
#    id = db.Column(db.Integer, primary_key =True)
#    title = db.Column(db.String(100), nullable=False, unique=True)
#    content = db.Column(db.String(500), nullable=False, unique=True)
#    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
#
#    def __repr__(self):
#        return ''.join(['User: ', self.user_id, '\r\n', 'Title: ', self.title, '\r\n',self.content])

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    songs = db.relationship('Songs', backref='user', lazy=True)
    
    def __repr__(self):
        return ''.join([
            'User ID: ', str(self.id), '\r\n', 
            'Email: ', self.email, '\r\n', 
            'Name: ',self.first_name, '\r\n', ' ', self.last_name
        ])

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    artist = db.Column(db.String(500), nullable=False)
    album = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return ''.join([
            'Song ID: ', str(self.id), '\r\n',
            'Title: ', self.title, '\r\n',
            'Artist: ', self.artist, '\r\n', 
            'Album: ', self.album, '\r\n',
            'Genre: ', self.genre, '\r\n'
        ])

def load_song(id):
    return Songs.query.get(int(id))
        
@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))
