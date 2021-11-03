from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

# Application
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Bcrypt
bcrypt = Bcrypt(app)

# Login
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'warning'

# Database ORM
db = SQLAlchemy(app)

# Stylus
assets = Environment(app)
stylus = Bundle('css/src/main.styl',
                depends='css/src/partials/**.styl',
                filters='stylus,autoprefixer6,cssmin',
                output='css/style.css')
assets.register('stylus', stylus)

from main.routes import main
from auth.routes import auth
from admin.routes import admin

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)
