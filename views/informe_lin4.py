import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
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

rango_ini = os.environ.get('RANGO_INI')
rango_fin = os.environ.get('RANGO_FIN')

#range= [rango_ini, rango_fin]
range=[0,250]

linea='4'
linea_sig='5'

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


hora=dat.now()

layout = html.Div([
dcc.Location(id='url_linea'+linea, refresh=True),
dcc.Location(id='url_rehacer'+linea, refresh=True),
                    dbc.Row([
                        dbc.Col([
                dbc.Card([
                dbc.CardBody([
                dbc.Row([dbc.Col([dcc.Input(value=linea, type='text', id='input_linea' + linea, disabled=True,
                                style={'display':'none','margin-top': '5px', "width": "20%",
                                       'background-color': 'black', 'color': 'white',
                                       'text-align': 'center', 'font-size': '20px'})]),
                dbc.Col([dcc.Input(value='---', type='text', id='id_lin'+linea, disabled=True,
                                style={'margin-top': '5px', "width": "20%",
                                       'background-color': 'black', 'color': 'white',
                                       'text-align': 'center', 'font-size': '20px'})]),
             dbc.Col([html.H3('Informe Línea ' + linea)]),
             dbc.Col([dcc.Input(value='xxxxx', type='text', id='id_rehacer' + linea, disabled=True,
                                style={'display':'none','margin-top': '5px', "width": "20%",
                                       'background-color': 'black', 'color': 'white',
                                       'text-align': 'center', 'font-size': '20px'})]),
                         dbc.Col([])
                         ]),
            ])],color='#1c2833',style={ 'border': 'black 2px solid',  'text-align': 'center','margin-top': '10px','margin-left':'10px','margin-right':'10px'}),
                        ])
                    ]),
    dbc.Row([dbc.Col([dbc.Button('Ver Detalle', color="info", id='btn_ver_detalle_linea'+linea, n_clicks=1,
                                                 style={'display':'none','margin-left': '1px', 'margin-top': '10px'})], width=2),]),
    #############################################################################################CARD RESULTADO VER DETALLE 2
    dbc.Row([dbc.Col([html.Div(id='card_resultado_detalle_linea'+linea, style={"margin-top": '10px'}),

                      ], width=12)]),

    #############################################################################################CARD GRAFICO Y TABLA JUSTIFICACION 2
    dbc.Row([dbc.Col([html.Div(id='card_resultado_grafico_linea'+linea, style={"margin-top": '10px'}),

                      ], width=5),
             dbc.Col([html.Div(id='card_resultado_tabla_justif_linea'+linea, style={"margin-top": '10px'}),

                      ], width=7)
             ]),

    #############################################################################################CARD RENDIMIENTO Y OBSERVACION 2
    dbc.Row([dbc.Col([html.Div(id='card_rendimiento_linea'+linea, style={"margin-top": '10px'}),

                      ], width=5),
             dbc.Col([html.Div(id='card_observacion_linea'+linea, style={"margin-top": '10px'}),

                      ], width=7)
             ]),

    #############################################################################################CARD RENDIMIENTO Y OBSERVACION 2
    dbc.Row([dbc.Col([html.Div(id='card_btn_siguiente_linea' + linea, style={"margin-top": '10px'}),

                      ], width=12),

             ]),

    #############################################################################################CARD BTN Y DROP VER DETALLE 2
    dbc.Row([dbc.Col([html.Div(id='linea_final_linea'+linea, style={"margin-top": '30px'}),

                      ], width=12)]),
    ####################################################################################################  2
    dbc.Row([dbc.Col([], width=4), dbc.Col([dcc.Loading(
        id="loading_detalle_linea"+linea,
        children='',
        type="cube",
        style={'margin-top': '250px', 'width': '400px'}
    )], width=4)]),


    ###############################################################################
dcc.Store(id='data-store-crear', storage_type='session'),
dcc.Store(id='data-store-rehacer', storage_type='session'),
])



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


###############################################################3CARD RESULTADO DETALLE 2
@app.callback(
   [Output('card_resultado_detalle_linea'+linea, 'children'),
    Output('card_resultado_grafico_linea' + linea, 'children'),
    Output('card_resultado_tabla_justif_linea'+linea, 'children'),
    Output('card_rendimiento_linea'+linea, 'children'),
    Output('card_observacion_linea'+linea, 'children'),
    Output('card_btn_siguiente_linea' + linea, 'children'),
    Output('linea_final_linea'+linea, 'children'),
    Output("loading_detalle_linea"+linea, "children")],
[Input('btn_ver_detalle_linea'+linea, 'n_clicks'),
Input('id_lin'+linea, 'value')],
 [State('input_linea'+linea, 'value')]
)
def revisar_informelinea(n_clicks, id_rep, linea):
    print('calbacIN',id_rep)

    try:
        if n_clicks > 0:

            linea_prueba='4'

            url = f"http://{host}:{port_reporte}/infoLinea/&{linea}/&{id_rep}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            LINEA = salida_json['linea']
            #######################################RESUMEN ULTIMA OP LINEA
            ult_op = salida_json['ultima_op']
            operador = ult_op['Operador']
            ayudante1 = ult_op['Ayudante 1']
            ayudante2 = ult_op['Ayudante 2']
            op = ult_op['OP']
            producto = ult_op['Producto']
            total_op = ult_op['Total Op[Kg]']
            bueno = ult_op['MB Bueno Producido']
            fuera_especificacion = ult_op["MB Fuera de Especificacion Producido"]
            kilogramos_fabricados = ult_op['Kilogramos Fabricados(Kg)']
            recirculado = ult_op['MB Recirculado']
            sacos = ult_op['Sacos envasados']
            total_extruido = ult_op['MB Total extruido']
            kg_bueno = ult_op['kg_bueno']
            bitacora = ult_op['bitacora']
            ##############################################  RESUMEN GRAFICO LINEA
            GRAFICO = salida_json['grafico']
            df_graf = pd.DataFrame(GRAFICO)

            df_graf['date'] = pd.to_datetime(df_graf['fecha'], unit='ms')
            print('DF', df_graf)
            df_hora = df_graf.loc[:, 'date']
            r40001 = df_graf.loc[:, 'r40001']
            r40003 = df_graf.loc[:, 'r40003']
            ############################################    TABLA_JUSTIFICACION
            JUSTIFICACION = salida_json['tablaJustificacion']
            #hora_ini = JUSTIFICACION['hora_inicio']
            print('TABLA', JUSTIFICACION)
            lista_justificacion = JUSTIFICACION[0]

            if lista_justificacion['hora_inicio'] == '--':

                datos = {
                    'op': ['--', '--'],
                    'hora_inicio': ['--', '--'],
                    'hora_fin': ['--', '--'],
                    'clasificación': ['--', '--'],
                    'causa': ['--', '--'],

                }
                df_justificacion= pd.DataFrame(datos)
            else:
                df_justificacion = pd.DataFrame(JUSTIFICACION)
                df_justificacion['hora_inicio'] = pd.to_datetime(df_justificacion['hora_inicio'], unit='ms')
                df_justificacion['hora_fin'] = pd.to_datetime(df_justificacion['hora_fin'], unit='ms')

                ##cambio formato
                df_justificacion['hora_inicio'] = df_justificacion['hora_inicio'].dt.strftime('%d-%m %H:%M')
                df_justificacion['hora_fin'] = df_justificacion['hora_fin'].dt.strftime('%d-%m %H:%M')
                df_justificacion = df_justificacion.drop(['operador', 'jefe_turno'], axis=1)
                print(df_justificacion)
            ##################################################  RENDIMIENTO LINEAS
            RENDIMIENTO = salida_json['rendimientosLineas']
            lista_rendimiento = RENDIMIENTO[0]
            maximo = lista_rendimiento['rendimientoMaximo']
            medio = lista_rendimiento['rendimientoMedio']
            real = lista_rendimiento['rendimientoReal']
            print('rend',real)
            ##################################################  OBSERVACION


            # time.sleep(3)
            return (dbc.Card([

                    dbc.CardBody([dbc.Row([dbc.Col([dcc.Input(value=f'Línea {LINEA}', type='text', id='nom_linea_det', disabled=True, style={"width": "100%", 'background-color': 'black','color':'white','text-align': 'center','font-size': '25px'})])]),
                        dbc.Row([dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([dbc.Row([dbc.Col([html.H6('Operador',style={'margin-top':'10px'})], width=5),
                                                    dbc.Col([dcc.Input(value=operador, type='text', id='operador_det', disabled=True, style={'margin-top':'4px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '20px'})], width=7)
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('Ayudante 1', style={'margin-top': '10px'})], width=5),
                                                   dbc.Col([dcc.Input(value=ayudante1, type='text', id='ayudante1_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})], width=7)
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('Ayudante 2', style={'margin-top': '10px'})], width=5),
                                                   dbc.Col([dcc.Input(value=ayudante2, type='text', id='ayudante2_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})], width=7)

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})

                                            ], width=3),
                        #################################################################################################
                                        dbc.Col([dbc.Card([
                                    dbc.CardBody([dbc.Row([dbc.Col([html.H6('OP:',style={'margin-top':'10px'})]),
                                                    dbc.Col([dcc.Input(value=op, type='text', id='op_det', disabled=True, style={'margin-top':'4px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '20px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('PRODUCTO:', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=producto, type='text', id='producto_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '12px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('TOTAL OP(Kg):', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=total_op, type='text', id='total_op_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})
                                        ], width=3),

                        ################################################################################################
                                        dbc.Col([dbc.Card([
                                    dbc.CardBody([dbc.Row([dbc.Col([html.H6('MB Bueno producido:',style={'margin-top':'10px'})], width=7),
                                                    dbc.Col([dcc.Input(value=bueno, type='text', id='producido_det', disabled=True, style={'margin-top':'4px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '20px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('MB Fuera de Especificación:', style={'margin-top': '10px'})], width=7),
                                                   dbc.Col([dcc.Input(value=fuera_especificacion, type='text', id='fuera_espec_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})], width=5)
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('MB Recirculado:', style={'margin-top': '10px'})], width=7),
                                                   dbc.Col([dcc.Input(value=recirculado, type='text', id='recirculado_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})
                                        ], width=3),
                        ################################################################################################
                                        dbc.Col([dbc.Card([
                                    dbc.CardBody([dbc.Row([dbc.Col([html.H6('Sacos Envasados:',style={'margin-top':'10px'})]),
                                                    dbc.Col([dcc.Input(value=sacos, type='text', id='sacos_det', disabled=True, style={'margin-top':'4px',"width": "100%",  'background-color': 'black','color':'white','text-align': 'center','font-size': '20px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('MB Total Extruido:', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=total_extruido, type='text', id='total_extr_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('Kg bueno:', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=kg_bueno, type='text', id='total_acum_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})
                                        ], width=3),

                        ################################################################################################

                                ]),
                        ########################################################################################


                    ])
                    ],color='#1c2833',style={ 'border': 'black 2px solid',  'text-align': 'center','margin-top': '10px','margin-left':'10px','margin-right':'10px'}),
                    #####################################################################################       GRAFICO
                    html.Div(

                        dbc.Card([
                            dbc.CardBody([dcc.Graph(figure={'data': [
                    {'x': df_hora, 'y': r40001, 'type': 'line', 'name': 'Set [Kg/h]', 'line': {'color': 'yellow'}},
                    {'x': df_hora, 'y': r40003, 'type': 'line', 'name': ' Real[Kg/h]', 'line': {'color': 'red'}},

                ],
                                'layout': {
                                    'yaxis': {'range': range, 'title': 'Flujo masa[KG/H]'},
                                    'xaxis': {'title': 'Tiempo(hrs)'},
                                    'title': f'Línea  {LINEA}',
                                    'height': 300,
                                    'width': 700,
                                    'margin': {'l': 40, 'r': 20, 't': 25, 'b': 40},
                                    'plot_bgcolor': colors['background'],
                                    'paper_bgcolor': colors['background'],
                                    'font': {
                                        'color': colors['text']
                                    },
                                }
                            }),

                            ])
                        ], color='#1c2833',
                            style={'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px',
                                   'margin-left': '10px'}),
                    ),

                    ############################################################3 ###  TABLA JUSTIFICACIONES
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([dash_table.DataTable(
                                data=df_justificacion.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df_justificacion.columns],

                                style_header={'backgroundColor': '  #229954 ',
                                              'color': 'white',
                                              'font-size': '20px',
                                              'font-weight': 'bolder',
                                              'font-family': 'sans-serif '},
                                style_cell={
                                    'backgroundColor': 'white',
                                    # 'padding-top': '5px', 'padding-bottom': '5px',
                                    'font-size': '15px',
                                    'color': 'black',

                                    'font-weight': 'bolder',
                                    'font-family': 'sans-serif '
                                    # 'minWidth': 90, 'maxWidth': 90, 'width': 90

                                },
                            )])
                        ])
                    ], color='#1c2833', style={'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px','margin-right':'10px'}),
                    ##################################################################################################
                    dbc.Card([
                        dbc.CardBody([dbc.Row([dbc.Col([dcc.Input(value='Rendimiento Máximo', type='text', id='id', disabled=True,
                                                              style={'margin-top': '5px', "width": "100%",
                                                                     'background-color': 'black', 'color': 'white',
                                                                     'text-align': 'center', 'font-size': '20px'})]),

                                               dbc.Col([dcc.Input(value='Rendimiento Medio', type='text', id='id',disabled=True,
                                                                  style={'margin-top': '5px', "width": "100%",
                                                                         'background-color': 'black', 'color': 'white',
                                                                         'text-align': 'center', 'font-size': '20px'})]),

                                               dbc.Col([dcc.Input(value='Rendimiento Real', type='text', id='id',disabled=True,
                                                                  style={'margin-top': '5px', "width": "100%",
                                                                         'background-color': 'black', 'color': 'white',
                                                                         'text-align': 'center', 'font-size': '20px'})]),

                                    ]),
                                      dbc.Row([dbc.Col([dcc.Input(value=maximo, type='text', id='id', disabled=True,
                                                              style={'margin-top': '5px', "width": "100%",
                                                                     'background-color': 'black', 'color': 'white',
                                                                     'text-align': 'center', 'font-size': '25px'})]),

                                               dbc.Col([dcc.Input(value=medio, type='text', id='id',disabled=True,
                                                                  style={'margin-top': '5px', "width": "100%",
                                                                         'background-color': 'black', 'color': 'white',
                                                                         'text-align': 'center', 'font-size': '25px'})]),

                                               dbc.Col([dcc.Input(value=real, type='text', id='id',disabled=True,
                                                                  style={'margin-top': '5px', "width": "100%",
                                                                         'background-color': 'black', 'color': 'white',
                                                                         'text-align': 'center', 'font-size': '25px'})]),

                                      ])
                        ])
                    ], color='#1c2833', style={'height': '160px','border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px','margin-left':'10px'}),

                    ##################################################################################################
                    dbc.Card([
                        dbc.CardBody([dbc.Row([dbc.Col([html.Div('Ingrese Observación')])]),
                            dbc.Row([dbc.Col([dcc.Textarea(placeholder='Ingrese Observación',id="text_area_lin"+linea,value=bitacora,
                                                         style={"width": "90%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white'},
                                                         cols=15, rows=3),])

                                    ])
                                ])
                    ], color='#1c2833',style={'height': '160px', 'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px','margin-right': '10px'}),
                    ###############################################################################################
                    dbc.Card([

                        dbc.CardBody([dbc.Row([dbc.Col([]),dbc.Col([dbc.Button('Continuar', color="info", id='btn_guardar_lin'+linea, n_clicks=0,
                                                 style={'margin-left': '1px', 'margin-top': '10px'})]),
                                               dbc.Col([]),
                                               ]),
                                      dbc.Row([dbc.Col([]),
                                          dbc.Col([html.Div(id='result' + linea, style={"margin-top": '20px'})]),

                                          dbc.Col(
                                              [html.Div(id='result_rehacer' + linea, style={"margin-top": '20px'})]),
                                      ]),
                    ])
                ], color='#1c2833', style={'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px', 'margin-left':'10px', 'margin-right':'10px'}),
                    ############################################################################################3
                    html.Hr(style={'border': '4px solid grey', "margin-top": '30px',"margin-bottom": '60px'}),
                    html.Div(id="loading"))

        else:
            return ('','','','','','','','')



    except:
        return (dcc.Input(value='Sin Conexión', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '50px', "width": "80%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'}),'','','','','','','')





##################################################CALLBACK CREAR INFORME Y PASAR A LINEA 2

@app.callback(
    [Output('result'+linea,'children'),
   Output('url_linea'+linea,'pathname')],
[Input('btn_guardar_lin'+linea, 'n_clicks')],
[State('text_area_lin'+linea, 'value'),
State('id_lin'+linea, 'value'),
]
)
def update_crear_in(n_clicks,  obs,id):
    print()

    if n_clicks > 0:
        if obs == '':
            return html.H4('Debe Ingresar Observación', style={ 'color': 'red'}),'/informe_lin'+linea
        else:
            payload = {
                'id_reporte': id,
                'Observacion': obs,
                'linea': linea,

            }
            r = requests.post('http://' + host + ':' + port_reporte + '/observaciones__lineas', json=payload)

            respuesta = json.loads(r.text)
            print('resp1',respuesta)

        return 'ok','/informe_lin'+linea_sig

    else:
        return '','/informe_lin'+linea


##################################################CALLBACK REHACER INFORME Y PASAR A LINEA 2
'''
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
    '''
