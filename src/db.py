from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    #tags
    level = db.Column(db.String, nullable=False)
    application_required = db.Column(db.Boolean)
    #interested_users
    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    #favorite_clubs
    #created_posts
    #liked_posts
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    #author
    #type
    body = db.Column(db.String, nullable=False)
    #interested_users
    
#class Tag(db.Model)
