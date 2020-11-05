from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import _
from flask_babel import lazy_gettext as _l
from flask import render_template, url_for, jsonify

from flask import g
from flask_babel import get_locale

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)
app.config['JSON_AS_ASCII'] = False

@babel.localeselector
def get_locale():
	return request.accept_languages.best_match(app.config['LANGUAGES'])
	#return 'es'

@app.before_request
def before_request():
	# ...
	g.locale = str(get_locale())

from app import routes, models
	