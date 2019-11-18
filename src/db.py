from flask_sqlalchemy import SQLAlchemy

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
    # tags

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        self.level = kwargs.get('level')
        self.application_required = kwargs.get('application_required')
        self.interested_users = []

    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    favorite_clubs = db.relationship('Club', secondary=association_club_user, back_populates='interested_users')
    created_posts = db.relationship('Post', cascade='delete')
    liked_posts = db.relationship('Post', secondary=association_user_post, back_populates='interested_users')

    def __init__(self, **kwargs):
        self.netid = kwargs.get('netid')
        self.password = kwargs.get('password')
        self.favorite_clubs = []
        self.created_posts = []
    
class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    liked_posts = db.relationship('User', secondary=association_user_post, back_populates='liked_posts')
    #type

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.body = kwargs.get('body')

# class Tag(db.Model)
