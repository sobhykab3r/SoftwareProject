from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from flask_wtf.csrf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
photos = UploadSet("photos", IMAGES)
mail = Mail()
simple = SimpleMDE()
csrf = CSRFProtect()

def create_app(config_name):
    
    app = Flask(__name__)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)
    csrf.init_app(app)

    # Registering the main app Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Registering auth blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/authenticate')
    
    # Setting config
    from .request import configure_request
    configure_request(app)

    # Configure UploadSet
    configure_uploads(app, photos)

    return app
