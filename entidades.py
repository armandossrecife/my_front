from flask_login import UserMixin
from banco import db, user_files

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False) 
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    my_files = db.relationship('File', secondary=user_files, backref='myfiles')

# Classe que representa os dados de um arquivo
class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    original_filename = db.Column(db.String(100))
    filename = db.Column(db.String(100))