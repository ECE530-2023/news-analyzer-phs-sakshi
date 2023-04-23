import os
from flask import Flask
from flask_dance.contrib.google import make_google_blueprint


from flask_login import LoginManager

from configuration.config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


google_blueprint = make_google_blueprint(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    scope=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_url="/index"
)

app.register_blueprint(google_blueprint, url_prefix="/login")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
