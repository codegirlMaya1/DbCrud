from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:568312@localhost/gymdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)

class WorkoutSession(db.Model):
    session_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    session_date = db.Column(db.Date)
    session_time = db.Column(db.String(50))
    activity = db.Column(db.String(255))

member = db.relationship('Member', backref=db.backref('workoutsessions', lazy=True))

from flask import request, jsonify

@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    age = request.json['age']
    new_member = Member(name=name, age=age)
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'New member added'}), 201

@app.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{'id': member.id, 'name': member.name, 'age': member.age} for member in members])

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    member.name = request.json['name']
    member.age = request.json['age']
    db.session.commit()
    return jsonify({'message': 'Member updated'})

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted'})

@app.route('/workoutsessions', methods=['POST'])
def add_workoutsession():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    session_time = request.json['session_time']
    activity = request.json['activity']
    new_session = WorkoutSession(member_id=member_id, session_date=session_date, session_time=session_time, activity=activity)
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'New workout session added'}), 201

@app.route('/workoutsessions', methods=['GET'])
def get_workoutsessions():
    sessions = WorkoutSession.query.all()
    return jsonify([{'session_id': session.session_id, 'member_id': session.member_id, 'session_date': session.session_date, 'session_time': session.session_time, 'activity': session.activity} for session in sessions])

@app.route('/workoutsessions/<int:session_id>', methods=['PUT'])
def update_workoutsession(session_id):
    session = WorkoutSession.query.get(session_id)
    if not session:
        return jsonify({'message': 'Session not found'}), 404
    session.session_date = request.json['session_date']
    session.session_time = request.json['session_time']
    session.activity = request.json['activity']
    db.session.commit()
    return jsonify({'message': 'Session updated'})

@app.route('/workoutsessions/<int:session_id>', methods=['DELETE'])
def delete_workoutsession(session_id):
    session = WorkoutSession.query.get(session_id)
    if not session:
        return jsonify({'message': 'Session not found'}), 404
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Session deleted'})

@app.route('/members/<int:member_id>/workoutsessions', methods=['GET'])
def get_member_workoutsessions(member_id):
    sessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    return jsonify([{'session_id': session.session_id, 'session_date': session.session_date, 'session_time': session.session_time, 'activity': session.activity} for session in sessions])

if __name__ == '__main__':
    app.run(port=5000)