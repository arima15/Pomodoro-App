# This is an edit to an existing file: backend/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Activity, PomodoroSession, Streak, User
from datetime import datetime, date

main = Blueprint('main', __name__)

# CRUD for Activities
@main.route('/activities', methods=['POST'])
@jwt_required()
def create_activity():
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name')
    color = data.get('color')
    if not name:
        return jsonify({'msg': 'Activity name required'}), 400
    activity = Activity(user_id=user_id, name=name, color=color)
    db.session.add(activity)
    db.session.commit()
    return jsonify({'msg': 'Activity created', 'id': activity.id}), 201

@main.route('/activities', methods=['GET'])
@jwt_required()
def get_activities():
    user_id = get_jwt_identity()
    activities = Activity.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': a.id, 'name': a.name, 'color': a.color} for a in activities]), 200

@main.route('/activities/<int:activity_id>', methods=['PUT'])
@jwt_required()
def update_activity(activity_id):
    user_id = get_jwt_identity()
    activity = Activity.query.filter_by(id=activity_id, user_id=user_id).first()
    if not activity:
        return jsonify({'msg': 'Activity not found'}), 404
    data = request.get_json()
    activity.name = data.get('name', activity.name)
    activity.color = data.get('color', activity.color)
    db.session.commit()
    return jsonify({'msg': 'Activity updated'}), 200

@main.route('/activities/<int:activity_id>', methods=['DELETE'])
@jwt_required()
def delete_activity(activity_id):
    user_id = get_jwt_identity()
    activity = Activity.query.filter_by(id=activity_id, user_id=user_id).first()
    if not activity:
        return jsonify({'msg': 'Activity not found'}), 404
    db.session.delete(activity)
    db.session.commit()
    return jsonify({'msg': 'Activity deleted'}), 200

# Start Pomodoro Session
@main.route('/sessions/start', methods=['POST'])
@jwt_required()
def start_session():
    user_id = get_jwt_identity()
    data = request.get_json()
    activity_id = data.get('activity_id')
    start_time = datetime.utcnow()
    session = PomodoroSession(user_id=user_id, activity_id=activity_id, start_time=start_time, end_time=start_time, duration=0)
    db.session.add(session)
    db.session.commit()
    return jsonify({'msg': 'Session started', 'session_id': session.id}), 201

# End Pomodoro Session
@main.route('/sessions/end/<int:session_id>', methods=['POST'])
@jwt_required()
def end_session(session_id):
    user_id = get_jwt_identity()
    session = PomodoroSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not session:
        return jsonify({'msg': 'Session not found'}), 404
    end_time = datetime.utcnow()
    session.end_time = end_time
    session.duration = int((end_time - session.start_time).total_seconds())
    db.session.commit()
    return jsonify({'msg': 'Session ended', 'duration': session.duration}), 200

# Get Analytics/Streaks
@main.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    user_id = get_jwt_identity()
    # Total pomodoro sessions and total duration
    sessions = PomodoroSession.query.filter_by(user_id=user_id).all()
    total_sessions = len(sessions)
    total_duration = sum(s.duration for s in sessions)
    # Streaks: count unique days with at least one session
    unique_days = set(s.start_time.date() for s in sessions)
    streak_days = len(unique_days)
    return jsonify({
        'total_sessions': total_sessions,
        'total_duration_seconds': total_duration,
        'streak_days': streak_days
    }), 200 