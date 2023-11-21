"""  
CMSC Team 5
Perform testing of ResNet-152 processing
Paul Wojcik, Jack Boswell, Andrew Rios, Nelson Romero, Nikhil Thomas
"""

from flask import Blueprint, g, redirect, render_template, request, session, url_for
from importlib.resources import files

from .utils.web_image import WebImage
from .models.resnet_152 import resnet_152_analysis

driver_blueprint = Blueprint("models", __name__, url_prefix="/models")

@driver_blueprint.route('/resnet152', methods=('GET', 'POST'))
def flask_resnet_152_analysis():
    """Process image using ResNet-152"""
    try:
        web_image = WebImage(session["image_filepath"])
    except FileNotFoundError:
            return redirect(url_for('index'))
    results = resnet_152_analysis(web_image)

    return render_template('results.html', results=results["ResNet-152"])