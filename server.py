# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin

import dash_bootstrap_components as dbc
from dotenv import load_dotenv

#engine = create_engine(config.get('database', 'con'))
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
# DEFINE THE DATABASE CREDENTIALS



external_stylesheets = [
    dbc.themes.COSMO, # Bootswatch theme
    'https://use.fontawesome.com/releases/v5.9.0/css/all.css', # for social media icons
]
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.DARKLY], meta_tags=[{'charset': 'utf-8',},{'name': 'viewport','content': 'width=device-width, initial-scale=1, shrink-to-fit=no'}])
#app=dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server.config.update(SECRET_KEY='hardsecretkey')


# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
