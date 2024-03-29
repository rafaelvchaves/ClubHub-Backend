from flask_sqlalchemy import SQLAlchemy
import bcrypt
import datetime
import hashlib
import os

db = SQLAlchemy()

association_club_user = db.Table('association_club_user', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('club_id', db.Integer, db.ForeignKey('club.id'))
)

association_user_post = db.Table('association_user_post', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Club(db.Model):
    __tablename__ = 'club'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)
    application_required = db.Column(db.Boolean)
    interested_users = db.relationship('User', secondary=association_club_user, back_populates='favorite_clubs')
    category = db.Column(db.String, nullable=False)
    href = db.Column(db.String)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.level = kwargs.get('level')
        self.application_required = kwargs.get('application_required')
        self.interested_users = []
        self.category = kwargs.get('category')
        self.href = kwargs.get('href')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'application_required': self.application_required,
            'interested_users': [u.serialize_no_clubs() for u in self.interested_users],
            'category': self.category,
            'href': self.href
        }
    
    def serialize_no_users(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'level': self.level,
            'application_required': self.application_required,
            'category': self.category,
            'href': self.href
        }

    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    # User information
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_digest = db.Column(db.String, nullable=False)
    favorite_clubs = db.relationship('Club', secondary=association_club_user, back_populates='interested_users')
    created_posts = db.relationship('Post', cascade='delete')
    liked_posts = db.relationship('Post', secondary=association_user_post, back_populates='interested_users')

    # Session information
    session_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    update_token = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.favorite_clubs = []
        self.created_posts = []
        self.liked_posts = []
        self.password_digest = bcrypt.hashpw(
            kwargs.get("password").encode("utf8"), bcrypt.gensalt(rounds=13)
        )
        self.renew_session()

    # Used to randomly generate session/update tokens
    def _urlsafe_base_64(self):
        return hashlib.sha1(os.urandom(64)).hexdigest()

    # Generates new tokens, and resets expiration time
    def renew_session(self):
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode("utf8"), self.password_digest)

    # Checks if session token is valid and hasn't expired
    def verify_session_token(self, session_token):
        return (
            session_token == self.session_token
            and datetime.datetime.now() < self.session_expiration
        )

    def verify_update_token(self, update_token):
        return update_token == self.update_token

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'favorite_clubs': [c.serialize_no_users() for c in self.favorite_clubs],
            'created_posts': [p.serialize_no_users() for p in self.created_posts],
            'liked_posts': [p.serialize_no_users() for p in self.liked_posts]
        }

    def serialize_no_clubs(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    interested_users = db.relationship('User', secondary=association_user_post, back_populates='liked_posts')

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.body = kwargs.get('body')
        self.author_id = kwargs.get('author_id')
        self.interested_users = []

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'author_id': self.author_id,
            'interested_users': [u.serialize_no_clubs() for u in self.interested_users]
        }

    def serialize_no_users(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'author_id': self.author_id
        }
