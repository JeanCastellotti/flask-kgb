from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle

# Application
app = Flask(__name__)
app.config.from_pyfile('settings.py')

# Database ORM
db = SQLAlchemy(app)

# Stylus
assets = Environment(app)
stylus = Bundle('css/src/main.styl',
                depends='css/src/partials/**.styl',
                filters='stylus,autoprefixer6,cssmin',
                output='css/style.css')
assets.register('stylus', stylus)
