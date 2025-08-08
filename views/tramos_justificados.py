import pymysql
import random
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL
import json
from datetime import datetime as dat
import dash_bootstrap_components as dbc
import time
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
port = os.environ.get('PORT_REPORTE')
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

layout = html.Div([dcc.Location(id='url_reporte', refresh=True),
                    dcc.Location(id='url_ver_reporte', refresh=True),
                        #html.Meta(httpEquiv="refresh", content="300"),  # refresh pagina
                   html.Div(id='refrech'),

    dbc.Row([dbc.Col([], width=2), dbc.Col([dbc.Card([
        dbc.CardBody([
            dbc.Row([dbc.Col([html.Div('Seleccione Fecha')]),
                    dbc.Col([html.Div('Seleccione Línea')]),
                     dbc.Col([html.Div('Seleccione Turno')]),
                    dbc.Col([html.Div('')]),
                     ]),

            dbc.Row([
                dbc.Col([dcc.DatePickerSingle(
                    id='Date_reporte_ini',
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
                dbc.Col([dcc.Dropdown(id='menu_lineas_reporte',options=[{'label':'Línea 1', 'value':'1' },
                                                {'label':'Línea 2', 'value':'2' },
                                                {'label': 'Línea 3', 'value': '3'},
                                                {'label':'Línea 4', 'value':'4' },
                                                {'label':'Línea 5', 'value':'5' },
                                                {'label': 'Línea 6', 'value': '6'},
                                                {'label': 'Línea 7', 'value': '7'},
                                                {'label': 'Línea 8', 'value': '8'},
                                                {'label': 'Línea 9', 'value': '9'},
                                                {'label': 'Línea 10', 'value': '10'},

                                                 ], value='1', clearable=False, placeholder='Seleccione Linea',
                                                    style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),
                dbc.Col([dcc.Dropdown(id='menu_turno_reporte', options=[{'label': 'Mañana', 'value': 'Mañana'},
                                                                        {'label': 'Tarde', 'value': 'Tarde'},
                                                                        {'label': 'Noche', 'value': 'Noche'},
                                                                        {'label': 'Mañana-Sabado', 'value': 'Mañana-Sabado'},
                                                                        ], value='Mañana',
                                      clearable=False, placeholder='Seleccione Turno',
                                      style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),

                dbc.Col([dbc.Button('Buscar', color="info", id='btn_buscar_reporte', n_clicks=0,
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
    dbc.Row([dbc.Col([html.Div(id='card_result_reporte')])]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_rep1",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
dbc.Row([dbc.Col([html.Div(id='card_result_reporte2')] ,width=12)]),
##########################################################################################################3######
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_tabla",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
dbc.Row([dbc.Col([], width=3),dbc.Col([html.Div(id='resultado1')])]),
dbc.Row([dbc.Col([], width=2),dbc.Col([html.Div(id='mostrar_btn_refresh1')])]),

##############################################################################################################################

dbc.Row([dbc.Col([html.Div(id='res1')])]),
##########################################################################################################3######

])
#############################################callback MOSTRAR SELECCION DE INFORMES

@app.callback([
   Output('card_result_reporte', 'children'),
Output('card_result_reporte2', 'children'),
    Output("loading_rep1", "children")],
[Input('btn_buscar_reporte', 'n_clicks')],
[State('Date_reporte_ini', 'date'),
 State('menu_lineas_reporte', 'value'),
 State('menu_turno_reporte', 'value')]
)
def update_reporte(n_clicks, data, menu_linea,turno):
    print()
    if n_clicks > 0:
        data_str = data[0:10]
        print('data', data_str)
        if turno == 'Mañana':
            val_turno = 'A'
        elif turno == 'Tarde':
            val_turno = 'B'
        elif turno == 'Noche':
            val_turno = 'C'
        elif turno == 'Mañana-Sabado':
            val_turno = 'D'

        url = f"http://{host}:{port}/justificacion_turnos/&{menu_linea}/&{val_turno}/&{data_str}"
        print(url)
        response = requests.get(url)
        salida_json = response.json()
        print(salida_json)
        if salida_json['estado'] == 0:
            tramos = salida_json['tramos']
            op = salida_json['op']
            df_op = pd.DataFrame(op)
            #df_op['J'] = data['J'].str[:10]
            df_limit=df_op.iloc[:,0].str[:40]# limite de caracteres
            df_2 = pd.DataFrame(tramos)


            salida = []
            for index, row in df_2.iterrows():
                ID = row["id"]
                OP = row["op"]

                ##cambio  de fomato datetime(int) a
                row['hora_inicio'] = pd.to_datetime(row['hora_inicio'], unit='ms')
                row['hora_fin'] = pd.to_datetime(row['hora_fin'], unit='ms')

                print(f" las horas son {row['hora_inicio']}   {row['hora_fin']} y son del tipo {type(row['hora_fin'])}")

                row["hora_inicio"] = row["hora_inicio"].strftime('%d-%m %H:%M')
                row["hora_fin"] = row["hora_fin"].strftime('%d-%m %H:%M')

                hora_inicio = row["hora_inicio"]
                hora_fin = row["hora_fin"]


                clasificacion = row["clasificacion"]
                causa = row["causa"]
                salida = salida + [html.Tr([html.Td(ID),html.Td(OP), html.Td(hora_inicio), html.Td(hora_fin),html.Td(clasificacion),html.Td(causa),
                                            dbc.Button('Modificar', color="success", disabled=False,size="sm",
                                                       id={'type': 'ingresar', 'index': row["id"]},n_clicks=0)])]
            return (dbc.Container([
                dbc.Table(
                    # Header
                    [html.Tr([
                        html.Th('ID'),html.Th('OP'),
                        html.Th('INICIO'),
                        html.Th('FIN'),
                    html.Th('CLASIFICACION'),
                    html.Th('CAUSA'),])] + salida
                    # Body
                    # [html.Tr([ html.Td(i[2]),html.Td(i[3]),html.Td(i[4]),dbc.Button('Ingresar', color="success",disabled=True, id={'type': 'ingresar', 'index':  i[0]}, n_clicks=0),]) for i in info],
                    , style={'font-size': '25px'},bordered=True,responsive=True,  hover=True,striped=True,
                ),
            ]),html.Div(dbc.Card([
                dbc.CardBody([
                    dbc.Row([dbc.Col([html.H3('Modificar Informe')])]),
                dbc.Row([dbc.Col([html.Div('ID')], width=2),
                         dbc.Col([html.Div('OP')], width=4),
                             dbc.Col([html.Div('Clasificación')], width=2),
                         dbc.Col([html.Div('Causa')], width=2),
                            dbc.Col([html.Div('')], width=2),
                             ]),
                              dbc.Row([
                                       dbc.Col([dcc.Input(value='---', type='text', id='id_result', disabled=True,
                                                          style={'margin-top': '5px', "width": "100%",
                                                                 'background-color': 'black', 'color': 'white',
                                                                 'text-align': 'center', 'font-size': '25px'})], width=2),
                                  dbc.Col([dcc.Dropdown(id='menu_op', value='', clearable=False,options=[{"label": i, "value": i} for i in df_limit],
                                                        placeholder='Seleccione OP',
                                                        style={'width': '100%', 'color': 'black',
                                                               'margin-top': '10px'}),
                                           dcc.Interval(id='interval_menu_op', interval=10000,
                                                        n_intervals=0), ], width=4),
                                        dbc.Col([dcc.Dropdown(id='menu_clasificacion', value='', clearable=False, placeholder='Seleccione Clasificación',
                                                        style={'width': '100%', 'color': 'black', 'margin-top': '10px'}),
                                                 dcc.Interval(id='interval_menu_clasificacion', interval=10000, n_intervals=0),], width=2),
                                    dbc.Col([dcc.Dropdown(id='menu_causa', value='', clearable=False, placeholder='Seleccione Causa',
                                                        style={'width': '100%', 'color': 'black', 'margin-top': '10px'}),
                                             dcc.Interval(id='interval_menu_causa', interval=30000, n_intervals=0)], width=2),

                                        dbc.Col([dcc.ConfirmDialogProvider(children=html.Button('Modificar',style={"margin-top": '10px','font-size': '20px'} ),id='btn_guardar_modificacion',
                                                            message='Seguro Desea modificar?',
                                                        )], width=2)

                                       ]),
                                dbc.Row([html.Div(children=[
                                        dash_table.DataTable(
                                                id='table',
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
                                            }

                                        )],style={'display':'none'}),])


                              ])],color='#1c2833',
                style={"width": "110rem", 'border': 'black 2px solid', 'margin-left': '50px','text-align':'center',
                        'margin-top': '10px'}
            )

                ),html.Div(id="loading"))
        else:
            return dbc.Card([
                dbc.CardBody([dcc.Input(value='No Existe Información', type='text', id='xxxx', disabled=True,
                         style={'margin-top': '20px', 'margin-left': '50px', "width": "80%",
                                'background-color': 'black', 'color': 'white',
                                'text-align': 'center', 'font-size': '35px'})])],color='#1c2833',
                style={"width": "50rem", 'border': 'black 2px solid', 'margin-left': '410px','text-align':'center',
                        'margin-top': '10px'}
                        ),'',html.Div(id="loading")
    else:
        return '','',''


id=''
clasificaciones=''
df_causa=pd.DataFrame()
###esta funcion, se ejecuta con los botones ingresar
##este callback es el de la esquina sup derecha,se llena cuando se hace un click en "Ingresar"
@app.callback(   [Output('menu_clasificacion', 'options'),Output('id_result', 'value'),Output('table', 'data'),Output('table', 'columns'),Output("loading_tabla", "children")],[Input({'type': 'ingresar', 'index': ALL}, 'id'),Input({'type': 'ingresar', 'index': ALL}, 'n_clicks'),Input('interval_menu_causa', 'n_intervals')],[State({'type': 'ingresar', 'index': ALL}, 'n_clicks')]
)
def mostrar_CARD(value,clicks,inte,cli):
    print(f"llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")
    print('value',value)
    print('clic', clicks)
    print('clic2', cli)

    global id
    global clasificaciones
    global df_causa
    for i, j in enumerate(cli):

        if j == 1:
            print('jout',j)
            id = str(value[i]['index'])
            print('id----', id)
            url = f"http://{host}:{port}/info_tramo_justificacion/&{id}"
            print(url)
            response = requests.get(url)
            salida_json = response.json()

            clasificaciones=salida_json['clasificaciones']
            causas=salida_json['causas']
            df_causa=pd.DataFrame.from_dict([causas])









    return ([{'label': i, 'value': i} for i in clasificaciones], id,df_causa.to_dict('records'),[{"name": i, "id": i} for i in df_causa.columns],html.Div(id="loading"))


########################################callback menu causas depende de clasificaciones
@app.callback(Output('menu_causa', 'options'),
                [Input('menu_clasificacion', 'value'),
                 State('table', 'data')],
              )
def menu_causas(menu, data):

    if menu == '':
        return dash.no_update

    else:

        df1 = pd.DataFrame(data)
        print('df1',df1.loc[0,menu])
        lista1=df1.loc[0,menu].split(';')
        print('lista1',lista1)
        lista=['uno','dos']
        return [{'label': i, 'value': i} for i in lista1]

################CARD DE Resultados de busqueda,, se abre al apretar Observacion,,
@app.callback([Output('resultado1', 'children'),
    Output('res1', 'children'),
    Output('mostrar_btn_refresh1', 'children'),
    Output('refrech', 'children')],
    [Input('btn_guardar_modificacion', 'submit_n_clicks')],
   [State('id_result', 'value'),
    State('menu_op', 'value'),
    State('menu_clasificacion', 'value'),
    State('menu_causa', 'value')])
def ver_resultado(submit_n_clicks, id, menu_op,menu_cla, menu_causa):
    print("#######$$$$$$$$$$$$$$$###############################")


    if not submit_n_clicks:
        return ['','','','']
    if not id  or not menu_op or not  menu_cla or not menu_causa :

        return [html.Div(html.H3('Debe completar todos los campos', style={'color': 'red'})),'','','']
    else:
        ID=int(id)
        op=menu_op.split("/")#separa por slash
        print('seleccion',op[0])#toma el primer registro
        payload = {

            'id': ID,
            'op': op[0],
            'clasificacion': menu_cla,
            'causa': menu_causa,

        }
        direccion=f'http://{host}:{port}/info_tramo_justificacion/'
        r = requests.post(direccion , json=payload)
        response_dict = json.loads(r.text)
        print('status1', response_dict)
        #respuesta = json.loads(r.json())

        status = response_dict['estado']
        print('status',status)
        print('status', type(status))
        #se guardo el registro correctamente con un 1,, con 0 no
        #status='1'
        if status == 0:
            pass

        return ['',msj()
            , html.Button(
            children='OK',
            n_clicks=1,
            type='submit',
            id='btn_volver_reporte',
            style={'display': 'none'}
        ),html.Div(html.Meta(httpEquiv="refresh", content="5"))
        ]

#############################################################
@app.callback(Output('url_reporte', 'pathname'),
              [Input('btn_volver_reporte', 'n_clicks')],)
def registro_volver(n_clicks):
    if n_clicks > 0:
        time.sleep(5)
        return '/reporte'


########################################MENSAJE MODAL
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def msj():
    return html.Div(
    [
        dbc.Button("Open modal", id="open", n_clicks=1,style={'display':'none'}),
        dbc.Modal(
            [
                dbc.ModalHeader("TOPCOLOR"),
                dbc.ModalBody("Datos Modificados correctamente"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
    ]
)