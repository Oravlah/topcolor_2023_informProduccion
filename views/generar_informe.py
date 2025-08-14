
from datetime import datetime as dat

import json
from datetime import datetime, timedelta
from server import app

import os
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4,letter, inch
#from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph ,Spacer,PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
import requests
#from rotatedtext import verticalText
#from verticaltext import textoVertical
from dash import dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc

from dash import Dash, dcc, html, Input, Output, callback
from dateutil.tz import tzutc, tzlocal

import datetime
import base64
from datetime import datetime
from urllib.request import urlopen

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
#esto es IMPORTANTE para problema de generacion de matplotli usandoi -"Tcl_AsyncDelete: async handler deleted by the wrong thread"
matplotlib.use('agg')  #
#warnings.simplefilter("ignore", UserWarning)

import yagmail



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
zona_horaria= os.environ.get('zona')

##################################################


host2 = os.environ.get('IP_API2')
host3 = os.environ.get('IP_API3')


###### Esto te obtiene la ruta actual donde esta el archivo nuevo_diseño.py de forma variable

directorio_actual = os.getcwd()

#  del archivo PDF
_archivo = "informe_topcolor.pdf"

# Unir el directorio actual con el  del archivo
ruta_archivo = os.path.join(directorio_actual, _archivo)

pdf_path = ruta_archivo


hora=dat.now()

global fecha_informe
fecha_informe=""

layout = html.Div([
                dbc.Row([dbc.Col([], width=2), dbc.Col([dbc.Card([
        dbc.CardBody([
            dbc.Row([dbc.Col([html.Div('Seleccione Fecha')]),
                     dbc.Col([html.Div('Seleccione Turno')]),
                    dbc.Col([html.Div('')]),
html.Div(id='output-div')
                     ]),

            dbc.Row([
                dbc.Col([dcc.DatePickerSingle(
                    id='Date_generar_ini',
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

                dbc.Col([dcc.Dropdown(id='menu_turno_generar', options=[{'label': 'Mañana', 'value': 'A'},
                                                                        {'label': 'Tarde', 'value': 'B'},
                                                                        {'label': 'Noche', 'value': 'C'},
                                                                        {'label': 'Mañana-Sabado', 'value': 'D'},
                                                                        ], value='Mañana',
                                      clearable=False, placeholder='Seleccione Turno',
                                      style={'width': '100%', 'color': 'black', 'margin-top': '10px'})]),

                dbc.Col([dbc.Button('Buscar', color="info", id='btn_buscar_generar', n_clicks=0,
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

    dbc.Row([dbc.Col([], width=1),dbc.Col([html.Div(id='card_result_generar')])]),

##############################################################################################################################
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_1_generar",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),
###########################################################################
            dbc.Row([dbc.Col([], width=1),dbc.Col([html.Div(id='card_result_descargar')])]),

##############################################################################################################################
                   dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_D",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),

dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_2_generar",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),

dbc.Row([dbc.Col([], width=2), dbc.Col([dcc.Loading(
                       id="loading_3_generar",
                       children='',
                       type="cube",
                       style={'margin-top': '250px', 'width': '400px'}
                   )], width=6)]),

dbc.Row([dbc.Col([html.Div(id='res_in')])]),
dbc.Row([dbc.Col([dcc.Download(id="download-text")])]),
])


#############################################callback MOSTRAR SELECCION DE INFORMES

@app.callback(
   [Output('card_result_generar', 'children'),
    Output("loading_1_generar", "children")],
[Input('btn_buscar_generar', 'n_clicks')],
[State('Date_generar_ini', 'date'),
 State('menu_turno_generar', 'value')]
)
def update_informe(n_clicks, fecha, turno):

    # ocurre que si uno no selecciona fecha, por defecto tira la fecha con hora- min-seg(2023-07-13 18:08:57.321036), si se selecciona solo la fecha(2023-07-13 )
    #para esto se hace split y se  toma solo lo primero
    date_arreglo = fecha.split(" ")
    date = date_arreglo[0]
    fecha_informe=date

    # hora de peticion, se va a utilizar para el argumento de los nombres de los graficos
    ahora = datetime.now()
    ahora_str = ahora.strftime("%Y%m%d%H%M%S")

    if n_clicks > 0 and len(turno)<2:
##solicito si existe el informe
        url7 = f'http://{host}:{port_reporte}/estado_reporte_turno/&{str(turno)}/&{str(date)}'
        datos7 = urlopen(url7)
        print('URL', url7)
        usuario7 = json.loads(datos7.read())

        #estado del informe
        estado=int(usuario7['estado'])
        if estado < 100:

            ##Nombre turno


            jt_1=usuario7['jefeTurno'] #{'jefeTurno': 'JOSÉ RIVERA                                  '}
            turno_api_1 = usuario7['turno']
            id_reporte=usuario7['id_reporte'] #'id_reporte': 15,
            fecha_creacion_1 = usuario7['fecha_creacion']  #   {'fechaInsert': '2023-07-12T09:12:48'}

            ##viene un dict dentro de otro
            turno_api=turno_api_1['turno']
            jt=jt_1['jefeTurno']
            fecha_creacion = fecha_creacion_1['fechaInsert']



            return html.Div(dbc.Card([
            dbc.CardBody([
            dbc.Row([dbc.Col([html.H3('Informe Seleccionado')])]),
            dbc.Row([dbc.Col([html.Div('Fecha')]),
                     dbc.Col([html.Div('Turno')]),
                     dbc.Col([html.Div('Operador Turno')]),

                     ]),
            dbc.Row([
                dbc.Col([dcc.Input(value=date, type='text', id='fecha_descargar', disabled=True,
                                   style={'margin-top': '5px', "width": "100%",
                                          'background-color': 'black', 'color': 'white',
                                          'text-align': 'center', 'font-size': '25px'})]),
                dbc.Col([dcc.Input(value=turno_api, type='text', id='turno_descargar', disabled=True,
                                   style={'margin-top': '5px', "width": "100%",
                                          'background-color': 'black', 'color': 'white',
                                          'text-align': 'center', 'font-size': '25px'})]),
                dbc.Col([dcc.Input(value=jt, type='text', id='oerador_descargar', disabled=True,
                                   style={'margin-top': '5px', "width": "100%",
                                          'background-color': 'black', 'color': 'white',
                                          'text-align': 'center', 'font-size': '25px'})]),



            ]),
                dbc.Row([dbc.Col([]),dbc.Col([dbc.Button("Descargar informe", id='download-link',disabled = False,
        download='informe_topcolor.pdf',
        href='',
        target='_blank', color="info", className="me-1",style={"margin-top": '20px'})]),
                    dbc.Col([dbc.Button("Enviar informe", id='enviar-link',disabled = False,
        download='informe_topcolor.pdf',
        href='',
        target='_blank', color="info", className="me-1",style={"margin-top": '20px'})]),
                         dbc.Col([]),
                ]),

        ])], color='#1c2833',
        style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px', 'text-align': 'center',
               'margin-top': '10px'}
        )

        ), html.Div(id="loading")

        else:
            return html.Div(dbc.Card([
            dbc.CardBody([
            dbc.Row([dbc.Col([html.H3('No Existe Informe para la Fecha Seleccionada ')])]),
            dbc.Row([dbc.Col([html.Div('')]),
                     dbc.Col([html.Div('')]),
                     dbc.Col([html.Div('')]),
                     dbc.Col([html.Div('')]),
                     ]),


        ])], color='#1c2833',
        style={"width": "70rem", 'border': 'black 2px solid', 'margin-left': '100px', 'text-align': 'center',
               'margin-top': '10px'}
        )

        ), html.Div(id="loading")
    else:
        return '', ''


########################################  CALBAK PAR DESHABILITAR BOTONES

@app.callback([Output("download-link", "disabled"),
                Output('enviar-link', "disabled")],
              [Input('download-link', 'n_clicks'),
               Input('enviar-link', 'n_clicks')]
              )
def bloqueo_descargar(n_clicks,n_clicks2):
    #print("boton doownload")
    if n_clicks is not None or n_clicks2 is not None:

        return  True, True
    else:
        return False,False

#############################################callback DESCARGAR
####BOTON "Descargar informe"
#@app.callback([Output("download-text", "data"), Output("loading_D", "children"),Output('res_in', 'children')],[Input('download-link', 'n_clicks')],[State('fecha_descargar', 'value'),State('turno_descargar', 'value')],prevent_initial_call=True)
#@app.callback([Input('download-link', 'n_clicks')],[State('fecha_descargar', 'value'),State('turno_descargar', 'value')],prevent_initial_call=True)
@app.callback([Output("download-text", "data"),Output("loading_3_generar", "children")],[Input('download-link', 'n_clicks')],[State('fecha_descargar', 'value'),State('turno_descargar', 'value')],prevent_initial_call=True)

def update_descargar(n_clicks, fecha, turno):
    print(f"boton doownload con los datos {fecha}   y  {turno}")



    if n_clicks is not None:

        ruta_informe=crear_informe(fecha,turno)
        return  dcc.send_file(ruta_informe), html.Div(id="loading")

    else:
        return no_update,''



@app.callback(  Output('output-div', 'children'),Output("loading_2_generar", "children"),[Input('enviar-link', 'n_clicks')],[State('fecha_descargar', 'value'),State('turno_descargar', 'value')],prevent_initial_call=True)
def enviar_correo(n_clicks, fecha, turno):
    #print("boton doownload")

    if n_clicks is not None:


        print("enviar informe por correo")
        archivo=crear_informe(fecha,turno)


        user = os.environ.get('user')
        app_password = os.environ.get('app_password')
        destinatarios = os.environ.get('destinatarios')
        to = destinatarios.split(";")

        subject = f'informe produccion {fecha} turno:{turno}'
        content = [f'Informe de produccion , topcolor dia {fecha} turno:{turno}', 'pytest.ini', 'test.png']

        with yagmail.SMTP(user, app_password) as yag:
            yag.send(to, subject, content, attachments=archivo)
            print('Sent email successfully')
        print("correo enviado exitoso")
        return "correo enviado exitoso",''
    return '',''

def encode_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        encoded_pdf = base64.b64encode(file.read()).decode('utf-8')
    return encoded_pdf


########################################MENSAJE MODAL
@app.callback(
    Output("modal_in", "is_open"),
    [Input("open_in", "n_clicks"), Input("close_in", "n_clicks")],
    [State("modal_in", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def msj_in():
    return html.Div(
    [
        dbc.Button("Open modal", id="open_in", n_clicks=1,style={'display':'none'}),
        dbc.Modal(
            [
                dbc.ModalHeader("Topcolor"),
                dbc.ModalBody("Informe Descargado Correctamente"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_in", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_in",
            is_open=False,
        ),
    ]
)


def crear_informe(fecha,turno):
    ahora = datetime.now()
    ahora_str = ahora.strftime("%Y%m%d%H%M%S")
    valor = turno
    ip = host
    puerto = port_reporte
    print(f"valor leido es {valor} con fecha {fecha}")
    print(f" inicio crera funcion antes de usuario :{datetime.now()}")
    # usuario()
    url7 = f'http://{ip}:{puerto}/estado_reporte_turno/&{str(valor)}/&{str(fecha)}'
    datos7 = urlopen(url7)
    usuario7 = json.loads(datos7.read())
    print(f" inicio crera funcion despues de usuario :{datetime.now()} con usuario7={usuario7}")
    if True:
        print(f"existe datos para informe")
        ## Obtengo las variables fecha y turno de la pagina #########
        fecha = fecha
        turno = valor

        id = usuario7["id_reporte"]

        print(f"el id es {id}")
        url8 = f'http://{ip}:{puerto}/tabla_resumen_linea/&{str(str(usuario7["id_reporte"]))}'
        print(url8)
        datos8 = urlopen(url8)
        usuario8 = json.loads(datos8.read())
        print('USUARIO8', usuario8)

        usuarios = []
        print(f" linea 271 :{datetime.now()}")
        print(f'http://{ip}:{puerto}/infoLinea/&1/&{str(usuario7["id_reporte"])}')
        print(f'http://{ip}:{puerto}/infoLinea/&2/&{str(usuario7["id_reporte"])}')

        usuario9 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&1/&{str(usuario7["id_reporte"])}').read())
        usuario10 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&2/&{str(usuario7["id_reporte"])}').read())
        usuario11 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&3/&{str(usuario7["id_reporte"])}').read())
        usuario12 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&4/&{str(usuario7["id_reporte"])}').read())
        usuario13 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&5/&{str(usuario7["id_reporte"])}').read())
        usuario14 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&6/&{str(usuario7["id_reporte"])}').read())
        usuario15 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&7/&{str(usuario7["id_reporte"])}').read())
        usuario16 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&8/&{str(usuario7["id_reporte"])}').read())##linea aditivo
        usuario17 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&9/&{str(usuario7["id_reporte"])}').read())
        usuario18 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&10/&{str(usuario7["id_reporte"])}').read())
        usuario19 = json.loads(urlopen(f'http://{ip}:{puerto}/infoLinea/&10/&{str(usuario7["id_reporte"])}').read())### linea compostable
        print("$" * 100)
        print(f'http://{ip}:{puerto}/infoLinea/&3/&{str(usuario7["id_reporte"])}')
        #print(f'http://{ip}:{puerto}/infoLinea/&6/&{str(usuario7["id_reporte"])}')
        #print(usuario14)


        usuarios.append(usuario9)
        usuarios.append(usuario10)
        usuarios.append(usuario11)
        usuarios.append(usuario12)
        usuarios.append(usuario13)
        usuarios.append(usuario14)
        usuarios.append(usuario15)
        usuarios.append(usuario16)
        usuarios.append(usuario17)
        usuarios.append(usuario18)
        usuarios.append(usuario19)

        root_dir = os.getcwd()  # ruta actual
        nombre = f"informe_topcolor_{id}_{ahora_str}.pdf"  # nombre archivo
        ruta = f"{root_dir}/informe/{nombre}"

        pagesize = (30 * inch, 10 * inch)  # 20 inch width and 10 inch height

        doc = SimpleDocTemplate(ruta, pagesize=letter) # tamaño letter

        #doc = SimpleDocTemplate(ruta, pagesize=letter,leftMargin=2.2*inch, rightMargin=2.2*inch,topMargin=0.1*inch,bottomMargin=0.1*inch)  # tamaño letter
        # Obtener una hoja de estilos de ejemplo
        styles = getSampleStyleSheet()
        # print(letter)
        # Definir un estilo personalizado con el formato de letra deseado
        mi_estilo = ParagraphStyle(name='mi_estilo', parent=styles['Normal'], fontSize=6.5)
        mi_estilo2 = ParagraphStyle(name='mi_estilo', parent=styles['Normal'], fontSize=8.5, textColor=colors.white, alignment=0)

        mi_estilo_3 = ParagraphStyle(name='mi_estilo', parent=styles['Normal'], fontSize=8)
        mi_estilo10 = ParagraphStyle(name='mi_estilo', parent=styles['Normal'], fontSize=4.5)

        #logo
        _imagen = "imagenes/img.png"
        #_imagen = "assets/topcolor.png"

        # Unir el directorio actual con el  del archivo
        ruta_archivo2 = os.path.join(directorio_actual, _imagen)

        pdf_path2 = ruta_archivo2
        formato = "%Y-%m-%d"
        fecha_date = datetime.strptime(fecha, formato)

        ##### Creo las listas de los dias y semanas para ser leida a gusto ######
        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        dia_semana_espanol = dias_semana[fecha_date.weekday()]
        dias_mes = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre","octubre", "noviembre", "diciembre"]
        mes_espanol = dias_mes[fecha_date.month - 1]

        # Imprimir los resultados
        dia_escrito = dia_semana_espanol
        dia_numero = fecha_date.strftime("%d")
        mes = mes_espanol
        año = fecha_date.strftime("%Y")
        #### Se crea la imagen de topcolor y sus dimensiones #########
        logo = Image(pdf_path2)
        logo.drawHeight = 0.6 * inch * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 0.6 * inch
        # lineas = list(usuario1)
        Fecha = Paragraph(f"{dia_escrito}, {dia_numero} {mes}, {año}", mi_estilo2)
        ###### Se crean los paragraphs con texto en cada casilla de la primera tabla #############
        A = Paragraph("LÍNEA DE TRABAJO", mi_estilo)
        L1 = Paragraph("LinC1", mi_estilo)
        L2 = Paragraph("LinC2", mi_estilo)
        L3 = Paragraph("LinC3", mi_estilo)
        L4 = Paragraph("LinC4", mi_estilo)
        L5 = Paragraph("LinC5", mi_estilo)
        L6 = Paragraph("LinC6", mi_estilo)
        L7 = Paragraph("LinC7", mi_estilo)
        L8 = Paragraph("LinC8", mi_estilo) #cambio orden para mostrar l8 antes que linea adt
        L9 = Paragraph("LinBlc", mi_estilo)
        L10 = Paragraph("LinAdt", mi_estilo)
        L11 = Paragraph("LinCompost", mi_estilo)
        E1 = Paragraph("TIEMPO  EXTRUSIÓN [min]", mi_estilo)
        print("------291---")
        E2 = Paragraph(f"{usuario8['datos'][0]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E3 = Paragraph(f"{usuario8['datos'][1]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E4 = Paragraph(f"{usuario8['datos'][2]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E5 = Paragraph(f"{usuario8['datos'][3]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E6 = Paragraph(f"{usuario8['datos'][4]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E7 = Paragraph(f"{usuario8['datos'][5]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E8 = Paragraph(f"{usuario8['datos'][6]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E9 = Paragraph(f"{usuario8['datos'][9]['Tiempo Extrusión[min]']}",mi_estilo_3)#cambio orden para mostrar l8 antes que linea adt
        E10 = Paragraph(f"{usuario8['datos'][8]['Tiempo Extrusión[min]']}",mi_estilo_3)
        E11 = Paragraph(f"{usuario8['datos'][7]['Tiempo Extrusión[min]']}",mi_estilo_3)
        ECOM = Paragraph(f"{usuario8['datos'][7]['Tiempo Extrusión[min]']}", mi_estilo_3)##COMPOSTABLE
        E12 = Paragraph("PRODUCCION [Kg]", mi_estilo)
        E13 = Paragraph(f"{usuario8['datos'][0]['Produccion[Kg]']}",mi_estilo_3)
        E14 = Paragraph(f"{usuario8['datos'][1]['Produccion[Kg]']}",mi_estilo_3)
        E15 = Paragraph(f"{usuario8['datos'][2]['Produccion[Kg]']}",mi_estilo_3)
        E16 = Paragraph(f"{usuario8['datos'][3]['Produccion[Kg]']}",mi_estilo_3)
        E17 = Paragraph(f"{usuario8['datos'][4]['Produccion[Kg]']}",mi_estilo_3)
        E18 = Paragraph(f"{usuario8['datos'][5]['Produccion[Kg]']}",mi_estilo_3)
        E19 = Paragraph(f"{usuario8['datos'][6]['Produccion[Kg]']}",mi_estilo_3)
        E20 = Paragraph(f"{usuario8['datos'][9]['Produccion[Kg]']}",mi_estilo_3)
        E21 = Paragraph(f"{usuario8['datos'][8]['Produccion[Kg]']}",mi_estilo_3)
        E22 = Paragraph(f"{usuario8['datos'][7]['Produccion[Kg]']}",mi_estilo_3)
        ECOM2 = Paragraph(f"{usuario8['datos'][7]['Produccion[Kg]']}", mi_estilo_3)# COMPOSTABLE
        E23 = Paragraph("RENDIMIENTO REAL [Kg/h]", mi_estilo)
        E24 = Paragraph(f"{usuario8['datos'][0]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E25 = Paragraph(f"{usuario8['datos'][1]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E26 = Paragraph(f"{usuario8['datos'][2]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E27 = Paragraph(f"{usuario8['datos'][3]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E28 = Paragraph(f"{usuario8['datos'][4]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E29 = Paragraph(f"{usuario8['datos'][5]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E30 = Paragraph(f"{usuario8['datos'][6]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E31 = Paragraph(f"{usuario8['datos'][9]['Rendimiento Real[Kg/h]']}",mi_estilo_3)#cambio orden para mostrar l8 antes que linea adt
        E32 = Paragraph(f"{usuario8['datos'][8]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        E33 = Paragraph(f"{usuario8['datos'][7]['Rendimiento Real[Kg/h]']}",mi_estilo_3)
        ECOM3 = Paragraph(f"{usuario8['datos'][7]['Rendimiento Real[Kg/h]']}", mi_estilo_3)  # COMPOSTABLE
        ###
        E34 = Paragraph("TIEMPO DETENCIÓN [min]", mi_estilo)
        E35 = Paragraph(f"{usuario8['datos'][0]['Tiempo Detensión[min]']}",mi_estilo_3)
        E36 = Paragraph(f"{usuario8['datos'][1]['Tiempo Detensión[min]']}",mi_estilo_3)
        E37 = Paragraph(f"{usuario8['datos'][2]['Tiempo Detensión[min]']}",mi_estilo_3)
        E38 = Paragraph(f"{usuario8['datos'][3]['Tiempo Detensión[min]']}",mi_estilo_3)
        E39 = Paragraph(f"{usuario8['datos'][4]['Tiempo Detensión[min]']}",mi_estilo_3)
        E40 = Paragraph(f"{usuario8['datos'][5]['Tiempo Detensión[min]']}",mi_estilo_3)
        E41 = Paragraph(f"{usuario8['datos'][6]['Tiempo Detensión[min]']}",mi_estilo_3)
        E42 = Paragraph(f"{usuario8['datos'][9]['Tiempo Detensión[min]']}",mi_estilo_3)#cambio orden para mostrar l8 antes que linea adt
        E43 = Paragraph(f"{usuario8['datos'][8]['Tiempo Detensión[min]']}",mi_estilo_3)
        E44 = Paragraph(f"{usuario8['datos'][7]['Tiempo Detensión[min]']}",mi_estilo_3)
        ECOM4 = Paragraph(f"{usuario8['datos'][7]['Tiempo Detensión[min]']}", mi_estilo_3)#COMPOSTABLE

        E45 = Paragraph("  ")
        E46 = Paragraph("  ")
        E47 = Paragraph("  ")
        E48 = Paragraph("  ")
        E49 = Paragraph("  ")
        E50 = Paragraph("  ")
        E51 = Paragraph("  ")
        E52 = Paragraph("  ")
        E53 = Paragraph("  ")
        E54 = Paragraph("  ")
        E55 = Paragraph("  ")

        ####Los estilos de las tablas correspondientes #############
        estilo_celda = TableStyle([
            ('BOX', (0, 0), (-1, -1), 0, 'WHITE'),  # Sin bordes
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),  # Color de texto negro
            ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
            # ('WORDWRAP', (0, 0), (-1, -1), 0, 0),
        ])
        
        ##estilo para la tabla donde esta el jefe de turno, turno id de informe
        estilo_celda2 = TableStyle([
            ('BOX', (1, 0), (3, 2), 0, 'BLACK'),  # Sin bordes
            ('TEXTCOLOR', (2, 0), (2, 2), colors.white),  # Color de texto negro
            ('BACKGROUND', (1, 0), (1, 2), colors.grey),
            ('BACKGROUND', (2, 0), (2, 2), colors.white),
            ('GRID', (1, 0), (3, 2), 0.5, colors.black),
            ('FONTSIZE', (1, 0), (2, 1), 6),
            ('WORDWRAP', (0, 0), (-1, -1), 0, 0),
        ])
        estilo_celda3 = TableStyle([
            ('BOX', (0, 0), (1, 2), 0, 'BLACK'),  # Sin bordes
            ('BOX', (3, 0), (4, 2), 0, 'BLACK'),  # Sin bordes
            ('BOX', (6, 0), (7, 2), 0, 'BLACK'),  # Sin bordes
            ('BOX', (9, 0), (10, 2), 0, 'BLACK'),  # Sin bordes
            ('TEXTCOLOR', (0, 0), (0, 2), colors.white),  # Color de texto blanco
            ('TEXTCOLOR', (3, 0), (3, 2), colors.white),  # Color de texto blanco
            ('TEXTCOLOR', (6, 0), (6, 2), colors.white),  # Color de texto blanco
            ('TEXTCOLOR', (9, 0), (9, 2), colors.white),  # Color de texto blanco
            ('BACKGROUND', (0, 0), (0, 2), colors.grey),
            ('BACKGROUND', (3, 0), (3, 2), colors.grey),
            ('BACKGROUND', (6, 0), (6, 2), colors.grey),
            ('BACKGROUND', (9, 0), (9, 2), colors.grey),
            # ('BACKGROUND', (1,0), (1,1), colors.grey),
            # ('BACKGROUND', (2,0), (2,1), colors.white),
            ('GRID', (0, 0), (1, 2), 0.5, colors.black),
            ('GRID', (3, 0), (4, 2), 0.5, colors.black),
            ('GRID', (6, 0), (7, 2), 0.5, colors.black),
            ('GRID', (9, 0), (10, 2), 0.5, colors.black),
            ('FONTSIZE', (1, 0), (-1, -1), 6),
            ('WORDWRAP', (0, 0), (0, 2), 0, 0),
        ])

        estilo_celda4 = TableStyle([
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),  # Color de texto negro
            ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),])

        estilo_celda5 = TableStyle([('BOX', (0, 0), (0, 1), 0.5, colors.black)])

        ##nombre turno

        n_turno=nombre_turno(turno)


        #### Los datos de las tablas correspondientes ################
        data1 = [[logo,"    " ,Paragraph('REPORTE  POR TURNO', mi_estilo2), Fecha]]
        data2 = [[" ", Paragraph("ID reporte:", mi_estilo), Paragraph(f"{id}", mi_estilo)],
                 [" ", Paragraph("TURNO:", mi_estilo), Paragraph(f"{n_turno}", mi_estilo)],
                 [" ", Paragraph("LÍDER DE TURNO:", mi_estilo),Paragraph(f"{usuario7['jefeTurno']['jefeTurno']}", mi_estilo)]]
        data3 = [[Paragraph('RESUMEN DEL TURNO', mi_estilo2)]]

        ######## Creación de tablas ##################
        tabla = Table(data1)
        tabla2 = Table(data2)
        tabla3 = Table(data3)

        ###### Insertar estilos #############
        tabla.setStyle(estilo_celda)
        tabla2.setStyle(estilo_celda2)
        tabla3.setStyle(estilo_celda)

    # _argW y _argH son el alto y ancho de cada fila y columna por letter que son las dimensiones de cada hoja en pdf

    tabla._argW[0] = 0.3 * inch
    tabla._argH[0] = 20
    data = [[A, L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11],
            [E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, ECOM],
            [E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, ECOM2],
            [E23, E24, E25, E26, E27, E28, E29, E30, E31, E32, E33, ECOM3],
            [E34, E35, E36, E37, E38, E39, E40, E41, E42, E43, E44, ECOM4],]
    t = Table(data, style=[
        ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (11, 0), colors.lightgrey),
        ('ALIGN', (3, 1), (3, 1), 'CENTER'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (3, 2), (3, 2), 'LEFT'),
        ('WORDWRAP', (0, 0), (-1, -1), 0, 0),])
    ##################################GRAFICOS##########################################################
    graficos_guardados = []
    for i in range(len(usuario8['datos'])): #len(usuario8['datos'])
        df = pd.DataFrame(usuarios[1]["grafico"])
        print('ccccc',df)
        if i == 0 or i == 1 or i == 8 or i == 9:  #8 es para blanco, 9 es para la linea 8 real
            print('USUARIOS', range(len(usuario8['datos'])))
            if usuarios[i]["estado"] == 102:
                pd.DataFrame(usuarios[i]["mensaje"])
            df = pd.DataFrame(usuarios[i]["grafico"])
            plt.figure()
            plt.plot(pd.to_datetime(df['fecha'], unit='ms'), pd.to_numeric(df['canal1'].fillna("").astype('string')), linewidth=0.5, label='Motor 1', color='blue')
            plt.plot(pd.to_datetime(df['fecha'], unit='ms'), pd.to_numeric(df['canal2'].fillna("").astype('string')),linewidth=0.5, label='Motor 2', color='red')
            plt.legend(['ch0', 'ch1'])
            ax = plt.gca()

            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            y_max = df[[str('canal1'), str('canal2')]].max().max()
            #ax.set_ylim(0, y_max * 1.2)  # Puedes ajustar el factor de multiplicación según tus necesidades
            ax.set_ylim(-1, 3)  # Puedes ajustar el factor de multiplicación según tus necesidades
            nombre_archivo2 = str(f"graficos/grafico_linea{i + 1}.png")
            # plt.legend(loc='upper right') agrega leyenda a los gráficos
            plt.xlabel('horario', fontsize=10, color='black')
            plt.ylabel('canales digitales', fontsize=10, color='black')
            plt.savefig(nombre_archivo2)
            plt.close()
            graficos_guardados.append(nombre_archivo2)
        else:
            df = pd.DataFrame(usuarios[i]["grafico"])
            #print(df)
            plt.figure()
            #plt.plot(pd.to_datetime(df['fecha']), pd.to_numeric(df['r40001'].fillna("").astype('string')),linewidth=0.5, label='Motor 1', color='blue')
            #plt.plot(pd.to_datetime(df['fecha']), pd.to_numeric(df['r40003'].fillna("").astype('string')),linewidth=0.5, label='Motor 2', color='red')

            plt.plot(pd.to_datetime(df['fecha'], unit='ms'), pd.to_numeric(df['r40001'].fillna("").astype('string')),linewidth=0.5, label='Set[Kg/H]', color='blue')
            plt.plot(pd.to_datetime(df['fecha'], unit='ms'), pd.to_numeric(df['r40003'].fillna("").astype('string')), linewidth=0.5, label='Real[Kg/H]', color='red')
            plt.legend(['Set[Kg/H]', 'Flujo Real[Kg/H]'])
            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            y_max = df[[str('r40001'), str('r40003')]].max().max()
            ax.set_ylim(0, y_max * 1.2)  # Puedes ajustar el factor de multiplicación según tus necesidades
            nombre_archivo1 = str(f"graficos/grafico_linea{i + 1}.png")
            # plt.legend(loc='upper right') agrega leyenda a los gráficos
            #plt.title(f'linea {i}', fontsize=20)
            plt.xlabel('horario', fontsize=10, color='black')
            plt.ylabel('flujo masa[kg/h]', fontsize=10, color='black')
            plt.savefig(nombre_archivo1)
            plt.close()
            graficos_guardados.append(nombre_archivo1)
    ####Datos del gráfico ###########
    imagenes = []
    list=[1,2,3,4,5,6,7,8,9,10,11]
    for i in range(len(list)):
        _imagen2 = f"graficos/grafico_linea{i + 1}.png"
        ruta_archivo3 = os.path.join(directorio_actual, _imagen2)
        pdf_path3 = ruta_archivo3
        I2 = Image(pdf_path3)
        imagenes.append(I2)
        imagenes[i].drawHeight = 3.5 * inch
        imagenes[i].drawWidth = 3.2 * inch

    ##### Más de arrglar filas y columnas (dimensiones) ############
    #t._argH[4] = 0.45 * inch #dimension para la tabla resumen turno, la fila 4
    #t._argH[5] = 0.45 * inch
    #t._argH[6] = 0.45 * inch
    espacio = Spacer(1, 10)
    t._argW[1] = 0.50 * inch #ancho de la primera columna
    t._argW[2] = 0.50 * inch
    t._argW[3] = 0.50  * inch
    t._argW[4] = 0.50  * inch
    t._argW[5] = 0.50  * inch
    t._argW[6] = 0.50 * inch
    t._argW[7] = 0.50 * inch
    t._argW[8] = 0.50  * inch
    t._argW[9] = 0.50  * inch
    t._argW[10] = 0.50  * inch
    t._argW[11] = 0.50 * inch

    ####Agregar a la lista elements todas las tablas  y espacios ############

####ESTA SON LAS COLUMNAS PRIMERAS, LAS GENERALES
    elements = []
    # print(len(usuario8['datos']))
    elements.append(tabla)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(tabla2)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(tabla3)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(espacio)
    elements.append(t)  ##tabla de resumenes turno

    ##ESPACIOS
    ##espaciar antes de la primera linea
    for v in range(35): ##32 #con 33 se cae el programa, usar como prueba se cae la pagina 2,, minimo es 34
        elements.append(espacio)  #espacio = Spacer(1, 10)
    ##FIN PRIMERAS TABLAS GENERALES







    ####desde aca se crean las infos de cada linea,, donde i=0 es para linea 1
   #for i in range(10): #range(len(usuario8['datos'])):  #poner en 10 para las 10 lineas
    for i in [0,1,2,3,4,5,6,9,8,7, 10]:              ##orden de las lineasm donde 7 nes aditivo y posicion 9 e linea 8
        ##nombre real de las lineas, recordar que estan almacenadas por posicion, donde i=0 es linea1, i=1 linea 2 etc
        if i==7:
            tabla4 = Table([[Paragraph(f'LÍNEA ADITIVO', mi_estilo2)]])

        elif i==8:
            tabla4 = Table([[Paragraph(f'LÍNEA BLANCO', mi_estilo2)]])
        elif i==9:
            tabla4 = Table([[Paragraph(f'LÍNEA 8', mi_estilo2)]])
        elif i == 10:
            tabla4 = Table([[Paragraph(f'LÍNEA COMPOSTABLE', mi_estilo2)]])
        else:
            tabla4 = Table([[Paragraph(f'LÍNEA {i + 1}', mi_estilo2)]])

        tabla4.setStyle(estilo_celda)
        elements.append(tabla4)
        elements.append(espacio)
        elements.append(espacio)
        tabla5 = Table([[Paragraph("OPERADOR:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['Operador']}", mi_estilo), "",
                         Paragraph("OP:", mi_estilo), Paragraph(f"{usuarios[i]['ultima_op']['OP']}", mi_estilo),
                         "", Paragraph("MB Bueno producido", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['MB Bueno Producido']}", mi_estilo), "",
                         Paragraph("Sacos envasados", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['Sacos envasados']}", mi_estilo)],
                        [Paragraph("AYUDANTE 1:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['Ayudante 1']}", mi_estilo), "",
                         Paragraph("PRODUCTO:", mi_estilo),
                         Paragraph(f" {usuarios[i]['ultima_op']['Producto']}", mi_estilo10), "",
                         Paragraph("MB Fuera de Especificación:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['MB Fuera de Especificacion Producido']}", mi_estilo), "",
                         Paragraph("MB total extruido:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['MB Total extruido']}", mi_estilo)],
                        [Paragraph("AYUDANTE 2:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['Ayudante 2']}", mi_estilo), "",
                         Paragraph("Total OP [Kg]:", mi_estilo),
                         Paragraph(f" {usuarios[i]['ultima_op']['Total Op[Kg]']}", mi_estilo), "",
                         Paragraph("MB Recirculado:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['MB Recirculado']}", mi_estilo), "",
                         Paragraph("Kg Bueno:", mi_estilo),
                         Paragraph(f"{usuarios[i]['ultima_op']['kg_bueno']}", mi_estilo)]])
        tabla5._argH[0] = 30
        tabla5._argH[1] = 30
        tabla5._argH[2] = 30
        tabla5._argW[3] = 55
        tabla5._argH[0] = 30
        tabla5._argW[1] = 60
        tabla5.setStyle(estilo_celda3)
        elements.append(tabla5)
        elements.append(espacio)
        elements.append(espacio)
        elements.append(espacio)
        tabla6 = Table([[Paragraph("RENDIMIENTO LÍNEA", mi_estilo), Paragraph("JUSTIFICA TIEMPOS", mi_estilo)]])
        tabla6.setStyle(estilo_celda4)
        elements.append(tabla6)
        elements.append(espacio)

        ##aca se forma la tabla de las justificaciones
        lis_parcial=[[Paragraph("Hora Inicio", mi_estilo), Paragraph("Hora Termino", mi_estilo),
                         Paragraph("OP", mi_estilo),
                         Paragraph("Clasificación", mi_estilo), Paragraph("Causa", mi_estilo),
           #              Paragraph("Observaciones", mi_estilo)],  #Paragraph("Observaciones", mi_estilo)],
                     ]]

        print(f" en la tabla justificacion de {i} existen {len(usuarios[i]['tablaJustificacion'])}")
        num_justificaciones=len(usuarios[i]['tablaJustificacion'])
 #numero de campos de justificacion







        for m in range(0,num_justificaciones):
            lista_buff=[]
            try:

                ##la hora llega en utc
                if usuarios[i]['tablaJustificacion'][m]['hora_inicio']=='--':
                    numero=int(0)
                    usuarios[i]['tablaJustificacion'][m]['hora_inicio']="--"
                    usuarios[i]['tablaJustificacion'][m]['hora_fin'] = "--"
                else:
                    numero = int(usuarios[i]['tablaJustificacion'][m]['hora_inicio'])
                    my_datetime = dat.fromtimestamp(numero / 1000)
                    local = my_datetime.astimezone(tzlocal()) + timedelta( hours=int(zona_horaria))  ##SE CAMBIA LA HORA TODO generar uuna mejor forma
                    hora_inicio_str = local.strftime("%d-%m %H:%M")
                    usuarios[i]['tablaJustificacion'][m]['hora_inicio'] = hora_inicio_str

                    ###hora fin
                    numero = int(usuarios[i]['tablaJustificacion'][m]['hora_fin'])
                    my_datetime = dat.fromtimestamp(numero / 1000)
                    local = my_datetime.astimezone(tzlocal()) + timedelta(hours=int(zona_horaria))
                    hora_inicio_str = local.strftime("%d-%m %H:%M")
                    usuarios[i]['tablaJustificacion'][m]['hora_fin'] = hora_inicio_str


            except:
                print("por el except es string")
            lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['hora_inicio']}", mi_estilo))
            lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['hora_fin']}", mi_estilo))
            lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['op']}", mi_estilo))
            #lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['jefe_turno']}", mi_estilo))
            lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['clasificacion']}", mi_estilo10),)
            lista_buff.append(Paragraph(f"{usuarios[i]['tablaJustificacion'][m]['causa']}", mi_estilo10))
            #lista_buff.append(Paragraph(f"-7-", mi_estilo))

            lis_parcial.append(lista_buff)
            ##para hacer espacio
       # lis_parcial.append([Paragraph("", mi_estilo), Paragraph("", mi_estilo), Paragraph("", mi_estilo),Paragraph("", mi_estilo), Paragraph("", mi_estilo) ])

        tabla8 = Table(lis_parcial,style=[
            ('BOX', (0, 0), (-1, -1), 1, 'BLACK'),  # Sin bordes
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (6, 0), colors.grey),
            ('FONTSIZE', (0, 0), (-1, -1), 4)])

        for c in range(2,len(lis_parcial)):
            tabla8._argH[c] = 30


        ##esto se puede borrar, era para insertar una imagen
        _imagen3 = "imagenes/rendimiento.png"
        ruta_archivo4 = os.path.join(directorio_actual, _imagen3)
        pdf_path4 = ruta_archivo4
        I3 = Image(pdf_path4)
        I3.drawHeight = 0.55 * inch
        I3.drawWidth = 2.8 * inch
        tabla11 = Table([[I3]])
        #################

        dat_rendimiento = usuarios[i]['rendimientosLineas'][0]
        data8 = [["R. Maximo[Kg/H]", "R. Medio[Kg/H]", "R. Real[Kg/H]"],[dat_rendimiento['rendimientoMaximo'], dat_rendimiento['rendimientoMedio'],dat_rendimiento['rendimientoReal']]]
        tab_rend = Table(data8, style=[
            ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (10, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('WORDWRAP', (0, 0), (-1, -1), 0, 0),
        ])
        #tab_rend._argW[0] = 0.70 * inch  # ancho de la primera columna
        ##tabla 11 es un dibujo que muestra los rendimientos

        tabla9 = Table([[Paragraph("Observación general:", mi_estilo)],[Paragraph(f'{usuarios[i]["observacion"]}', mi_estilo)]])
        tabla9.setStyle(estilo_celda5)


        #esto estaba
        ##tabla10 = Table([[imagenes[i], tabla8], [tabla11, tabla9]])
        tabla10 = Table([[imagenes[i], tabla8], [tab_rend, tabla9]])
        elements.append(tabla10)


        ##espaciados al final
        lista=[]#6,8,9,10,7
        print(f"PARA LA LINEA {i}  datos justificados es {num_justificaciones}")

        tabla_buff = Table([[Paragraph(f'LÍNEA {i + 1} con numero justificaciones {num_justificaciones}', mi_estilo2)]])
        tabla_buff.setStyle(estilo_celda)
        elements.append(PageBreak())


        '''
       
       
            if i<5 :  #pagina 1,2,3                                         
                for f in range(15-num_justificaciones):  # 18               
                    elements.append(espacio)                                
                elements.append(tabla_buff)                                 
                elements.append(PageBreak())                                
                #PageBreak()                                                
            else:                                                           
                for f in range(0):  # 17  ##probar con 15                   
                    elements.append(espacio)                                
                                                                            
        
        '''













    ###Aquí se crea el pdf y se puede descargar desde el navegador##############
    doc.build(elements)
    return ruta

def nombre_turno(turno):
    nombreTurno = ""
    if turno.upper() == "A":
        nombreTurno = "Mañana"
    elif turno.upper() == "B":
        nombreTurno = "Tarde"
    elif turno.upper() == "C":
        nombreTurno = "Noche"
    elif turno.upper() == "D":
        nombreTurno = "Sabado"
    return nombreTurno