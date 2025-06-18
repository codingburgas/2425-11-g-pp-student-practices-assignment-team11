from flask import Blueprint

errors_bp = Blueprint('errors', __name__, url_prefix='/errors')

from . import routes