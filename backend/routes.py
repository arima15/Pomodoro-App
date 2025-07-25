from flask import Blueprint

main = Blueprint('main', __name__)

# Example route (to be replaced with real endpoints)
@main.route('/')
def index():
    return 'Pomodoro App Backend is running.' 