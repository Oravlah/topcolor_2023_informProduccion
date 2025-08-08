import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State

from datetime import datetime as dat
import dash_bootstrap_components as dbc
import time
import json
import requests

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
linea='11'
linea_sig='home'



hora=dat.now()

layout = html.Div([
dcc.Location(id='url_linea'+linea, refresh=True),
dcc.Location(id='url_rehacer'+linea, refresh=True),
                    dbc.Row([
                        dbc.Col([
dbc.Card([
            dbc.CardBody([
                dbc.Row([dbc.Col([dcc.Input(value='xxxxx', type='text', id='id_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "20%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),
                         dbc.Col([html.H3('Informe Línea '+linea)]),
                         dbc.Col([dcc.Input(value='xxxxx', type='text', id='id_rehacer'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "20%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})])]),
            dbc.Row([dbc.Col([html.Div('Fecha',style={"margin-top": '20px'})]),
                         dbc.Col([html.Div('Turno',style={"margin-top": '20px'})]),
                        dbc.Col([html.Div('Operador',style={"margin-top": '20px'})]),
                        dbc.Col([html.Div('Ayudante',style={"margin-top": '20px'})]),

                         ]),
                          dbc.Row([
                                   dbc.Col([dcc.Input(value='00/00', type='text', id='fecha_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),
                                    dbc.Col([dcc.Input(value='--', type='text', id='turno_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),

                                    dbc.Col([dcc.Input(value='--', type='text', id='operador_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),

                                    dbc.Col([dcc.Input(value='--', type='text', id='ayudante_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),



                                   ]),


#################################################################################################
                                dbc.Row([dbc.Col([html.Div('Balance masa',style={"margin-top": '20px'})]),
                                     dbc.Col([html.Div('Rendimiento',style={"margin-top": '20px'})]),
                                    dbc.Col([html.Div('Kg Fabricación Turno',style={"margin-top": '20px'})]),
                                    dbc.Col([html.Div('Kg Fabricación Total',style={"margin-top": '20px'})]),

                                     ]),
                                dbc.Row([
                                   dbc.Col([dcc.Input(value='--', type='text', id='balance_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),
                                    dbc.Col([dcc.Input(value='--', type='text', id='rendimiento_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),

                                    dbc.Col([dcc.Input(value='--', type='text', id='fabturno_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),

                                    dbc.Col([dcc.Input(value='--', type='text', id='fabtotal_lin'+linea, disabled=True,
                                                      style={'margin-top': '5px', "width": "100%",
                                                             'background-color': 'black', 'color': 'white',
                                                             'text-align': 'center', 'font-size': '25px'})]),



                                   ]),
###################################################################################################################
                dbc.Row([dbc.Col([html.H5('Observación', style={"margin-top": '30px'})]),


                         ]),
                            dbc.Row([dbc.Col([
                                        dcc.Textarea(placeholder='Ingrese Observación',id="text_area_lin"+linea,value='',
                                                     style={"width": "80%", 'margin-top': '20px','margin-bottom':'5px','background-color': 'black', 'color': 'white'},
                                                     cols=15, rows=3),
                                                dcc.Interval(id='interval_linea'+linea, interval=30000, n_intervals=0),

                            ]),

                            ]),
#######################################################################################################################
                    dbc.Row([
                        dbc.Col([dcc.ConfirmDialogProvider(children=html.Button('Guardar Informe',
                                                                                style={"margin-top": '20px',
                                                                                       'font-size': '20px'}),
                                                           id='btn_guardar_lin'+linea,
                                                           message='Seguro Desea Guardar Informe?',
                                                           )])
                    ]),
######################################################################################################################3
                    dbc.Row([
                        dbc.Col([html.Div(id='result'+linea,style={"margin-top": '20px'})]),
                        dbc.Col([html.Div(id='result_rehacer'+linea,style={"margin-top": '20px'})]),
                    ]),


                          ])],color='#1c2833',
            style={"width": "90rem", 'border': 'black 2px solid', 'margin-left': '100px','text-align':'center',
                    'margin-top': '10px'}
        )
                        ])
                    ]),
###########################################################################
                    dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading"+linea,
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
####################################################################3
                    dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                        id="loading_rehacer" + linea,
                        children='',
                        type="cube",
                        style={'margin-top': '250px', 'width': '400px'}
                    )], width=6)]),
dcc.Store(id='data-store-crear', storage_type='session'),
dcc.Store(id='data-store-rehacer', storage_type='session'),
])


##################################################### CALLBACK MUESTRA LOS DATOS GUARDADOS DEL INFORME LINEA 1
@app.callback(
   [Output('fecha_lin'+linea, 'value'),
    Output('turno_lin'+linea, 'value'),
    Output('operador_lin'+linea, 'value'),
    Output('ayudante_lin'+linea, 'value'),
    Output('balance_lin'+linea, 'value'),
    Output('rendimiento_lin'+linea, 'value'),
    Output('fabturno_lin'+linea, 'value'),
    Output('fabtotal_lin'+linea, 'value'),],
[Input('interval_linea'+linea, 'n_intervals')])
def update_valores_lin(id):
    print()
    try:
        fecha='2023-03-17'
        turno='A'
        operador='Jose G'
        ayudante='Pedro P'
        balance='--'
        rendimiento='50%'
        fab_turno='430'
        fab_total='800'
        return fecha,turno,operador,ayudante,balance,rendimiento,fab_turno,fab_total
    except:
        exception='---'
        return exception,exception,exception,exception,exception,exception,exception,exception


####################################################CALLBACK QUE RECIBE ID
@app.callback(
    dash.dependencies.Output('id_lin'+linea, 'value'),
    [dash.dependencies.Input('data-store-crear', 'modified_timestamp')],
    [dash.dependencies.State('data-store-crear', 'data')]
)
def receive_data(timestamp, data):
    if timestamp is not None:
        return f'{data}'

####################################################CALLBACK QUE RECIBE ID REHACER
@app.callback(
    dash.dependencies.Output('id_rehacer'+linea, 'value'),
    [dash.dependencies.Input('data-store-rehacer', 'modified_timestamp')],
    [dash.dependencies.State('data-store-rehacer', 'data')]
)
def receive_data(timestamp, data):
    if timestamp is not None:
        return f'{data}'
##################################################CALLBACK CREAR INFORME Y PASAR A LINEA 2

@app.callback(
    [Output('result'+linea,'children'),
   Output('url_linea'+linea,'pathname'),
Output('loading' + linea, 'children')],
[Input('btn_guardar_lin'+linea, 'submit_n_clicks')],
[State('text_area_lin'+linea, 'value'),
State('id_lin'+linea, 'value'),
]
)
def update_crear_in(submit_n_clicks,  obs,id):
    print()

    if not submit_n_clicks:
        return '','/informe_lin'+linea,''
    if obs == '':
        return html.H4('Debe Ingresar Observación', style={ 'color': 'red'}),'/informe_lin'+linea,''
    else:
        payload = {
            'id_reporte': id,
            'Observacion': obs,
            'linea': linea,

        }
        r = requests.post('http://' + host + ':' + port_reporte + '/observaciones__lineas', json=payload)

        respuesta = json.loads(r.text)
        print('resp1',respuesta)

        return 'ok','/'+linea_sig,html.Div(id="loading")

##################################################CALLBACK REHACER INFORME Y PASAR A LINEA 2

@app.callback(
    [Output('result_rehacer'+linea,'children'),
   Output('url_rehacer'+linea,'pathname'),
     Output('loading_rehacer'+linea,'children')],
[Input('btn_guardar_lin'+linea, 'submit_n_clicks')],
[State('text_area_lin'+linea, 'value'),
State('id_rehacer'+linea, 'value'),
]
)
def update_crear_in(submit_n_clicks,  obs,id):
    print()

    if not submit_n_clicks:
        return '','/informe_lin'+linea,''
    if obs == '':
        return html.H4('Debe Ingresar Observación', style={ 'color': 'red'}),'/informe_lin'+linea,''
    else:
        payload = {
            'id_reporte': id,
            'Observacion': obs,
            'linea': linea,

        }
        r = requests.post('http://' + host + ':' + port_reporte + '/observaciones__lineas', json=payload)

        respuesta = json.loads(r.text)
        print('resp1',respuesta)

        return 'ok','/informe_lin'+linea_sig,html.Div(id="loading")