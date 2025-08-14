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

x=11

layout = html.Div([dcc.Location(id='url_rehacer', refresh=True),
dcc.Location(id='url_rehacer2', refresh=True),
                    dcc.Location(id='url_siguiente', refresh=True),
                    dcc.Location(id='url_ver', refresh=True),
                        #html.Meta(httpEquiv="refresh", content="300"),  # refresh pagina
                        html.Div(id='refrech_rehacer'),

    dbc.Row([dbc.Col([], width=2), dbc.Col([dbc.Card([
        dbc.CardBody([
            dbc.Row([dbc.Col([html.Div('Seleccione Fecha')]),
                     dbc.Col([html.Div('Seleccione Turno')]),
                    dbc.Col([html.Div('')]),
                     ]),

            dbc.Row([
                dbc.Col([dcc.DatePickerSingle(
                    id='Date_informe_ini',
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

                dbc.Col([dcc.Dropdown(id='menu_turno_informe', options=[{'label': 'Mañana', 'value': 'Mañana'},
                                                                        {'label': 'Tarde', 'value': 'Tarde'},
                                                                        {'label': 'Noche', 'value': 'Noche'},
                                                                        {'label': 'Mañana-Sabado', 'value': 'Mañana-Sabado'},
                                                                        ], value='Mañana',
                                      clearable=False, placeholder='Seleccione Turno',
                                      style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),

                dbc.Col([dbc.Button('Buscar', color="info", id='btn_buscar_informe', n_clicks=0,
                                         style={'margin-left': '1px', 'margin-top': '10px'})]),

            ]),


        ])
    ], color="primary", inverse=True,
        style={"width": "50rem", "margin-top": '10px', 'margin-left': '100px', 'border': 'black 1px solid',
               'text-align': 'center'}
    ),
    ], width=5),

             ]),

#####################################################################################################################
    dbc.Row([dbc.Col([], width=1),
             dbc.Col([html.Hr(style={'border': '2px solid grey', "margin-top": '30px'})], width=9),
             dbc.Col([], width=1)]),
################################################################################################################################
    dbc.Row([dbc.Col([], width=1),dbc.Col([html.Div(id='card_result')])]),

##############################################################################################################################
################################################################################################################################
    dbc.Row([dbc.Col([html.Div(id='card_ver_informe')], width=12)]),
################################################################################################################################
    dbc.Row([dbc.Col([], width=1),dbc.Col([html.Div(id='card_result_modificar')])]),

##############################################################################################################################
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_1",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),

##############################################################################################################################
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_mod",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
##############################################################################################################################
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_ver",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
###########################################################################
    dbc.Row([dbc.Col([html.Div(id='card_crear',style={'margin-top': '20px'})], width=12)]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_2",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_3",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
################################################################
                   dbc.Row([
    dcc.Store(id='data-store-crear', storage_type='session'),
    dcc.Store(id='data-store-rehacer', storage_type='session'),
    dcc.Store(id='data-store-ver', storage_type='session'),
                            ]),

#####################################################################################
#################################################################################
dbc.Row([dbc.Col([], width=3),dbc.Col([html.Div(id='resultado_rehacer')])]),
dbc.Row([dbc.Col([], width=2),dbc.Col([html.Div(id='mostrar_btn_refresh_rehacer')])]),

##############################################################################################################################

dbc.Row([dbc.Col([html.Div(id='res1-rehacer')])]),




]),


########################################

#############################################callback MOSTRAR SELECCION DE INFORMES

#aca se revisa si existe un informe en fecha y turno seleccionado
@app.callback(
   [Output('card_result', 'children'),
    Output("loading_1", "children")],
[Input('btn_buscar_informe', 'n_clicks')],
[State('Date_informe_ini', 'date'),
 State('menu_turno_informe', 'value')]
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


            ListaJefesTurno=[{'label': 'Alvaro', 'value': 'Alvaro'},{'label': 'Juan', 'value': 'Juan'},{'label': 'Miguel', 'value': 'Miguel'}]



            if estado < 100:
                id_reprte=salida_json['id_reporte']
                print('iiiiddd',id_reprte)
                jefeTurno = salida_json['jefeTurno']
                jefe_turno = jefeTurno['jefeTurno']
                return html.Div(dbc.Card([
                dbc.CardBody([
                    dbc.Row([ dbc.Col([dcc.Input(value=id_reprte, type='text', id='id_reh', disabled=True,
                                                     style={'display':'none','margin-top': '5px', "width": "30%",
                                                            'background-color': 'black', 'color': 'white',
                                                            'text-align': 'center', 'font-size': '25px'})]),
                              dbc.Col([html.H3('Informe Seleccionado')]),
                              dbc.Col([])]),
                dbc.Row([dbc.Col([html.Div('Fecha')]),
                             dbc.Col([html.Div('Turno')]),
                            dbc.Col([html.Div('Jefe Turno')]),
                            dbc.Col([html.Button(
                                        children='Modificar Informe',
                                        n_clicks=0,
                                        type='submit',
                                        id='btn_modificar_informe',
                                        style={ 'font-size': '20px'}
                                    ),]),
                             ]),
                              dbc.Row([

                                       dbc.Col([dcc.Input(value=date, type='text', id='fecha_in_ver', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})]),
                                        dbc.Col([dcc.Input(value=turno, type='text', id='turno_in_ver', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})]),
                                        dbc.Col([dcc.Input(value=jefe_turno, type='text', id='jefe_turno_in_ver', disabled=True,
                                                     style={'margin-top': '5px', "width": "100%",
                                                            'background-color': 'black', 'color': 'white',
                                                            'text-align': 'center', 'font-size': '25px'})]),

                                        dbc.Col([dcc.ConfirmDialogProvider(children=html.Button('Ver Informe',style={"margin-top": '10px','font-size': '20px'} ),id='btn_ver_informe',
                                                            message='Seguro Desea Ver Informe?',
                                                        )])

                                       ]),


                              ])],color='#1c2833',
                style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px','text-align':'center',
                        'margin-top': '10px'}
            )

                ),html.Div(id="loading")
            else:

                ##aca no existe el reporte, se debe crear, primero traer los fefes de turno
                url = f"http://{host}:{port_reporte}/jefes_turno/"
                print(url)
                response = requests.get(url)
                salida_json = response.json()
                print(salida_json)
                jefesT = salida_json['jefesT']
                print(jefesT)
                print(type(jefesT))
                ListaJefesTurno=jefesT




                return html.Div(dbc.Card([
                    dbc.CardBody([
                        dbc.Row([dbc.Col([html.H3('Informe No Existe, Debe Crearlo')])]),
                        dbc.Row([dbc.Col([html.Div('Fecha')]),
                                 dbc.Col([html.Div('Turno')]),
                                 dbc.Col([html.Div('Jefe Turno')]),
                                 dbc.Col([html.Div('')]),
                                 ]),
                        dbc.Row([
                            dbc.Col([dcc.Input(value=date, type='text', id='fecha_in_crear', disabled=True,
                                               style={'margin-top': '5px', "width": "100%",
                                                      'background-color': 'black', 'color': 'white',
                                                      'text-align': 'center', 'font-size': '25px'})]),
                            dbc.Col([dcc.Input(value=turno, type='text', id='turno_in_crear', disabled=True,
                                               style={'margin-top': '5px', "width": "100%",
                                                      'background-color': 'black', 'color': 'white',
                                                      'text-align': 'center', 'font-size': '25px'})]),
                            dbc.Col([dcc.Dropdown(id='menu_jefe_turno', options=ListaJefesTurno,
                                                  value='',
                                                  clearable=False, placeholder='Seleccione Jefe Turno',
                                                  style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),

                            dbc.Col([dcc.ConfirmDialogProvider(children=html.Button('Crear Informe',style={"margin-top": '10px','font-size': '20px'} ),id='btn_crear_informe',
                                                            message='Seguro Desea Generar Informe?',
                                                        )])

                        ]),
                        dbc.Row([dbc.Col([html.Div(id='result_crear', style={"margin-top": '10px'})]), ])

                    ])],color='#1c2833',
                    style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px', 'text-align': 'center',
                           'margin-top': '10px'}
                )

                ),html.Div(id="loading")
        else:
            return '',''
    except:
        return func_except_card_informe()


################################################################## CARD VER INFORME
@app.callback(
   [Output('data-store-ver', 'data'),
Output('url_ver','pathname'),],
[Input('btn_ver_informe', 'submit_n_clicks')],
[State('fecha_in_ver', 'value'),
 State('turno_in_ver', 'value'),
 State('jefe_turno_in_ver', 'value')
 ]
)
def revisar_informe(submit_n_clicks, fecha, turno,jefe):
    print()
    if not submit_n_clicks:
        return '','/home'
    else:
        datos=[fecha,turno,jefe]
        return datos,'/page-2'


'''
#############################################callback MOSTRAR MODIFICAR INFORMES

@app.callback(
   [Output('card_result_modificar', 'children'),
    Output("loading_mod", "children")],
[Input('btn_modificar_informe', 'n_clicks')],
[State('Date_informe_ini', 'date'),
 State('menu_turno_informe', 'value')
 ]
)
def modificar_informe(n_clicks, fecha,turno):
    print()
    try:
        if n_clicks > 0:
            date_arreglo = fecha.split(" ")
            date = date_arreglo[0]

            url = f"http://{host}:{port_reporte}/jefes_turno/"
            print(url)
            response = requests.get(url)
            salida_json = response.json()
            print(salida_json)
            jefesT = salida_json['jefesT']
            print(jefesT)
            print(type(jefesT))
            ListaJefesTurno = jefesT
            return html.Div(dbc.Card([
                dbc.CardBody([
                    dbc.Row([dbc.Col([html.H3('Seleccionar Jefe de Turno')])]),
                dbc.Row([dbc.Col([html.Div('Fecha')]),
                             dbc.Col([html.Div('Turno')]),
                            dbc.Col([html.Div('Jefe Turno')]),
                         dbc.Col([html.Div('')]),

                             ]),
                              dbc.Row([
                                       dbc.Col([dcc.Input(value=date, type='text', id='fecha_mod', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})]),
                                        dbc.Col([dcc.Input(value=turno, type='text', id='turno_mod', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})]),
                                  dbc.Col([dcc.Dropdown(id='menu_jefe_mod', options=ListaJefesTurno,
                                                        value='',
                                                        clearable=False, placeholder='Seleccione Jefe Turno',
                                                        style={'width': '100%', 'color': 'black',
                                                               'margin-top': '10px'})]),
                                  dbc.Col([dcc.ConfirmDialogProvider(
                                      children=html.Button('Rehacer Informe', style={"margin-top": '10px','font-size': '20px'}),
                                      id='btn_rehacer_informe',
                                      message='Seguro Desea Rehacer Informe?',
                                      )]),

                                       ]),

                                    dbc.Row([dbc.Col([html.Div(id='result_rehacer',style={"margin-top": '10px'})]),])


                              ])],color='#1c2833',
                style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px','text-align':'center',
                        'margin-top': '10px'}
            )

                ),html.Div(id="loading")
        else:
            return '',''

    except:
        return func_except_card_informe()

'''


###################
################
###############
#############################################callback MOSTRAR MODIFICAR INFORMES
@app.callback(
   [Output('resultado_rehacer', 'children'),
    Output('res1-rehacer', 'children'),
    Output("loading_mod", "children")],
[Input('btn_modificar_informe', 'n_clicks')],
[State('Date_informe_ini', 'date'),
 State('menu_turno_informe', 'value')
 ]
)
def modificar_informe(n_clicks, fecha,turno):
    print()
    if n_clicks > 0:
        date_arreglo = fecha.split(" ")
        date = date_arreglo[0]
        time.sleep(5)
        return ['',msj_rehacer(date,turno),html.Div(id="loading")]

    else:
        return '','',''



@app.callback(

    Output('refrech_rehacer', 'children'),

[Input('mod', 'n_clicks')],
[State('Date_informe_ini', 'date'),
 State('menu_turno_informe', 'value'),
State('id_reh', 'value')
 ]
)
def modificar_informe(n_clicks, fecha,turno, id_reh):
    print()
    if n_clicks > 0:
        date_arreglo = fecha.split(" ")
        date = date_arreglo[0]
        #time.sleep(5)
        print('x'* 100)
        ids=int(id_reh)
        payload = {
            "id_reporte": str(ids)

        }
        dire=f'http://{host}:{port_reporte}/rehacer_informe'
        dire_get=f'http://{host}:{port_reporte}/rehacer_informe/&{ids}'
        print(f"vamos a reachecer el erporte id={ids} en la direccion {dire} ")
        #r = requests.post('http://' + host + ':' + port_reporte + '/rehacer_informe', json=payload)
        r = requests.get(dire_get)

        respuesta = json.loads(r.text)
        print(' REHACER', respuesta)
        return html.Div(html.Meta(httpEquiv="refresh", content="3"))


    else:
        return ''

    #############################################################


@app.callback(Output('url_rehacer2', 'pathname'),
              [Input('btn_volver_home', 'n_clicks')], )
def registro_volver(n_clicks):
    if n_clicks > 0:
        time.sleep(5)
        return '/home'


########################################MENSAJE MODAL
@app.callback(
    Output("modal_rehacer", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal_rehacer", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def msj_rehacer(fecha,turno):
    return html.Div(
        [
            dbc.Button("Open modal", id="open", n_clicks=1, style={'display': 'none'}),
            dbc.Modal(
                [
                    dbc.ModalHeader("Seguro Desea Rehacer Informe"),
                    dbc.ModalBody([dbc.Row([dbc.Col([html.H4('Fecha')]),
                                            dbc.Col([html.H4('Turno')])]),
                        dbc.Row([
                        dbc.InputGroup(
                            [dbc.Row([dbc.Col([
                                dbc.Input(id='input1', value=fecha),
                            ])]),
                                dbc.Row([dbc.Col([
                                    dbc.Input(id='input2', value=turno),
                                ])]),

                            ],
                            className="mb-3",
                        )
                    ])
                    ]),
                    dbc.ModalFooter(
                        dbc.ButtonGroup(
                            [dbc.Row([dbc.Col([

                                dbc.Button(
                                    "CERRAR", id="close", className="ml-auto", n_clicks=0
                                )])]),dbc.Row([dbc.Col([
                                dbc.Button(
                                    "REHACER", id="mod", className="ml-auto", n_clicks=0, style={'margin-left':'10px'}
                                )])])
                            ]
                        )
                    ),
                ],
                id="modal_rehacer",
                is_open=False,
            ),
        ]
    )








##################################################CALLBACK CREAR INFORME
@app.callback(
   [Output('result_crear','children'),
    Output('card_crear','children'),
Output('data-store-crear', 'data'),
Output("loading_2", "children"),],
[Input('btn_crear_informe', 'submit_n_clicks')],
[State('fecha_in_crear', 'value'),
 State('turno_in_crear', 'value'),
 State('menu_jefe_turno', 'value')
 ]
)
def crear_reporte(submit_n_clicks, fecha, turno, menu_jefe):
    print()
    try:
        if not submit_n_clicks:
            return '','','',''
        if menu_jefe == '':
            return html.H4('Debe Seleccionar Jefe Turno', style={'color': 'red'}),'','',''
        else:
            if turno == 'Mañana':
                val_turno = 'A'
            elif turno == 'Tarde':
                val_turno ='B'
            elif turno == 'Noche':
                val_turno ='C'
            elif turno == 'Mañana-Sabado':
                val_turno = 'D'
            payload = {
                'turno':val_turno,
                'dia': fecha,
                'jefe_turno': menu_jefe,
            }
            r=requests.post('http://'+host+':'+port_reporte+'/crear_reporte', json=payload)
            #print('request2',r.text)
            respuesta = json.loads(r.text)

            print("La respuesta que llega es del post:")
            print(respuesta)

            status = respuesta['estado']
            id_informe = respuesta['id_informe']
            datos1 =respuesta['datos']
            lin1 = datos1[0] #esto llega {"linea 1": {"tiempo extrusion": 10, "kilogramos fabricados": 12, "rendimiento real": 10 } }
            lin2 = datos1[1]  #{'linea 1': {'tiempo extrusion': 10, 'kilogramos fabricados': 12, 'rendimiento real': 10}}
            lin3 = datos1[2]
            lin4 = datos1[3]
            lin5 = datos1[4]
            lin6 = datos1[5]
            lin7 = datos1[6]
            lin8 = datos1[9]  ##aca cambio el orden, para mostrar la linea 8 real en este puesto
            lin9 = datos1[8]
            lin10 = datos1[7] ##linea aditivo

            df1 = pd.DataFrame(lin1)
            #esto es df1
            #                          linea 1
            #kilogramos fabricados       12
            #rendimiento real            10
            #tiempo extrusion            10

            df2 = pd.DataFrame(lin2)
            df3 = pd.DataFrame(lin3)
            df4 = pd.DataFrame(lin4)
            df5 = pd.DataFrame(lin5)
            df6 = pd.DataFrame(lin6)
            df7 = pd.DataFrame(lin7)
            df8 = pd.DataFrame(lin8)
            df9 = pd.DataFrame(lin9)
            df10 = pd.DataFrame(lin10)
            df_total =  pd.concat([df1,df2,df3,df4,df5, df6,df7,df8,df9,df10],axis = 1)
            df_ok = df_total.reset_index(names="Línea de Trabajo")

            return '',dbc.Card([
                    dbc.CardBody([ dbc.Row([dbc.Col([
                        html.Div([dash_table.DataTable(

                            columns=[{'id': c, 'name': c} for c in df_ok.columns],

                            data=df_ok.to_dict('records'),
                            style_header={'backgroundColor': '  #229954 ',
                                          'color': 'white',
                                          'font-size': '25px',
                                          'font-weight': 'bolder',
                                          'font-family': 'sans-serif '},
                            style_cell={
                                'backgroundColor': 'white',
                                # 'padding-top': '5px', 'padding-bottom': '5px',
                                'font-size': '20px',
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
                        dbc.Row([dbc.Col([dcc.ConfirmDialogProvider(children=html.Button('Seguir',style={"margin-top": '30px','font-size': '20px'} ),id='btn_seguir_informe',
                                                            message='Seguro Desea Seguir Informe?',
                                                        )])

                        ])

                    ])],color='#1c2833',
                    style={ 'border': 'black 2px solid',  'text-align': 'center',
                           'margin-top': '10px'}
                ),id_informe,html.Div(id="loading")
    except:
        return func_except_card_tabla()

##################################################CALLBACK REHACER INFORME
@app.callback([Output('result_rehacer','children'),
               Output('data-store-rehacer', 'data'),
Output("loading_3", "children"),
   Output('url_rehacer','pathname')],
[Input('btn_rehacer_informe', 'submit_n_clicks')],
[State('fecha_mod', 'value'),
 State('turno_mod', 'value'),
 State('menu_jefe_mod', 'value')
 ]
)
def update_rehacer_in(submit_n_clicks, fecha, turno, menu_jefe):
    print()
    if not submit_n_clicks:
        return '','','','/home'
    else:
        print('menujefe',menu_jefe)
        if menu_jefe == '':
            return html.H4('Debe Seleccionar Jefe Turno', style={'color': 'red'}),'','','/home'
        else:
            if turno == 'Mañana':
                val_turno = 'A'
            elif turno == 'Tarde':
                val_turno = 'B'
            elif turno == 'Noche':
                val_turno = 'C'
            elif turno == 'Mañana-Sabado':
                val_turno = 'D'
            payload = {
                'turno': val_turno,
                'dia': fecha,
                'jefe_turno': menu_jefe,
            }
            r = requests.post('http://' + host + ':' + port_reporte + '/crear_reporte', json=payload)
            # print('request2',r.text)
            respuesta = json.loads(r.text)
            id_informe = respuesta['id_informe']
            status = respuesta['estado']
            print('respuesta rehacer',respuesta)

            return 'ok',id_informe,html.Div(id="loading"),'/informe_lin1'

##################################################CALLBACK SIGUIENTE INFORME
@app.callback(
   Output('url_siguiente','pathname'),
[Input('btn_seguir_informe', 'submit_n_clicks')],
)
def update_sig_in(submit_n_clicks):
    print()
    if not submit_n_clicks:
        return '/home'
    else:

        return '/informe_lin1'


#####################################FUNCION EXCEPT CARD RESULTADO 1
def func_except_card_informe():
    print()
    return html.Div(dbc.Card([
        dbc.CardBody([
            dbc.Row([dbc.Col([html.H3('Sin Conexión')])]),
            dbc.Row([dbc.Col([html.Div('Fecha')]),
                     dbc.Col([html.Div('Turno')]),
                     dbc.Col([html.Div('Jefe Turno')]),

                     ]),
            dbc.Row([
                dbc.Col([dcc.Input(value='---', type='text', id='fecha_in_crear', disabled=True,
                                   style={'margin-top': '5px', "width": "100%",
                                          'background-color': 'black', 'color': 'white',
                                          'text-align': 'center', 'font-size': '25px'})]),
                dbc.Col([dcc.Input(value='---', type='text', id='turno_in_crear', disabled=True,
                                   style={'margin-top': '5px', "width": "100%",
                                          'background-color': 'black', 'color': 'white',
                                          'text-align': 'center', 'font-size': '25px'})]),
                dbc.Col([dcc.Dropdown(id='menu_jefe_turno', options=[{'label': 'Alvaro', 'value': 'Alvaro'},
                                                                     {'label': 'Juan', 'value': 'Juan'}],
                                      value='---',
                                      clearable=False, placeholder='Seleccione Jefe Turno',
                                      style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),



            ]),

        ])], color='#1c2833',
        style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px', 'text-align': 'center',
               'margin-top': '10px'}
    )

    ), html.Div(id="loading")

#####################################FUNCION EXCEPT CARD TABLA
def func_except_card_tabla():
    print()
    datos_except = {
        'Línea de trabajo': ['Tiempo Extrusion', 'Kilogramos fabricados', 'Rendimiento Real'],
        'Sin Conexión': ['---', '---', '---'],
        'Sin Conexión2': ['---', '---', '---'],
        'Sin Conexión3': ['---', '---', '---'],
      }
    df = pd.DataFrame(datos_except)
    return dbc.Card([
        dbc.CardBody([dbc.Row([dbc.Col([
            html.Div([dash_table.DataTable(

                columns=[{'id': c, 'name': c} for c in df.columns],

                data=df.to_dict('records'),
                style_header={'backgroundColor': '  #229954 ',
                              'color': 'white',
                              'font-size': '30px',
                              'font-weight': 'bolder',
                              'font-family': 'sans-serif '},
                style_cell={
                    'backgroundColor': 'white',
                    # 'padding-top': '5px', 'padding-bottom': '5px',
                    'font-size': '25px',
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


        ])], color='#1c2833',
        style={"width": "100rem", 'border': 'black 2px solid', 'margin-left': '50px', 'text-align': 'center',
               'margin-top': '10px'}
    ), html.Div(id="loading")

