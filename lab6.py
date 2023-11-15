"""  
CMSC Team 5
A preliminary Browser-based GUI
Paul Wojcik
"""

from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


def get_date():
    """Get date"""
    date = datetime.now()
    date = date.strftime("%A, %b %d, %Y")
    return date

def get_time():
    """Get time"""
    time = datetime.now()
    time = time.strftime("%I:%M:%S %p")
    return time

@app.route('/home/')
def home():
    """create home page"""
    return render_template("home.html", date=get_date(), time=get_time())

if __name__ == "__main__":
    app.run()
