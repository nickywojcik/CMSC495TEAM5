"""  
CMSC Team 5
A preliminary Browser-based GUI
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
Written by Jack Boswell and Paul Wojcik
"""

from datetime import datetime
import os
import uuid
from pathlib import Path
import shutil

from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.utils import secure_filename

from neural_network_evaluator.models import ModelFactory
from neural_network_evaluator.utils import AnalysisResults, WebImage

def get_project_root() -> Path:
    """Get path of project root folder"""
    return Path(__file__).parent

def create_upload_dir() -> None:
    """Create static/uploads if non-existent"""
    if 'user' in session:
        Path("neural_network_evaluator/static/uploads/" + session["user"]).mkdir(parents=True, exist_ok=True)
        return
    
    Path("neural_network_evaluator/static/uploads").mkdir(parents=True, exist_ok=True)

def create_app(test_config=None) -> Flask:
    """Create Flask App"""
    app = Flask(__name__)
    
    # Secret Key Needed for Session Data
    app.config["SECRET_KEY"] = '82af34baa11e09830d85ed0a984f68d6b6175db9b87fd6ba8f7bd424aa0ba867'

    # Set default image upload folder
    app.config["UPLOAD_FOLDER"] = os.path.join(get_project_root(), 'static/uploads')

    @app.route('/', methods=('GET', 'POST'))
    def index():
        """create index page"""
        if request.method == "POST":

            # Get rid of existing image and Save uploaded image
            clear_image()
            try:
                if not 'user' in session:
                    session["user"] = str(uuid.uuid4()) # Generate unique identifier for upload folder

                # Get uploaded image
                image = request.files["file"]

                # Get Image name
                session["image_filename"] = secure_filename(image.filename)

                # Get filepath of image
                session['raw_filepath'] = os.path.join(app.config["UPLOAD_FOLDER"], session["user"])

                # Get fullpath of image by both URL and filesystem pathing
                session["raw_image_filepath"] = os.path.join(session['raw_filepath'], session["image_filename"])
                session["url_image_filepath"] = os.path.join("uploads", session['user'], session["image_filename"])

                # Create upload directory
                create_upload_dir()

                # Save image to disk
                image.save(session["raw_image_filepath"])

            except FileNotFoundError:
                return redirect(url_for('index'))
            
            # Display uploaded image
            return render_template("index.html", image_uploaded="true",
                                   image=url_for("static", filename="uploads/" + session["user"] + "/" + session["image_filename"]))
        else:

            # Display default image
            return render_template("index.html", image_uploaded="false", image=url_for("static", filename="frankie.jpg"))

    @app.route('/clearImage', methods=('GET', 'POST'))
    def clear_image():
        """Delete image off of server"""
        try:
            os.remove(session["raw_image_filepath"])
            session.pop('raw_image_filepath')
        except (KeyError, FileNotFoundError) as e:
            pass
          
        return redirect(url_for('index'))
    
    @app.route('/cleanup', methods=('GET', 'POST'))
    def cleanup(error=None):
        """Cleanup user data after session expire"""
        if 'raw_filepath' in session:
            shutil.rmtree(session["raw_filepath"])
            session.clear()

        return redirect(url_for('index'))
    
    @app.route('/results', methods=('GET', 'POST'))
    def return_results():
        """Get PyTorch CNN Image classification results"""
        try:
            web_image = WebImage(session["raw_image_filepath"])
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

        # Delete objects to save memory
        del web_image, factory, resnet152_model, densenet201_model, vgg19_model

        return render_template('results.html', resnet_results=results.get_results()["resnet152"], 
                               densenet_results=results.get_results()["densenet201"],
                               vgg_results=results.get_results()["vgg19"],
                               highest_averaged_results=results.get_highest_averaged_result(),
                               image=url_for('static', filename='uploads/' + session["user"] + "/" + session["image_filename"]))
    
    return app