from flask import request, jsonify
from .models import Member, WorkoutSession
from . import app1, db

@app1.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    new_member = Member(name=data['name'], age=data['age'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Member added successfully'}), 201

@app1.route('/members', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{'id': m.id, 'name': m.name, 'age': m.age} for m in members])

@app1.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    member.name = data['name']
    member.age = data['age']
    db.session.commit()
    return jsonify({'message': 'Member updated successfully'})

@app1.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = Member.query.get(id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member deleted successfully'})

@app1.route('/workoutsessions', methods=['POST'])
def add_workout_session():
    data = request.get_json()
    new_session = WorkoutSession(
        member_id=data['member_id'],
        session_date=data['session_date'],
        session_time=data['session_time'],
        activity=data['activity']
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({'message': 'Workout session added successfully'}), 201

@app1.route('/workoutsessions', methods=['GET'])
def get_workout_sessions():
    sessions = WorkoutSession.query.all()
    return jsonify([{
        'session_id': s.session_id,
        'member_id': s.member_id,
        'session_date': s.session_date,
        'session_time': s.session_time,
        'activity': s.activity
    } for s in sessions])

@app1.route('/workoutsessions/<int:session_id>', methods=['PUT'])
def update_workout_session(session_id):
    data = request.get_json()
    session = WorkoutSession.query.get(session_id)
    if not session:
        return jsonify({'message': 'Session not found'}), 404
    session.session_date = data['session_date']
    session.session_time = data['session_time']
    session.activity = data['activity']
    db.session.commit()
    return jsonify({'message': 'Workout session updated successfully'})

@app1.route('/workoutsessions/<int:session_id>', methods=['DELETE'])
def delete_workout_session(session_id):
    session = WorkoutSession.query.get(session_id)
    if not session:
        return jsonify({'message': 'Session not found'}), 404
    db.session.delete(session)
    db.session.commit()
    return jsonify({'message': 'Workout session deleted successfully'})

@app1.route('/members/<int:member_id>/workoutsessions', methods=['GET'])
def get_member_workout_sessions(member_id):
    sessions = WorkoutSession.query.filter_by(member_id=member_id).all()
    return jsonify([{
        'session_id': s.session_id,
        'session_date': s.session_date,
        'session_time': s.session_time,
        'activity': s.activity
    } for s in sessions])

if __name__ == '__main__':
    app1.run(port=5000)
