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
    application_required = post_body.get('application_required',None)
    club = Club(
        name = name,
        description = description,
        level = level,
        application_required = application_required
    )
    db.session.add(club)
    db.session.commit()
    return json.dumps({'success': True, 'data': club.serialize()}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
