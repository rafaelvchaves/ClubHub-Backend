import json
from db import db, Club, User, Post
from flask import Flask, request
from sqlalchemy import or_, and_

db_filename = "ClubHub.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()
    
@app.route('/api/clubs/')
def get_all_clubs():
    if not request.data:
        clubs = Club.query.all()
    else:
        request_body = json.loads(request.data)
        category = request_body.get('category')
        search_query = request_body.get('search_query')
        level = request_body.get('level')
        application_required = request_body.get('application_required')
        matches_category = Club.category == category if category else True
        matches_text = or_(Club.name.contains(search_query), Club.description.contains(search_query)) if search_query else True
        matches_level = Club.level == level if level else True
        matches_app_required = or_(Club.application_required == application_required, Club.application_required.is_(None)) if application_required is not None else True
        clubs = Club.query.filter(and_(matches_category, matches_text, matches_level, matches_app_required))
    res = {'success': True, 'data': [c.serialize() for c in clubs]}
    return json.dumps(res), 200

@app.route('/api/clubs/', methods=['POST'])
def create_club():
    post_body = json.loads(request.data)
    name = post_body.get('name')
    description = post_body.get('description', '')
    level = post_body.get('level')
    application_required = post_body.get('application_required', None)
    club = Club(
        name=name,
        description=description,
        level=level,
        application_required=application_required
    )
    db.session.add(club)
    db.session.commit()
    return json.dumps({'success': True, 'data': club.serialize()}), 201

@app.route('/api/club/<int:club_id>/')
def get_club(club_id):
    course = Club.query.filter_by(id=club_id).first()
    if not course:
        return json.dumps({'success': False, 'error': 'Club not found'}), 404
    return json.dumps({'success': True, 'data': course.serialize()}), 200

@app.route('/api/club/<int:club_id>/', methods=['DELETE'])
def delete_club(club_id):
    club = Club.query.filter_by(id=club_id).first()
    if not club:
        return json.dumps({'success': False, 'error': 'Club not found!'}), 404
    db.session.delete(club)
    db.session.commit()
    return json.dumps({'success': True, 'data': club.serialize()}), 200

@app.route('/api/users/')
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    name = post_body.get('name')
    netid = post_body.get('netid')
    password = post_body.get('password')
    user = User(
        name=name,
        netid=netid,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

@app.route('/api/user/<int:user_id>/', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    db.session.delete(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/user/<int:user_id>/')
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found'}), 404
    return json.dumps({'success': True, 'data': user.serialize()}), 200

@app.route('/api/posts/')
def get_all_posts():
    if not request.data:
        posts = Post.query.all()
    else:
        request_body = json.loads(request.data)
        search_query = request_body.get('search_query')
        author = request_body.get('author_id')
        matches_text = or_(Post.title.contains(search_query), Post.body.contains(search_query)) if search_query else True
        matches_author = Post.author_id == author if author else True
        posts = Post.query.filter(and_(matches_author, matches_text))
    res = {'success': True, 'data': [p.serialize() for p in posts]}
    return json.dumps(res), 200

@app.route('/api/posts/', methods=['POST'])
def create_post():
    post_body = json.loads(request.data)
    title = post_body.get('title')
    body = post_body.get('body')
    author_id = post_body.get('author_id')
    post = Post(
        title=title,
        body=body,
        author_id=author_id
    )
    db.session.add(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 201

@app.route('/api/post/<int:post_id>/')
def get_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return json.dumps({'success': False, 'error': 'Post not found'}), 404
    return json.dumps({'success': True, 'data': post.serialize()}), 200

@app.route('/api/post/<int:post_id>/', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        return json.dumps({'success': False, 'error': 'Post not found!'}), 404
    db.session.delete(post)
    db.session.commit()
    return json.dumps({'success': True, 'data': post.serialize()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
