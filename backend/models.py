from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy (to be used in app.py)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    activities = db.relationship('Activity', backref='user', cascade='all, delete-orphan')
    sessions = db.relationship('PomodoroSession', backref='user', cascade='all, delete-orphan')
    streaks = db.relationship('Streak', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20))  # Optional, for UI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sessions = db.relationship('PomodoroSession', backref='activity', cascade='all, delete-orphan')
    streaks = db.relationship('Streak', backref='activity', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Activity {self.name}>'

class PomodoroSession(db.Model):
    __tablename__ = 'pomodoro_sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # Store in seconds or minutes

    def __repr__(self):
        return f'<PomodoroSession {self.id} - User {self.user_id} - Activity {self.activity_id}>'

class Streak(db.Model):
    __tablename__ = 'streaks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    streak_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Streak {self.id} - User {self.user_id} - Activity {self.activity_id}>' 