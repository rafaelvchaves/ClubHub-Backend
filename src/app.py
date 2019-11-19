import json
from db import db, Club, User, Post
from flask import Flask, request

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
    clubs = Club.query.all()
    res = {'success': True, 'data': [c.serialize() for c in clubs]}
    return json.dumps(res), 200

@app.route('/api/clubs/', methods=['POST'])
def create_club():
    post_body = json.loads(request.data)
    name = post_body.get('name','')
    description = post_body.get('description','')
    level = post_body.get('level','')
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

@app.route('/api/users/')
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200

@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    netid = post_body.get('netid','')
    password = post_body.get('password','')
    user = User(
        netid = netid,
        password = password
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
