from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime as dat
from server import app, User
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import json
import requests
import bcrypt

from dotenv import load_dotenv
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
########################

port_web = os.environ.get('PUERTO_WEB')
########################
api_login= os.environ.get('api_login')
port_login = os.environ.get('port_login')


url_login = f'http://{api_login}:{port_login}/login/'
print(url_login)


layout = html.Div(children=[dbc.Row([dbc.Col([],width=4, align='start'),
                                    dbc.Col([dbc.Card([

			                                dbc.CardBody(
				                                [
                                                 html.Div(
                                                     className="container",
                                                     children=[
                                                     dcc.Location(id='url_login', refresh=True),
                                                    html.Div('''POR FAVOR INICIE SESIÓN''', id='h1'),
                                                    html.Br(),
                                                    html.Div(

                                                    children=[
                                                    dcc.Input(
                                                    placeholder='Ingrese Usuario',
                                        type='text',
                                        id='uname-box'
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    dcc.Input(
                                        placeholder='Ingrese Password',
                                        type='password',
                                        id='pwd-box'
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Button(
                                        children='Logín',
                                        n_clicks=0,
                                        type='submit',
                                        id='login-button'
                                    ),
                                    html.Div(children='', id='output-state')
                                ]
                            ),
                        ]
                    )
				]

			),
dbc.CardImg(src='assets/logovesat.png',top=True),
			# dbc.CardFooter("This is the footer"),
		], color="primary", inverse=True, style={"width": "35rem", "margin-top": '5px', 'border': 'black 1px solid','text-align':'center'},
		)

],width=4, align='center')

]),
################################# STORE QUE RECIBE LOS DATOS DESDE EL MAIN    ##############
dcc.Store(id='data-store-datos', storage_type='session'),

########################### ACA EL STORE QUE CAPTURA EL ROL DEL USUARIO
dcc.Store(id='data-store-rol', storage_type='session'),

    ]
)


@app.callback([Output('url_login', 'pathname'),
                Output('output-state', 'children'),
               Output('data-store-rol', 'data')],
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    print(f"los input del login son {input1}  {input2}")
    if n_clicks > 0:
        if not input1 or not input2:
            return '/login','Debe Completar Los Datos','0'
        if input1!=None and input2!=None:
            hora = dat.now()
            pas_hash = bcrypt.hashpw(input2.encode(), bcrypt.gensalt()).decode()
            hora_post = hora.strftime("%Y-%m-%d %H:%M:%S")
            payload = {

                'username': input1,
                #'fecha': hora_post,
                'password': pas_hash,
                #'mensaje': 'nada',


            }

            r = requests.post(url_login, json=payload)
            print('payload', payload)
            response_dict = json.loads(r.text)
            print('respuesta post login1', response_dict)



            if response_dict['authorized'] == True:
                rol = response_dict['role']
                user = User(input1)
                login_user(user)
            #if estado == 0:
                return '/home','', rol
            else:
                return '/login','Usuario o Passwor Incorrectos','0'
        else:
            return '/login','','0'
    else:
        return '/login','','0'