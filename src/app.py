""" main app class to register all blueprints and make the Flask app """
import os
from flask import Flask
from flask_dance.contrib.google import make_google_blueprint
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "supersecretkey"


google_blueprint = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    scope=["https://www.googleapis.com/auth/userinfo.email",
           "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_url="/"
)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "News-Analyzer-API documentation"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

app.register_blueprint(google_blueprint, url_prefix="/login")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
