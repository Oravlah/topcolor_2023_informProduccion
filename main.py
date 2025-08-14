# index page
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from server import app, server
from flask_login import logout_user, current_user
import dash_bootstrap_components as dbc
from views import  login, login_fd, logout,  home,  historico, ver_informe, informe_lin1, informe_lin2, informe_lin3, informe_lin4, informe_lin5, informe_lin6, informe_lin7, informe_lin8, informe_lin9, informe_lin10,informe_lin11,tramos_justificados,rehacer_informe,sig_informe,generar_informe,configuracion_correos

from dotenv import load_dotenv
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
ENV_VARS = os.path.join(BASEDIR, ".env")
# se cargan las variables de entorno
load_dotenv(ENV_VARS)
########################

port_web = os.environ.get('PUERTO_WEB')

navbar = dbc.NavbarSimple(
    children=[
html.Img(src='assets/topcolor.png', height="48px", width='48px', className='logo'),
        dbc.NavItem(dbc.NavLink(id='home', className='link')),
        dbc.NavItem(dbc.NavLink(id='ver_informe', className='link')),
        dbc.NavItem(dbc.NavLink(id='tramos_justificados', className='link')),
        dbc.NavItem(dbc.NavLink(id='generar_informe', className='link')),
        html.Div(id='menu_configuracion', className='link'),
        dbc.NavItem(dbc.NavLink(id='user-name', className='link')),
        dbc.NavItem(dbc.NavLink(id='logout', className='link') ),
        #html.Img(src='assets/logovesat.png', height="48px", width='100px', className='logo'),
        #dbc.Label("    ", style=dict(marginRight=10)),


    ],
    style={'height': 50},
    brand='INFORMES  TOPCOLOR',
    color= "dark",
    dark=True,

)
app.layout = html.Div(
    [
        navbar,
        html.Div([
            html.Div(
                html.Div(id='page-content', className='content'),
                className='content-container'
            ),
        ], className='container-width'),
        dcc.Location(id='url', refresh=False),
    ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        logout_user()
        return login.layout
    elif pathname == '/login':
        logout_user()
        return login.layout

    elif pathname == '/home':
        if current_user.is_authenticated:
            return home.layout
        else:
            return login_fd.layout

    elif pathname == '/tramos_justificados':
        if current_user.is_authenticated:
            return tramos_justificados.layout
        else:
            return login_fd.layout



    elif pathname == '/ver_informe':
        if current_user.is_authenticated:
            return ver_informe.layout
        else:
            return login_fd.layout

    elif pathname == '/rehacer_informe':
        if current_user.is_authenticated:
            return rehacer_informe.layout
        else:
            return login_fd.layout

    elif pathname == '/sig_informe':
        if current_user.is_authenticated:
            return sig_informe.layout
        else:
            return login_fd.layout

    elif pathname == '/generar_informe':
        if current_user.is_authenticated:
            return generar_informe.layout
        else:
            return login_fd.layout

    elif pathname == '/page-2':
        if current_user.is_authenticated:
            return ver_informe.page_2_layout
        else:
            return login_fd.layout


    elif pathname == '/configuracion_correos':
        if current_user.is_authenticated:
            return configuracion_correos.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin1':
        if current_user.is_authenticated:
            return informe_lin1.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin2':
        if current_user.is_authenticated:
            return informe_lin2.layout
        else:
            return login_fd.layout
    elif pathname == '/informe_lin3':
        if current_user.is_authenticated:
            return informe_lin3.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin4':
        if current_user.is_authenticated:
            return informe_lin4.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin5':
        if current_user.is_authenticated:
            return informe_lin5.layout
        else:
            return login_fd.layout


    elif pathname == '/informe_lin6':
        if current_user.is_authenticated:
            return informe_lin6.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin7':
        if current_user.is_authenticated:
            return informe_lin7.layout
        else:
            return login_fd.layout


    elif pathname == '/informe_lin8':
        if current_user.is_authenticated:
            return informe_lin8.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin9':
        if current_user.is_authenticated:
            return informe_lin9.layout
        else:
            return login_fd.layout


    elif pathname == '/informe_lin10':
        if current_user.is_authenticated:
            return informe_lin10.layout
        else:
            return login_fd.layout

    elif pathname == '/informe_lin11':
        if current_user.is_authenticated:
            return informe_lin11.layout
        else:
            return login_fd.layout


    elif pathname == '/logout':
        if current_user.is_authenticated:
            logout_user()
            return logout.layout
        else:
            return logout.layout
    else:
        return '404'

#####ACA VAN LOS TITULOS DEL MENU. SOLO APARARECEN CUANDO ESTE LOGUEADO
@app.callback(Output('home', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Home', href='/home')
    else:
        return '        '


@app.callback(Output('ver_informe', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Ver_Informe', href='/ver_informe')
    else:
        return '        '


@app.callback(Output('tramos_justificados', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Tramos_Justificados', href='/tramos_justificados')
    else:
        return '        '

@app.callback(Output('generar_informe', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
       return html.A('Generar_Informe', href='/generar_informe')
    else:
        return '        '


@app.callback(Output('menu_configuracion', 'children'),[Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
       return dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Configuración_Lineas", href="configuracion_lineas"),
                dbc.DropdownMenuItem("Configuración_Correos", href="configuracion_correos"),


            ],
            nav=True,
            label="Configuración",
        ),
    else:
        return '                       '




@app.callback(
    Output('user-name', 'children'),
    [Input('page-content', 'children')])
def cur_user(input1):
    #print(f"linea 174 es {current_user.username} ")
    if current_user.is_authenticated:
        return html.Div('Usuario: ' + current_user.id)
        # 'User authenticated' return username in get_id()
    else:
        return ''


@app.callback(
    Output('logout', 'children'),
    [Input('page-content', 'children')])
def user_logout(input1):
    if current_user.is_authenticated:
        return html.A('Logout', href='/logout')
    else:
        return ''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port_web)
