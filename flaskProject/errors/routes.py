
from flask import render_template
from sqlalchemy.exc import IntegrityError


from . import errors_bp

@errors_bp.errorhandler(404)
def not_found_error(error):
    return render_template("errors/404.html"), 404


@errors_bp.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@errors_bp.errorhandler(403)
def forbidden_error(error):
    return render_template("errors/403.html"), 403


@errors_bp.errorhandler(401)
def unauthorized_error(error):
    return render_template("errors/401.html"), 401

@errors_bp.errorhandler(IntegrityError)
def integrity_error(error):
    return render_template("errors/already_registered.html"), 409

