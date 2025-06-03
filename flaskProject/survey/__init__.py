from flask import Blueprint

survey_bp = Blueprint('survey', __name__, template_folder="survey" ,url_prefix='/survey')
from . import routes