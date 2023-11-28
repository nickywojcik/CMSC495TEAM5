"""  
CMSC Team 5
A preliminary Browser-based GUI
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell and Paul Wojcik
"""

from datetime import datetime
import os
from pathlib import Path

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

def get_project_root() -> Path:
    """Get path of project root folder"""
    return Path(__file__).parent

def create_upload_dir() -> None:
    """Create static/uploads if non-existent"""
    Path("neural_network_evaluator/static/uploads").mkdir(parents=True, exist_ok=True)

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

            # Get rid of existing image and Save uploaded image
            clear_image()
            try:

                # TODO: Clean up below mess
                image = request.files["file"]
                filename = secure_filename(image.filename)
                session["image_filename"] = filename
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                session["image_filepath"] = os.path.join(app.config["UPLOAD_FOLDER"], filename) # Save image filepath for image processing in a later context
                create_upload_dir()
                image.save(session["image_filepath"])
            except FileNotFoundError:
                return redirect(url_for('index'))
            # Display uploaded image
            return render_template("index.html", image_uploaded="true",
                                   image=url_for("static", filename="uploads/" + filename))
        else:

            # Display default image
            filename = "frankie.jpg"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            return render_template("index.html", image_uploaded="false", image=url_for("static", filename=filename))

    @app.route('/clearImage', methods=('GET', 'POST'))
    def clear_image():
        """Delete image off of server"""
        #TODO: Need to figure out how to do this if the session ends
        try:
            os.remove(session["image_filepath"])
            session.pop('image_filepath')
        except (KeyError, FileNotFoundError) as e:
            pass
          
        return redirect(url_for('index'))
    
    # Register model blueprints for image processing
    # No longer necessary; leaving in temporarily due to Design Plan
    # TODO: Need wayahead on Flask endpoints
    #app.register_blueprint(model_driver.driver_blueprint)

    @app.route('/results', methods=('GET', 'POST'))
    def return_results():
        """Get PyTorch CNN Image classification results"""
        try:
            web_image = WebImage(session["image_filepath"])
        except FileNotFoundError:
            return redirect(url_for('index'))
        
        # Create Models
        factory = ModelFactory()
        resnet152_model = factory.create_model("resnet152")
        densenet201_model = factory.create_model("densenet201")
        vgg19_model = factory.create_model("vgg19")

        # Analyze Image
        resnet152_model.analyze_image(web_image)
        densenet201_model.analyze_image(web_image)
        vgg19_model.analyze_image(web_image)

        # Compile Results
        results = AnalysisResults()
        results.add_result(resnet152_model.get_top_results())
        results.add_result(densenet201_model.get_top_results())
        results.add_result(vgg19_model.get_top_results())

        return render_template('results.html', resnet_results=results.get_results()["resnet152"], 
                               densenet_results=results.get_results()["densenet201"],
                               vgg_results=results.get_results()["vgg19"],
                               highest_averaged_results=results.get_highest_averaged_result(),
                               image=url_for('static', filename='uploads/' + session["image_filename"]))
        
    return app
