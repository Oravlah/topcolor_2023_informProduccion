import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

import plotly.graph_objects as go
from datetime import datetime as dat
import dash_bootstrap_components as dbc
from datetime import date


import users_mgt as um


#um.create_user_table()

#um.add_user('jose','jose.1','vesat@test.com')
