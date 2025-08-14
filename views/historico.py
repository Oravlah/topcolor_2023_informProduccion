import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html

from dash.dependencies import Input, Output, State

from datetime import datetime as dat
import dash_bootstrap_components as dbc

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
lineas=[7,3,8]
nombre_lineas=["7","aditivo",3]


hora=dat.now()

layout = html.Div([
    dbc.Row([dbc.Col([], width=2),dbc.Col([dbc.Card([
            dbc.CardBody([
                dbc.Row([dbc.Col([html.Div('Seleccione Fecha')]),
                        dbc.Col([html.Div('Seleccione Línea')]),
                        dbc.Col([html.Div('Seleccione Turno')]),
                         ]),

                dbc.Row([
                    dbc.Col([dcc.DatePickerSingle(
                        id='Date_ini',
                        min_date_allowed=dat(1900, 1, 1),
                        max_date_allowed=dat.today(),
                        initial_visible_month=dat.today(),
                        date=str(dat.today()),
                        clearable=True,
                        with_portal=True,
                        display_format='YYYY-MM-DD',
                        stay_open_on_select=False,
                        first_day_of_week=1,
                        style={'margin-left': '5px','width': '100%'}

                    )
                    ]),
                    dbc.Col([dcc.Dropdown(id='menu_lineas_hist',options=[{'label':'Línea 1', 'value':'linea1' },
                                                {'label':'Línea 2', 'value':'linea2' },
                                                {'label': 'Línea 3', 'value': 'linea3'},
                                                {'label':'Línea 4', 'value':'linea4' },
                                                {'label':'Línea 5', 'value':'linea5' },
                                                {'label': 'Línea 6', 'value': 'linea6'},
                                                {'label': 'Línea 7', 'value': 'linea7'},
                                                {'label': 'Línea 8', 'value': 'linea8'},
                                                {'label': 'Línea 9', 'value': 'linea9'},
                                                {'label': 'Línea 10', 'value': 'linea10'},
                                                {'label': 'Línea 11', 'value': 'linea11'},
                                                {'label': 'Línea 12', 'value': 'linea12'},
                                                 ], value='', clearable=False, placeholder='Seleccione Linea',
                                                    style={'width': '100%', 'color': 'black', 'margin-top': '5px'})]),
                    dbc.Col([dcc.Dropdown(id='menu_turno_hist',options=[{'label':'A', 'value':'A' },
                                                  {'label':'B', 'value':'B' }], value='A', clearable=False, placeholder='Seleccione Turno',
                                                    style={'width': '100%', 'color': 'black', 'margin-top': '5px'})]),

                ]),

                dbc.Row([dbc.Col([dbc.Button('Ver Gráfico', color="info", id='btn_ver_grafico', n_clicks=0, style={'margin-left':'1px','margin-top':'20px'})])]),
])
], color="primary", inverse=True, style={"width": "65rem", "margin-top": '10px','margin-left':'80px', 'border': 'black 1px solid','text-align':'center'}
    ),
    ], width=5),

]),
########################################################################################
                    dbc.Row([dbc.Col([html.Div(id='tabla_hist_1', style={"margin-top":'20px',"margin-left":'50px'}),
                                    dcc.Interval(id='interval_tabla_1', interval=10000, n_intervals=0),

                             ], width=11)]),
    #############################################################################################
                        dbc.Row([dbc.Col([dbc.Row([html.Div(id='grafico_hist_1', style={"margin-top":'30px',"margin-left":'50px'}),
                                    dcc.Interval(id='interval_hist_1', interval=10000, n_intervals=0)]),

                             ], width=11)]),

#################################################################################################
    dbc.Row([dbc.Col([html.Div(id='tabla_hist_2', style={"margin-top": '30px', "margin-left": '50px'}),
                               dcc.Interval(id='interval_tabla_2', interval=10000, n_intervals=0),

                      ], width=11)])



])


######################callback GRAFICO 1
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
@app.callback(
   Output('grafico_hist_1', 'children'),
[Input('interval_hist_1', 'n_intervals')])
def update_valor_graf(id):
    try:
        hora_ini = dat.now()
        url = f"http://{host}:{port}/grafico/&{lineas[0]}"  #tiene 5 dosificadores
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        df = pd.DataFrame(salida_json)
        fecha = dat.now()
        hora_actual = fecha.strftime("%M")
        hora_fin = dat.now()
        #diferencia = (hora_fin.timestamp() - hora_ini.timestamp())

        df['date'] = pd.to_datetime(df['fecha'], unit='ms')

        df_hora = df.loc[:, 'date']
        r40001 = df.loc[:, 'r40001']
        r40003 = df.loc[:, 'r40003']

        return html.Div([dcc.Graph(figure={
            'data': [
                {'x': df_hora, 'y': r40001, 'type': 'line',  'name': 'Set[kg/h]','line': {'color': 'yellow' }},
                {'x': df_hora, 'y': r40003, 'type': 'line','name': 'Flujo Total[kg/h]','line': {'color': 'red' }},


            ],
                'layout': {
                    'title': 'Gráfico 1',
                    'height':300,
                    'width': 1670,
                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text']
                    },

                }
            }),

                            ]),
    except:
        return html.Div([html.H2('Sin Conexión')])

##########################################################################
@app.callback(
   Output('tabla_hist_1', 'children'),
[Input('interval_tabla_1', 'n_intervals')])
def update_valor_tabla(id):
    print()
    return html.Div([dt.DataTable(

                                            columns=[{'name': 'Hora', 'id': 'valor1'},
                                                     {'name': 'Set', 'id': 'valor2'},
                                                     {'name': 'Real', 'id': 'valor3'},
                                                     {'name': 'Producto', 'id': 'valor4'},
                                                     {'name': 'Operacion', 'id': 'valor5'},
                                                     {'name': 'cantidad', 'id': 'valor6'},
                                                     ],
                                            data=[{'valor1': '10:00', 'valor2': '4545','valor3': '100', 'valor4': '4545','valor5': '100', 'valor6': '4545'},


                                                  ],
        style_header={
            'font-size': '30px',
            'border': 'black 1px solid',
            'backgroundColor': 'black',

        },
        style_cell={
            'color': 'white',
            'backgroundColor': ' #3498db',
            'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px',
            'padding-bottom': '10px',
            'font-size': '20px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            # 'minWidth': 90, 'maxWidth': 90, 'width': 90

        },
                                            style_cell_conditional=[
                                                {
                                                    'padding-left': '5px', 'padding-right': '5px',
                                                    'textAlign': 'center',
                                                    'border': 'black 2px solid',
                                                }
                                            ],

                                        ),
                                        ])

##########################################################################
@app.callback(
   Output('tabla_hist_2', 'children'),
[Input('interval_tabla_2', 'n_intervals')])
def update_valor_tabla2(id):
    print()
    return html.Div([dt.DataTable(

        columns=[{'name': 'linea 1', 'id': 'valor1'},
                 {'name': 'linea 2', 'id': 'valor2'},
                 {'name': 'linea 3', 'id': 'valor3'},
                 {'name': 'linea 4', 'id': 'valor4'},
                 {'name': 'linea 5', 'id': 'valor5'},
                 ],
        data=[{'valor1': '100', 'valor2': '4545', 'valor3': '4545', 'valor4': '4545', 'valor5': '4545'},
              {'valor1': '200', 'valor2': '---', 'valor3': '4545', 'valor4': '4545', 'valor5': '4545'},
              {'valor1': '300', 'valor2': '8899', 'valor3': '4545', 'valor4': '4545', 'valor5': '4545'},
              {'valor1': '400', 'valor2': '222', 'valor3': '4545', 'valor4': '4545', 'valor5': '4545'},

              ],
        style_header={
            'font-size': '20px',
            'border': 'black 1px solid',
            'backgroundColor': 'black',

        },
        style_cell={
            'color': 'white',
            'backgroundColor': ' #1c2833',
            'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px',
            'padding-bottom': '10px',
            'font-size': '20px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            # 'minWidth': 90, 'maxWidth': 90, 'width': 90

        },
                                            style_cell_conditional=[
                                                {
                                                    'padding-left': '5px', 'padding-right': '5px',
                                                    'textAlign': 'center',
                                                    'border': 'black 2px solid',
                                                }
                                            ],

                                        ),
                                        ])