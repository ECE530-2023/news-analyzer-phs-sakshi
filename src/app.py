from flask import Flask
from flask_dance.contrib.google import make_google_blueprint, google
import os

from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# app.config['GOOGLE_CLIENT_ID'] = '427430065548-1ldttecl3sapmnb14ho8vieh41dsi7jf.apps.googleusercontent.com'
# app.config['GOOGLE_CLIENT_SECRET'] = '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'
# app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'

google_blueprint = make_google_blueprint(
    client_id="427430065548-1ldttecl3sapmnb14ho8vieh41dsi7jf.apps.googleusercontent.com",
    client_secret="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",
    scope=["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_url="/index"
)

app.register_blueprint(google_blueprint, url_prefix="/login")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'