from flask import Blueprint

ai_bp = Blueprint('ai', __name__, template_folder="ai" ,url_prefix='/ai')
from . import routes