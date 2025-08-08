import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import requests
from datetime import datetime as dat
import dash_bootstrap_components as dbc
import time
import json

from server import app
from dotenv import load_dotenv
import os



# Ruta base del proyecto
BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
########################
host = os.environ.get('IP_API')
port = os.environ.get('PORT')
port_reporte = os.environ.get('PORT_REPORTE')
# ##########################################   MENSAJES DEL .ENV
msj1 = os.environ.get('MSJ1')
msj2 = os.environ.get('MSJ2')
msj3 = os.environ.get('MSJ3')

##################################################
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
color_header = '#111111'
color_card1 = '#1c2833'
color_card2 = '#1c2833'
color_card3 = '#1c2833'
color_card4 = '#1c2833'
hora=dat.now()

layout = html.Div([html.H1('En Mantenimiento')
################################################################

])
#############################################callback MOSTRAR SELECCION DE INFORMES

