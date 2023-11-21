"""  
CMSC Team 5
A preliminary Browser-based GUI
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
"""

from datetime import datetime
import os
from pathlib import Path

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from . import model_driver

def get_project_root() -> Path:
    "Get path of project root folder"
    return Path(__file__).parent

def create_app(test_config=None) -> Flask:
    """Create Flask App"""
    app = Flask(__name__)
    
    # Secret Key Needed for Session Data
    app.config["SECRET_KEY"] = '82af34baa11e09830d85ed0a984f68d6b6175db9b87fd6ba8f7bd424aa0ba867'

    # Set default image upload folder
    app.config["UPLOAD_FOLDER"] = os.path.join(get_project_root(), 'static/uploads')

    @app.context_processor
    def get_date() -> str:
        """Returns date formatted as DayOfWeek, Mon Day, Year"""
        return { 'date' : datetime.now().strftime("%A, %b %d, %Y") }

    @app.context_processor
    def get_time() -> str:
        """Get time formatted as HH:MM:SS AM/PM"""
        return { "time" : datetime.now().strftime("%I:%M:%S %p") }

    @app.route('/', methods=('GET', 'POST'))
    def index():
        """create index page"""
        if request.method == "POST":

            # Save uploaded image
            image = request.files["file"]
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            session["image_filepath"] = os.path.join(app.config["UPLOAD_FOLDER"], filename) # Save image filepath for image processing in a later context
            image.save(session["image_filepath"])

            # Display uploaded image
            return render_template("index.html", image_uploaded="true",
                                   image=url_for("static", filename="uploads/" + filename))
        else:

            # Display default image
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], "frankie.jpg")
            session["image_filepath"] = os.path.join(app.config["UPLOAD_FOLDER"], filename) # Save image filepath for image processing in a later context
            image.save(session["image_filepath"])
            return render_template("index.html", image=filepath, image_uploaded="true")

    @app.route('/clearImage', methods=('GET', 'POST'))
    def clear_image():
        """Delete image off of server"""
        #TODO: Need to figure out how to do this if the session ends
        try:
            os.remove(session["image_filepath"])
            session.pop('image_filepath')
        except KeyError:
            pass
          
        return redirect(url_for('index'))
    
    # Register model blueprints for image processing
    app.register_blueprint(model_driver.driver_blueprint)
        
    return app
