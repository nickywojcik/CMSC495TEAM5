"""  
CMSC Team 5
A preliminary Browser-based GUI
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
"""

from datetime import datetime
from flask import Flask, render_template

def get_date() -> str:
    """Returns date formatted as DayOfWeek, Mon Day, Year"""
    return datetime.now().strftime("%A, %b %d, %Y")

def get_time() -> str:
    """Get time formatted as HH:MM:SS AM/PM"""
    return datetime.now().strftime("%I:%M:%S %p")

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        """create index page"""
        return render_template("index.html", date=get_date(), time=get_time())

    return app