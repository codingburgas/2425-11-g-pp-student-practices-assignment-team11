from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()

def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    from .auth import models
    from .survey import models
    from .companies import models

    with app.app_context():
        db.create_all()

    from .auth import auth_bp
    from .main import main_bp
    from .profile import profile_bp
    from .errors import errors_bp
    from .survey import survey_bp
    from .AI import ai_bp
    from .companies import companies_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(errors_bp)
    app.register_blueprint(survey_bp, url_prefix='/survey')
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(companies_bp, url_prefix='/companies')

    return app