from flask import Blueprint

profile_bp = Blueprint('profile', __name__, template_folder="profile" ,url_prefix='/profile')
from . import routes