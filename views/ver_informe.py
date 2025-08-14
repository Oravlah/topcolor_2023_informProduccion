import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State
import time
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
port_reporte = os.environ.get('PORT_REPORTE')

rango_ini = os.environ.get('RANGO_INI')
rango_fin = os.environ.get('RANGO_FIN')

range= [rango_ini, rango_fin]


hora=dat.now()

layout = html.Div([
    dbc.Row([dbc.Col([], width=2), dbc.Col([dbc.Card([
        dbc.CardBody([
            dbc.Row([dbc.Col([html.Div('Seleccione Fecha')]),
                     dbc.Col([html.Div('Seleccione Turno')]),
                     dbc.Col([html.Div('')]),
                     ]),

            dbc.Row([
                dbc.Col([dcc.DatePickerSingle(
                    id='Date_informe_ver',
                    min_date_allowed=dat(1900, 1, 1),
                    max_date_allowed=dat.today(),
                    initial_visible_month=dat.today(),
                    date=str(dat.today()),
                    clearable=True,
                    with_portal=True,
                    display_format='YYYY-MM-DD',
                    stay_open_on_select=False,
                    first_day_of_week=1,
                    style={'margin-left': '5px', 'width': '100%'}

                )
                ]),

                dbc.Col([dcc.Dropdown(id='menu_turno_informe_ver', options=[{'label': 'Mañana', 'value': 'Mañana'},
                                                                        {'label': 'Tarde', 'value': 'Tarde'},
                                                                        {'label': 'Noche', 'value': 'Noche'},
                                                                        {'label': 'Mañana-Sabado',
                                                                         'value': 'Mañana-Sabado'},
                                                                        ], value='Mañana',
                                      clearable=False, placeholder='Seleccione Turno',
                                      style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),

                dbc.Col([dbc.Button('Buscar', color="info", id='btn_buscar_informe_ver', n_clicks=0,
                                    style={'margin-left': '1px', 'margin-top': '10px'})]),

            ]),

        ])
    ], color="primary", inverse=True,
        style={"width": "50rem", "margin-top": '10px', 'margin-left': '100px', 'border': 'black 1px solid',
               'text-align': 'center'}
    ),
    ], width=5),

             ]),
################################################################################################################################
    dbc.Row([dbc.Col([], width=1), dbc.Col([html.Div(id='card_ver_informe')])]),

#############################################################################################TABLA INFORME 1
    dbc.Row([dbc.Col([html.Div(id='tabla_ver_informe', style={"margin-top": '10px'}),
                               dcc.Interval(id='interval_tabla_ver_informe', interval=10000, n_intervals=0),

                      ], width=12)]),

#############################################################################################CARD BTN Y DROP VER DETALLE 1
    dbc.Row([dbc.Col([html.Div(id='card_buscar_detalle', style={"margin-top": '10px'}),

                      ], width=12)]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=3), dbc.Col([dcc.Loading(
                       id="loading_ver",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=4)]),

#############################################################################################CARD BTN Y DROP VER DETALLE 1
    dbc.Row([dbc.Col([html.Div(id='card_resultado_detalle', style={"margin-top": '10px'}),

                      ], width=12)]),

#############################################################################################CARD GRAFICO Y TABLA JUSTIFICACION 1
    dbc.Row([dbc.Col([html.Div(id='card_resultado_grafico', style={"margin-top": '10px'}),

                      ], width=5),
            dbc.Col([html.Div(id='card_resultado_tabla_justif', style={"margin-top": '10px'}),

                      ], width=7)
             ]),


#############################################################################################CARD RENDIMIENTO Y OBSERVACION 1
    dbc.Row([dbc.Col([html.Div(id='card_rendimiento', style={"margin-top": '10px'}),

                      ], width=5),
            dbc.Col([html.Div(id='card_observacion', style={"margin-top": '10px'}),

                      ], width=7)
             ]),
#############################################################################################CARD BTN Y DROP VER DETALLE 1
    dbc.Row([dbc.Col([html.Div(id='linea_final', style={"margin-top": '30px'}),

                      ], width=12)]),
####################################################################################################3
                dbc.Row([dbc.Col([], width=3), dbc.Col([dcc.Loading(
                    id="loading_detalle1",
                    children='',
                    type="cube",
                    style={'margin-top': '250px', 'width': '400px'}
                )], width=4)]),



])

############################################################################### PAGINA VER INFORME 2
############################################################################### PAGINA VER INFORME 2
############################################################################### PAGINA VER INFORME 2
page_2_layout=html.Div([
dbc.Row([dbc.Col([], width=1), dbc.Col([dbc.Card([
                dbc.CardBody([
                    dbc.Row([dbc.Col([html.H3('Informe Seleccionado')])]),
                    dbc.Row([dbc.Col([html.Div('Nro. Reporte')], width=2),
                             dbc.Col([html.Div('Fecha')], width=3),
                             dbc.Col([html.Div('Turno')], width=3),
                             dbc.Col([html.Div('Jefe Turno')], width=4),


                             ]),
                              dbc.Row([
                                  dbc.Col([dcc.Input(value='---', type='text', id='id_ver2', disabled=True,
                                                     style={'margin-top': '5px', "width": "50%",
                                                            'background-color': 'black', 'color': 'white',
                                                            'text-align': 'center', 'font-size': '25px'})], width=2),
                                       dbc.Col([dcc.Input(value='---', type='text', id='fecha_ver2', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})], width=3),
                                        dbc.Col([dcc.Input(value='---', type='text', id='turno_ver2', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})], width=3),
                                        dbc.Col([dcc.Input(value='---', type='text', id='jefe_turno_ver2', disabled=True,
                                                     style={'margin-top': '5px', "width": "100%",
                                                            'background-color': 'black', 'color': 'white',
                                                            'text-align': 'center', 'font-size': '25px'})], width=4),



                                       ]),


                              ])],color='#1c2833',
                style={"width": "72rem", 'border': 'black 2px solid', 'margin-left': '100px','text-align':'center',
                        'margin-top': '10px'}
                )])]),
###################################################################################################################3
    dbc.Row([dbc.Col([html.Div(id='tabla_ver_informe2', style={"margin-top": '10px'}),
                      dcc.Interval(id='interval_tabla_ver_informe2', interval=10000, n_intervals=0),

                      ], width=12)]),

#############################################################################################CARD BTN Y DROP VER DETALLE 2
    dbc.Row([dbc.Col([html.Div(id='card_buscar_detalle2', style={"margin-top": '10px'}),

                      ], width=12)]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=3), dbc.Col([dcc.Loading(
                       id="loading_ver2",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=4)]),

#############################################################################################CARD RESULTADO VER DETALLE 2
    dbc.Row([dbc.Col([html.Div(id='card_resultado_detalle2', style={"margin-top": '10px'}),

                      ], width=12)]),

#############################################################################################CARD GRAFICO Y TABLA JUSTIFICACION 2
    dbc.Row([dbc.Col([html.Div(id='card_resultado_grafico2', style={"margin-top": '10px'}),

                      ], width=5),
            dbc.Col([html.Div(id='card_resultado_tabla_justif2', style={"margin-top": '10px'}),

                      ], width=7)
             ]),


#############################################################################################CARD RENDIMIENTO Y OBSERVACION 2
    dbc.Row([dbc.Col([html.Div(id='card_rendimiento2', style={"margin-top": '10px'}),

                      ], width=5),
            dbc.Col([html.Div(id='card_observacion2', style={"margin-top": '10px'}),

                      ], width=7)
             ]),
#############################################################################################CARD BTN Y DROP VER DETALLE 2
    dbc.Row([dbc.Col([html.Div(id='linea_final2', style={"margin-top": '30px'}),

                      ], width=12)]),
####################################################################################################  2
                dbc.Row([dbc.Col([], width=3), dbc.Col([dcc.Loading(
                    id="loading_detalle2",
                    children='',
                    type="cube",
                    style={'margin-top': '250px', 'width': '400px'}
                )], width=4)]),



dcc.Store(id='data-store-ver', storage_type='session'),
])
###############################################################################
###############################################################################
####################################################CALLBACK LAYOUT 2
@app.callback(
dash.dependencies.Output('id_ver2', 'value'),
    [dash.dependencies.Output('fecha_ver2', 'value'),
dash.dependencies.Output('turno_ver2', 'value'),
dash.dependencies.Output('jefe_turno_ver2', 'value'),
     dash.dependencies.Output('tabla_ver_informe2', 'children'),
     Output('card_buscar_detalle2', 'children')],
    [dash.dependencies.Input('data-store-ver', 'modified_timestamp')],
    [dash.dependencies.State('data-store-ver', 'data')]
)
def receive_data(timestamp, data):
    try:
        if timestamp is not None:
            date=data[0]
            turno=data[1]
            if turno == 'Mañana':
                val_turno = 'A'
            elif turno == 'Tarde':
                val_turno = 'B'
            elif turno == 'Noche':
                val_turno = 'C'
            elif turno == 'Mañana-Sabado':
                val_turno = 'D'

            url = f"http://{host}:{port_reporte}/estado_reporte_turno/&{val_turno}/&{date}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            print(salida_json)
            estado = salida_json['estado']
            msj = salida_json['mensaje']



            if estado < 100:
                jefeTurno = salida_json['jefeTurno']
                jefe_turno = jefeTurno['jefeTurno']
                id_reporte = salida_json['id_reporte']
                url2 = f"http://{host}:{port_reporte}/tabla_resumen_linea/&{id_reporte}"
                print(url2)
                response = requests.get(url2)
                salida_json2 = response.json()
                estado_resumen = salida_json2['estado']

                if estado_resumen < 100:
                    datos1 = salida_json2['datos']
                    dicc = datos1[0]

                    df2 = pd.DataFrame(datos1)
                    print('verc', df2)
                    return (id_reporte,data[0],data[1],data[2],html.Div(dbc.Card([
                            dbc.CardBody([ dbc.Row([dbc.Col([
                                html.Div([dash_table.DataTable(

                                    columns=[{'id': c, 'name': c} for c in df2.columns],

                                    data=df2.to_dict('records'),
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
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'font-weight': 'bolder',
                                        'font-family': 'sans-serif '
                                        # 'minWidth': 90, 'maxWidth': 90, 'width': 90

                                    },

                                ),
                                ])
                            ])

                            ]),


                            ])],color='#1c2833',
                            style={ 'border': 'black 2px solid',  'text-align': 'center',
                                   'margin-top': '10px'}
                        )),
                            #########################################################################
                             html.Div(dbc.Card([
                            dbc.CardBody([
                            dbc.Row([dbc.Col([html.H4('Ver Detalle por Línea')])]),
                    dbc.Row([dbc.Col([html.Div('')], width=4),
                             dbc.Col([html.Div('Seleccione Línea')], width=2),
                             dbc.Col([html.Div('')], width=2),
                             dbc.Col([html.Div('')], width=4),

                             ]),
                    dbc.Row([dbc.Col([html.Hr(style={'border': '4px solid grey', "margin-right": '30px'})], width=4),
                             dbc.Col([dcc.Dropdown(id='menu_lineas_ver_detalle2',
                                                   options=[{'label': 'Línea 1', 'value': '1'},
                                                            {'label': 'Línea 2', 'value': '2'},
                                                            {'label': 'Línea 3', 'value': '3'},
                                                            {'label': 'Línea 4', 'value': '4'},
                                                            {'label': 'Línea 5', 'value': '5'},
                                                            {'label': 'Línea 6', 'value': '6'},
                                                            {'label': 'Línea 7', 'value': '7'},
                                                            {'label': 'Línea 8', 'value': '8'},
                                                            {'label': 'Línea 9', 'value': '9'},
                                                            {'label': 'Línea 10', 'value': '10'},
                                                            {'label': 'Línea 11', 'value': '11'},

                                                            ], value='1', clearable=False,
                                                   placeholder='Seleccione Linea',
                                                   style={'width': '100%', 'color': 'black', 'margin-top': '10px'})],
                                     width=2),

                             dbc.Col([dbc.Button('Ver Detalle', color="info", id='btn_ver_detalle2', n_clicks=0,
                                                 style={'margin-left': '1px', 'margin-top': '10px'})], width=2),

                             dbc.Col([html.Hr(style={'border': '4px solid grey'})], width=4),
                             ]),

                    ])], color = '#1c2833',
                    style = {'border': 'black 2px solid', 'text-align': 'center', 'margin-left': '10px',
                             'margin-right': '10px',
                             'margin-top': '10px'}
                    )

                    )
                    )
                else:
                    msj_resumen = salida_json2['mensaje']
                    return '',data[0],data[1],data[2],dcc.Input(value=msj_resumen, type='text', id='xxxx', disabled=True,
                                     style={'margin-top': '20px', 'margin-left': '330px', "width": "50%",
                                            'background-color': 'black', 'color': 'white',
                                            'text-align': 'center', 'font-size': '35px'}),''

    except:
        return '--','--','--','--',dcc.Input(value='Sin Conexión', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '330px', "width": "50%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'}),''



###############################################################3CARD RESULTADO DETALLE 2
@app.callback(
   [Output('card_resultado_detalle2', 'children'),
    Output('card_resultado_tabla_justif2', 'children'),
    Output('card_rendimiento2', 'children'),
    Output('card_observacion2', 'children'),
    Output('linea_final2', 'children'),
    Output("loading_detalle2", "children")],
[Input('btn_ver_detalle2', 'n_clicks')],
[State('id_ver2', 'value'),
 State('menu_lineas_ver_detalle2', 'value')]
)
def revisar_informe2(n_clicks, id_rep, linea):
    print()
    try:
        if n_clicks > 0:
            url = f"http://{host}:{port_reporte}/infoLinea/&{linea}/&{id_rep}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            LINEA = salida_json['linea']
            #######################################RESUMEN ULTIMA OP LINEA
            ult_op=salida_json['ultima_op']
            operador=ult_op['Operador']
            ayudante1 = ult_op['Ayudante 1']
            ayudante2 = ult_op['Ayudante 2']
            op = ult_op['OP']
            producto = ult_op['Producto']
            total_op = ult_op['Total Op[Kg]']
            bueno = ult_op['MB Bueno Producido']
            kg_fabricado = ult_op['Kilogramos Fabricados(Kg)']
            recirculado = ult_op['MB Recirculado']
            sacos = ult_op['Sacos envasados']
            total_extruido = ult_op['MB Total extruido']
            kg_bueno = ult_op['kg_bueno']

            ############################################    TABLA_JUSTIFICACION
            ############################################    TABLA_JUSTIFICACION
            JUSTIFICACION = salida_json['tablaJustificacion']
            df_justificacion = pd.DataFrame(JUSTIFICACION)
            df_justificacion['hora_inicio'] = pd.to_datetime(df_justificacion['hora_inicio'], unit='ms')
            df_justificacion['hora_fin'] = pd.to_datetime(df_justificacion['hora_fin'], unit='ms')
            df_justificacion['hora_inicio'] = df_justificacion['hora_inicio'].dt.strftime('%d/%m/%Y %H:%M')
            df_justificacion['hora_fin'] = df_justificacion['hora_fin'].dt.strftime('%d/%m/%Y %H:%M')
            ##################################################  RENDIMIENTO LINEAS
            RENDIMIENTO = salida_json['rendimientosLineas']
            lista_rendimiento=RENDIMIENTO[0]
            maximo= lista_rendimiento['rendimientoMaximo']
            medio = lista_rendimiento['rendimientoMedio']
            real = lista_rendimiento['rendimientoReal']
            ##################################################  OBSERVACION
            OBSERVACION = salida_json['observacion']

            #time.sleep(3)
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
                                                   dbc.Col([dcc.Input(value=producto, type='text', id='producto_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])
                                                   ]),

                                          dbc.Row([dbc.Col([html.H6('TOTAL OP(Kg):', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=total_op, type='text', id='total_op_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})
                                        ], width=3),

                        ################################################################################################
                            dbc.Col([dbc.Card([
                                dbc.CardBody([dbc.Row(
                                    [dbc.Col([html.H6('MB Bueno producido:', style={'margin-top': '10px'})], width=7),
                                     dbc.Col([dcc.Input(value=bueno, type='text', id='producido_det', disabled=True,
                                                        style={'margin-top': '4px', "width": "100%",
                                                               'background-color': 'black', 'color': 'white',
                                                               'text-align': 'center', 'font-size': '20px'})])
                                     ]),

                                              dbc.Row([dbc.Col(
                                                  [html.H6('Kilogramos Fabricados(Kg):', style={'margin-top': '10px'})],
                                                  width=7),
                                                       dbc.Col([dcc.Input(value=kg_fabricado, type='text',
                                                                          id='fuera_espec_det', disabled=True,
                                                                          style={'margin-top': '4px', "width": "100%",
                                                                                 'background-color': 'black',
                                                                                 'color': 'white',
                                                                                 'text-align': 'center',
                                                                                 'font-size': '20px'})], width=5)
                                                       ]),

                                              dbc.Row([dbc.Col(
                                                  [html.H6('MB Recirculado:', style={'margin-top': '10px'})], width=7),
                                                       dbc.Col([dcc.Input(value=recirculado, type='text',
                                                                          id='recirculado_det', disabled=True,
                                                                          style={'margin-top': '4px', "width": "100%",
                                                                                 'background-color': 'black',
                                                                                 'color': 'white',
                                                                                 'text-align': 'center',
                                                                                 'font-size': '20px'})])

                                                       ])

                                              ])],
                                style={'border': 'black 2px solid', 'text-align': 'left', 'margin-top': '10px'})
                            ], width=3),
                            ################################################################################################
                            dbc.Col([dbc.Card([
                                dbc.CardBody(
                                    [dbc.Row([dbc.Col([html.H6('Sacos Envasados:', style={'margin-top': '10px'})]),
                                              dbc.Col([dcc.Input(value=sacos, type='text', id='sacos_det',
                                                                 disabled=True,
                                                                 style={'margin-top': '4px', "width": "100%",
                                                                        'background-color': 'black', 'color': 'white',
                                                                        'text-align': 'center', 'font-size': '20px'})])
                                              ]),

                                     dbc.Row([dbc.Col([html.H6('MB Total Extruido:', style={'margin-top': '10px'})]),
                                              dbc.Col([dcc.Input(value=total_extruido, type='text', id='total_extr_det',
                                                                 disabled=True,
                                                                 style={'margin-top': '4px', "width": "100%",
                                                                        'background-color': 'black', 'color': 'white',
                                                                        'text-align': 'center', 'font-size': '20px'})])
                                              ]),

                                     dbc.Row([dbc.Col([html.H6('Kilogramos Bueno(Kg):', style={'margin-top': '10px'})]),
                                              dbc.Col([dcc.Input(value=kg_bueno, type='text', id='total_acum_det',
                                                                 disabled=True,
                                                                 style={'margin-top': '4px', "width": "100%",
                                                                        'background-color': 'black', 'color': 'white',
                                                                        'text-align': 'center', 'font-size': '20px'})])

                                              ])

                                     ])],
                                style={'border': 'black 2px solid', 'text-align': 'left', 'margin-top': '10px'})
                            ], width=3),

                        ################################################################################################

                                ]),
                        ########################################################################################


                    ])
                    ],color='#1c2833',style={ 'border': 'black 2px solid',  'text-align': 'center','margin-top': '10px','margin-left':'10px','margin-right':'10px'}),

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
                        dbc.CardBody([dbc.Row([dbc.Col([dcc.Textarea(id="obs_inform",value=OBSERVACION,
                                                         style={"width": "90%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white'},
                                                         cols=15, rows=3),])

                                    ])
                                ])
                    ], color='#1c2833',style={'height': '160px', 'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px','margin-right': '10px'}),
                    ############################################################################################3
                    html.Hr(style={'border': '4px solid grey', "margin-top": '30px',"margin-bottom": '60px'}),
                    html.Div(id="loading"))

        else:
            return '','','','','',''

    except:
        return (dcc.Input(value='Sin Conexión', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '50px', "width": "80%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'}),'','','','','')

###############################################################3CARD RESULTADO DETALLE SOLO GRAFICO 2
@app.callback(
    Output('card_resultado_grafico2', 'children'),
    [Input('btn_ver_detalle2', 'n_clicks')],
    [State('id_ver2', 'value'),
    State('menu_lineas_ver_detalle2', 'value')]
)
def revisar_informe_graf2(n_clicks, id_rep, linea):
    print()
    if n_clicks > 0:
        if linea == '1' or linea == '2' :
            return  func_grafico1_2(linea, id_rep)
        else:
            return func_grafico_otros(linea,id_rep)

    else:
        return ''


################################################################################################################
###############################################CALLBACK LAYPOUT 1 ##############################################
#aca se revisa si existe un informe en fecha y turno seleccionado
@app.callback(
   [Output('card_ver_informe', 'children'),
Output('tabla_ver_informe', 'children'),
Output('card_buscar_detalle', 'children'),
    Output("loading_ver", "children")],
[Input('btn_buscar_informe_ver', 'n_clicks')],
[State('Date_informe_ver', 'date'),
 State('menu_turno_informe_ver', 'value')]
)
def revisar_informe(n_clicks, fecha, turno):
    print()
    try:
        if n_clicks > 0:
            date_arreglo = fecha.split(" ")
            date = date_arreglo[0]
            if turno == 'Mañana':
                val_turno = 'A'
            elif turno == 'Tarde':
                val_turno ='B'
            elif turno == 'Noche':
                val_turno ='C'
            elif turno == 'Mañana-Sabado':
                val_turno = 'D'

            url = f"http://{host}:{port_reporte}/estado_reporte_turno/&{val_turno}/&{date}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            print(salida_json)
            estado = salida_json['estado']
            msj = salida_json['mensaje']


            ListaJefesTurno=[{'label': 'Alvaro', 'value': 'Alvaro'},{'label': 'Juan', 'value': 'Juan'},{'label': 'Miguel', 'value': 'Miguel'}]



            if estado < 100:
                jefeTurno = salida_json['jefeTurno']
                jefe_turno = jefeTurno['jefeTurno']
                id_reporte = salida_json['id_reporte']
                url2 = f"http://{host}:{port_reporte}/tabla_resumen_linea/&{id_reporte}"
                print(url2)
                response = requests.get(url2)
                salida_json2 = response.json()
                estado_resumen = salida_json2['estado']


                if estado_resumen < 100:
                    datos1 = salida_json2['datos']



                    df2 = pd.DataFrame(datos1)
                    #df_total = pd.concat([df1, df2, df3], axis=0)
                    #dfi=df_total.set_index('linea')
                    #df_ok = df_total.reset_index()
                    #df_ok = df_total.reset_index(names="Línea de Trabajo")
                    print("los datos de la tabla resumen son")
                    print(df2)
                    #el orden de llegaada de las lineas es l1,l2.....ladt,lbl,l8, se debe ivertir
                    df2=df2.reindex([0,1,2,3,4,5,6,9,8,7])





                    return html.Div(dbc.Card([
                    dbc.CardBody([
                        dbc.Row([dbc.Col([html.H3('Informe Seleccionado')])]),
                    dbc.Row([dbc.Col([html.Div('Nro. Reporte')], width=2),
                            dbc.Col([html.Div('Fecha')], width=3),
                                 dbc.Col([html.Div('Turno')], width=3),
                                dbc.Col([html.Div('Jefe Turno')], width=4),


                                 ]),
                                  dbc.Row([
                                      dbc.Col([dcc.Input(value=id_reporte, type='text', id='id_ver1', disabled=True,
                                                         style={'margin-top': '5px', "width": "50%",
                                                                'background-color': 'black', 'color': 'white',
                                                                'text-align': 'center', 'font-size': '25px'})], width=2),
                                           dbc.Col([dcc.Input(value=date, type='text', id='fecha_in_ver', disabled=True,
                                                              style={'margin-top': '5px', "width": "100%",
                                                                     'background-color': 'black', 'color': 'white',
                                                                     'text-align': 'center', 'font-size': '25px'})], width=3),
                                            dbc.Col([dcc.Input(value=turno, type='text', id='turno_in_ver', disabled=True,
                                                              style={'margin-top': '5px', "width": "100%",
                                                                     'background-color': 'black', 'color': 'white',
                                                                     'text-align': 'center', 'font-size': '25px'})], width=3),
                                            dbc.Col([dcc.Input(value=jefe_turno, type='text', id='jefe_turno_in_ver', disabled=True,
                                                         style={'margin-top': '5px', "width": "100%",
                                                                'background-color': 'black', 'color': 'white',
                                                                'text-align': 'center', 'font-size': '25px'})], width=4),



                                           ]),


                                  ])],color='#1c2833',
                    style={"width": "72rem", 'border': 'black 2px solid', 'margin-left': '100px','text-align':'center',
                            'margin-top': '10px'}
                    )

                    ),html.Div(dbc.Card([
                        dbc.CardBody([ dbc.Row([dbc.Col([
                            html.Div([dash_table.DataTable(

                                columns=[{'id': c, 'name': c} for c in df2.columns],

                                data=df2.to_dict('records'),
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
                                    'overflow': 'hidden',
                                    'textOverflow': 'ellipsis',
                                    'font-weight': 'bolder',
                                    'font-family': 'sans-serif '
                                    # 'minWidth': 90, 'maxWidth': 90, 'width': 90

                                },

                            ),
                            ])
                        ])

                        ]),


                        ])],color='#1c2833',
                        style={ 'border': 'black 2px solid',  'text-align': 'center','margin-left':'10px','margin-right':'10px',
                               'margin-top': '10px'}
                    )),html.Div(dbc.Card([
                    dbc.CardBody([
                        dbc.Row([dbc.Col([html.H4('Ver Detalle por Línea')])]),
                    dbc.Row([dbc.Col([html.Div('')], width=4),
                            dbc.Col([html.Div('Seleccione Línea')], width=2),
                            dbc.Col([html.Div('')], width=2),
                             dbc.Col([html.Div('')], width=4),

                                 ]),
                                  dbc.Row([dbc.Col([html.Hr(style={'border': '4px solid grey',"margin-right": '30px'})], width=4),
                                           dbc.Col([dcc.Dropdown(id='menu_lineas_ver_detalle1',options=[{'label':'Línea 1', 'value':'1' },
                                                {'label':'Línea 2', 'value':'2' },
                                                {'label': 'Línea 3', 'value': '3'},
                                                {'label':'Línea 4', 'value':'4' },
                                                {'label':'Línea 5', 'value':'5' },
                                                {'label': 'Línea 6', 'value': '6'},
                                                {'label': 'Línea 7', 'value': '7'},
                                                {'label': 'Línea 8', 'value': '10'},
                                                {'label': 'Línea Bl', 'value': '9'},
                                                {'label': 'Línea Adt', 'value': '8'},

                                                 ], value='1', clearable=False, placeholder='Seleccione Linea',
                                                    style={'width': '100%', 'color': 'black', 'margin-top': '10px'})], width=2),

                                      dbc.Col([dbc.Button('Ver Detalle', color="info", id='btn_ver_detalle1', n_clicks=0,
                                                      style={'margin-left': '1px', 'margin-top': '10px'})], width=2),

                                           dbc.Col([html.Hr(style={'border': '4px solid grey'})], width=4),
                                           ]),


                                  ])],color='#1c2833',
                    style={ 'border': 'black 2px solid','text-align':'center','margin-left':'10px','margin-right':'10px',
                            'margin-top': '10px'}
                    )

                    ),html.Div(id="loading")

                else:
                    msj_resumen = salida_json2['mensaje']
                    return dcc.Input(value=msj_resumen, type='text', id='xxxx', disabled=True,
                                                          style={'margin-top': '20px',  'margin-left': '230px',"width": "50%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '35px'}),'','',html.Div(id="loading")


            else:
                return dcc.Input(value=msj, type='text', id='xxxx', disabled=True,
                                                          style={'margin-top': '20px',  'margin-left': '230px',"width": "50%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '35px'}),'','',html.Div(id="loading")
        else:
            return '','','',''
    except:
        return dcc.Input(value='Sin Conexión', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '230px', "width": "50%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'}),'', '', html.Div(id="loading")

############################################################3


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
###############################################################3CARD RESULTADO DETALLE
@app.callback(
   [Output('card_resultado_detalle', 'children'),
    Output('card_resultado_tabla_justif', 'children'),
    Output('card_rendimiento', 'children'),
    Output('card_observacion', 'children'),
    Output('linea_final', 'children'),
    Output("loading_detalle1", "children")],
[Input('btn_ver_detalle1', 'n_clicks')],
[State('id_ver1', 'value'),
 State('menu_lineas_ver_detalle1', 'value')]
)
def revisar_informe(n_clicks, id_rep, linea):
    print()
    try:
        if n_clicks > 0:
            url = f"http://{host}:{port_reporte}/infoLinea/&{linea}/&{id_rep}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            print("$"*100)
            print(salida_json)
            LINEA = salida_json['linea']
            #######################################RESUMEN ULTIMA OP LINEA
            ult_op=salida_json['ultima_op']
            operador=ult_op['Operador']
            ayudante1 = ult_op['Ayudante 1']
            ayudante2 = ult_op['Ayudante 2']
            op = ult_op['OP']
            producto = ult_op['Producto']
            total_op = ult_op['Total Op[Kg]']
            bueno = ult_op['MB Bueno Producido']
            fuera_especificacion = ult_op["MB Fuera de Especificacion Producido"]
            kg_fabricado = ult_op['Kilogramos Fabricados(Kg)']
            recirculado = ult_op['MB Recirculado']
            sacos = ult_op['Sacos envasados']
            total_extruido = ult_op['MB Total extruido']
            kg_bueno = ult_op['kg_bueno']



            ############################################    TABLA_JUSTIFICACION
            JUSTIFICACION = salida_json['tablaJustificacion'] #[{'op': '--', 'hora_inicio': '--', 'hora_fin': '--', 'clasificacion': '--', 'causa': '--'}] cuando no reciben datos
            print(len(JUSTIFICACION))
            print((JUSTIFICACION))
            if(len(JUSTIFICACION)<=1):
                df_justificacion = pd.DataFrame(JUSTIFICACION)
            else:
                df_justificacion = pd.DataFrame(JUSTIFICACION)
                df_justificacion['hora_inicio'] = pd.to_datetime(df_justificacion['hora_inicio'], unit='ms')
                df_justificacion['hora_fin'] = pd.to_datetime(df_justificacion['hora_fin'], unit='ms')
                df_justificacion['hora_inicio'] = df_justificacion['hora_inicio'].dt.strftime('%d/%m/%Y %H:%M')
                df_justificacion['hora_fin'] = df_justificacion['hora_fin'].dt.strftime('%d/%m/%Y %H:%M')


            ##################################################  RENDIMIENTO LINEAS
            RENDIMIENTO = salida_json['rendimientosLineas']
            lista_rendimiento=RENDIMIENTO[0]
            maximo= lista_rendimiento['rendimientoMaximo']
            medio = lista_rendimiento['rendimientoMedio']
            real = lista_rendimiento['rendimientoReal']
            ##################################################  OBSERVACION
            OBSERVACION = salida_json['observacion']
            print("932")
            #time.sleep(3)
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
                                                   dbc.Col([dcc.Input(value=producto, type='text', id='producto_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])
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

                                          dbc.Row([dbc.Col([html.H6('Kilogramos Fabricados(Kg):', style={'margin-top': '10px'})], width=7),
                                                   dbc.Col([dcc.Input(value=kg_fabricado, type='text', id='fuera_espec_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})], width=5)
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

                                          dbc.Row([dbc.Col([html.H6('Kilogramos Bueno(Kg):', style={'margin-top': '10px'})]),
                                                   dbc.Col([dcc.Input(value=kg_bueno, type='text', id='total_acum_det', disabled=True,style={'margin-top': '4px', "width": "100%",'background-color': 'black', 'color': 'white', 'text-align': 'center', 'font-size': '20px'})])

                                                ])


                                            ])],style={'border': 'black 2px solid','text-align':'left','margin-top':'10px'})
                                        ], width=3),

                        ################################################################################################

                                ]),
                        ########################################################################################


                    ])
                    ],color='#1c2833',style={ 'border': 'black 2px solid',  'text-align': 'center','margin-top': '10px','margin-left':'10px','margin-right':'10px'}),

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
                        dbc.CardBody([dbc.Row([dbc.Col([dcc.Textarea(id="obs_informe",value=OBSERVACION,
                                                         style={"width": "90%", 'margin-top': '10px','margin-bottom':'5px','background-color': 'black', 'color': 'white'},
                                                         cols=15, rows=3),])

                                    ])
                                ])
                    ], color='#1c2833',style={'height': '160px', 'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px','margin-right': '10px'}),
                    ############################################################################################3
                    html.Hr(style={'border': '4px solid grey', "margin-top": '30px',"margin-bottom": '60px'}),
                    html.Div(id="loading"))

        else:
            return '','','','','',''

    except:
        return (dcc.Input(value='Sin Conexión 1', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '50px', "width": "80%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'}),'','','','','')


###############################################################3CARD RESULTADO DETALLE SOLO GRAFICO
@app.callback(
    Output('card_resultado_grafico', 'children'),
    [Input('btn_ver_detalle1', 'n_clicks')],
    [State('id_ver1', 'value'),
    State('menu_lineas_ver_detalle1', 'value')]
)
def revisar_informe_graf(n_clicks, id_rep, linea):
    print()
    if n_clicks > 0:
        if linea == '1' or linea == '2' or linea == '9' or linea == '19':
            return  func_grafico1_2(linea, id_rep)
        else:
            return func_grafico_otros(linea,id_rep)

    else:
        return ''



##############################################  FUNCION GRAFICO LINEAS 1 2
def func_grafico1_2(linea,id):
    print()
    try:
        url = f"http://{host}:{port_reporte}/infoLinea/&{linea}/&{id}"
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        LINEA = salida_json['linea']
        ##############################################  RESUMEN GRAFICO LINEA
        GRAFICO = salida_json['grafico']
        df_graf = pd.DataFrame(GRAFICO)

        df_graf['date'] = pd.to_datetime(df_graf['fecha'], unit='ms')
        print('DF', df_graf)

        df_hora = df_graf.loc[:, 'date']
        ch1 = df_graf.loc[:, 'canal1']
        ch2 = df_graf.loc[:, 'canal2']
        ch3 = df_graf.loc[:, 'prod']
        range_12=[0,4]
        return html.Div(
            #####################################################################################       GRAFICO
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure={'data': [
                    {'x': df_hora, 'y': ch1, 'type': 'line', 'name': 'motor extrusora ','line': {'color': 'yellow'}},
                    {'x': df_hora, 'y': ch2, 'type': 'line', 'name': 'dosificador ', 'line': {'color': 'green'}},
                    {'x': df_hora, 'y': ch3, 'type': 'line', 'name': 'prod ', 'line': {'color': 'red'}},

                ],
                    'layout': {
                        'yaxis': {'range': range_12, 'title': 'Flujo masa[KG/H]'},
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
            ], color='#1c2833', style={'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px',
                                       'margin-left': '10px'}),
        )
    except:
        return html.Div([html.H2('Sin Conexión 2')])



##############################################  FUNCION GRAFICO LINEAS OTROS
def func_grafico_otros(linea,id):
    print('func',type(id))
    try:
        if linea ==  '8':
            range =[0,1500]

        elif linea == '7' or linea == '9' or linea == '10':
            range=[0,400]

        else:
            range=[0,250]
        url = f"http://{host}:{port_reporte}/infoLinea/&{linea}/&{id}"
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        LINEA = salida_json['linea']
        ##############################################  RESUMEN GRAFICO LINEA
        GRAFICO = salida_json['grafico']
        df_graf = pd.DataFrame(GRAFICO)

        df_graf['date'] = pd.to_datetime(df_graf['fecha'], unit='ms')
        #print('DF', df_graf)
        df_hora = df_graf.loc[:, 'date']
        r40001 = df_graf.loc[:, 'r40001']
        r40003 = df_graf.loc[:, 'r40003']
        return html.Div(
            #####################################################################################       GRAFICO
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
            ], color='#1c2833', style={'border': 'black 2px solid', 'text-align': 'center', 'margin-top': '10px',
                                       'margin-left': '10px'}),
        )
    except:
        return html.Div([dcc.Input(value='Sin Conexión 3', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '50px', "width": "80%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'})])