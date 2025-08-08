import configparser
from sqlalchemy import create_engine

from dotenv import load_dotenv
import os

config = configparser.ConfigParser()
config.read('config.txt')

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


connection_string = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
#print(connection_string)

engine = create_engine(connection_string, echo=True)