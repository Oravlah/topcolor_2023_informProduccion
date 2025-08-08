# Dash app initialization
import dash
# User management initialization
import os
from flask_login import LoginManager, UserMixin
from users_mgt import db, User as base
from config import config
import dash_bootstrap_components as dbc
from dotenv import load_dotenv

#engine = create_engine(config.get('database', 'con'))
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
# DEFINE THE DATABASE CREDENTIALS
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')
host = os.environ.get('IP_SERVIDOR')
port = os.environ.get('DB_PORT')
database = os.environ.get('DB_NAME')


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


# config
#server.config.update(SECRET_KEY=os.urandom(12),SQLALCHEMY_DATABASE_URI=config.get('database', 'con'),SQLALCHEMY_TRACK_MODIFICATIONS=False)
server.config.update(SECRET_KEY='hardsecretkey',SQLALCHEMY_DATABASE_URI=f'mysql+pymysql://{user}:{password}@{host}/{database}',SQLALCHEMY_TRACK_MODIFICATIONS=False)

#server.config['SECRET_KEY'] = 'hardsecretkey'
#server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://localvesatuser:070GITOOITU012tdotrwc024GTGFAE007wawftdotr700@10.6.0.7/topcolor2'
#server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(server)

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
