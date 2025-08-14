# Dash configuration
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from server import app

# Create app layout
layout = html.Div(children=[dbc.Row([dbc.Col([],width=3, align='start'),
                            dbc.Col([
                                dcc.Location(id='url_logout', refresh=True),
                            html.Div(
                                className="container",style={ 'margin-top':'20px', 'text-align':'center'},
                                    children=[dbc.Alert(html.H3('Usuario no autenticado -- Favor volver a autenticarse' ,id='alertv1'),color='danger')
                            ]
                            ),],width=6, align='center'),
                        ]),
                            dbc.Row([dbc.Col([""],width=6, align='start'),
                                     dbc.Col([html.Div(

                            # children=html.A(html.Button('LogOut'), href='/')
                            children=[
                                html.Br(),
                                html.Button(id='back-button', children='VOLVER', n_clicks=0)
                            ]
                        )],width=6, align='center'),





])


])


# Create callbacks
@app.callback(Output('url_logout', 'pathname'),
              [Input('back-button', 'n_clicks')])
def logout_dashboard(n_clicks):
    if n_clicks > 0:
        return '/'
