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
host_ege = os.environ.get('IP_API_EGE')



lineas=[1,2,3,4,5,6,7,8,9,10,11,12] #lineas reales 1,2,3,4,5,6,7,adtv,bla,8...
nombre_lineas=["7","aditivo",3]



hora=dat.now()

layout = html.Div([
    dcc.Location(id='urlmantener_config', refresh=True),
    dcc.Location(id='url_msj_ok', refresh=True),
                        dbc.Row([dbc.Col([], width=2),
                             dbc.Col([dbc.Card([
                                 dbc.CardBody([html.H4('Agregar Correo', style={'text-align': 'center'}),

                                          dbc.Row([dbc.Col([ dcc.Input(value='', type='text', id='input_msj', placeholder='Ingrese Correo',
                                                         style={"width": "100%", 'background-color': 'black',
                                                                'color': 'white', 'text-align': 'center',
                                                                'font-size': '30px', 'font-weight': 'bold',
                                                                'margin-top': '10px'})], width=12)
                                            ]),

                                         dbc.Row([dbc.Col([]),
                                                dbc.Col([dbc.Button('Agregar Correo', color="info", id='btn_ingresar', n_clicks=0,
                                                         style={'margin-top':'20px'})]),
                                                    dbc.Col([]),
                                            ]) ,
                                               dbc.Row([dbc.Col([html.Div(id='tabla_email',style={'margin-top':'20px'}),
                                                        dcc.Interval(id='interval_tabla_email', interval=10000, n_intervals=0),

                                                        ])
                                                        ]),
                                               dbc.Row([
                                            dbc.Col([html.Div(id='result_conf',style={'margin-left':'30px','margin-top':'20px'}),
                                             html.Div(id='mostrar_btn',style={'margin-left':'160px','margin-top':'20px'})])

                                               ]),



                                               ])],
                                 style={ 'border': 'black 2px solid', 'text-align': 'center',
                                        'margin-left': '5px', 'margin-top': '10px'})


                             ], width=8),


                    ]),









dbc.Row([dbc.Col([html.Div(id='res1_conf')])]),
])



############################################################################# CALLBACK CON INPUT PARA MODIFICAR MENSAJES 1 2 3
@app.callback(
    Output('tabla_email', 'children'),
    [Input('interval_tabla_email', 'n_intervals')])
def update_show_tabla(value):
    print(f"callback tabla")
    datos = {
        'Nombre': ['Jose Garcia','Juan Gomez','Jose Garcia','Juan Gomez'],
        'Correo': ['Jose.Garcia@gmail.com','Juan.Gomez@gmail.com','Jose.Garcia@gmail.com','Juan.Gomez@gmail.com'],


    }

    df_tiempo = pd.DataFrame(datos)

    return html.Div([dash_table.DataTable(
        columns=[{'id': c, 'name': c} for c in df_tiempo.columns],
        data=df_tiempo.to_dict('records'),
        style_header={'backgroundColor': '  #229954 ',
                      'color': 'white',
                      'font-size': '25px',
                      'font-weight': 'bolder',
                      'font-family': 'sans-serif '},
        style_cell={
            'backgroundColor': 'white',
            'font-size': '20px',
            'color': 'black',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'font-weight': 'bolder',
            'font-family': 'sans-serif '
        },
        style_cell_conditional=[
            {
                'padding-bottom': '5px', 'padding-top': '5px',
                'textAlign': 'center',
                'border': 'black 2px groove',
            }
        ],
        style_data_conditional=[
            {
                'if': {
                    'filter_query': '{origen} contains "TOTAL"'
                },
                'backgroundColor': '#229954',
                'color': 'white',
                'font-size': '20px'
            }
        ]
    )
    ])
#

@app.callback(dash.dependencies.Output('tabla_conf_correo', 'children'),
              [dash.dependencies.Input('btn_ingresar', 'n_clicks')])
def display_result_tabla(id):
    if n_clicks > 0:
        print('menu',menu)


########################################MENSAJE MODAL
@app.callback(
    Output("modal_conf", "is_open"),
    [Input("open_conf", "n_clicks"), Input("close_conf", "n_clicks")],
    [State("modal_conf", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def msj():
    return html.Div(
    [
        dbc.Button("Open modal", id="open_conf", n_clicks=1,style={'display':'none'}),
        dbc.Modal(
            [
                dbc.ModalHeader("TOP-COLOR"),
                dbc.ModalBody("Mensaje Ingresado correctamente"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_conf", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_conf",
            is_open=False,
        ),
    ]
)




########################################################### CALLBACK Q REDIRIGEN A HOME O A CONFIGURACION
####################################
@app.callback(Output('url_msj_ok', 'pathname'),
              [Input('volver_msj_ok', 'n_clicks')],)
def registro_volver(n_clicks):
    if n_clicks > 0:
        time.sleep(3)
        return '/configuracion'


@app.callback(Output('urlmantener_config', 'pathname'),
              [Input('mantener_config', 'n_clicks')],)
def registro_error(n_clicks):
    if n_clicks > 0:
        return '/configuracion'