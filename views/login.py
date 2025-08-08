from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from server import app, User
from flask_login import login_user
from werkzeug.security import check_password_hash

layout = html.Div(children=[dbc.Row([dbc.Col([],width=3, align='start'),
                                    dbc.Col([dbc.Card([

			                                dbc.CardBody(
				                                [
                                                 html.Div(
                                                     className="container",
                                                     children=[
                                                     dcc.Location(id='url_login', refresh=True),
                                                    html.Div('''POR FAVOR INICIE SESIÓN''', id='h1'),
                                                    html.Br(),
                                                    html.Div(

                                                    children=[
                                                    dcc.Input(
                                                    placeholder='Ingrese Usuario',
                                        type='text',
                                        id='uname-box'
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    dcc.Input(
                                        placeholder='Ingrese Password',
                                        type='password',
                                        id='pwd-box'
                                    ),
                                    html.Br(),
                                    html.Br(),
                                    html.Button(
                                        children='Login',
                                        n_clicks=0,
                                        type='submit',
                                        id='login-button'
                                    ),
                                    html.Div(children='', id='output-state')
                                ]
                            ),
                        ]
                    )
				]

			),
dbc.CardImg(src='assets/logovesat.png',top=True),
			# dbc.CardFooter("This is the footer"),
		], color="primary", inverse=True, style={"width": "35rem", "margin-top": '5px', 'border': 'black 1px solid','text-align':'center'},
		)

],width=4, align='center')

])

    ]
)


@app.callback(Output('url_login', 'pathname'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def sucess(n_clicks, input1, input2):
    print(f"los input del login son {input1}  {input2}")
    if input1!=None and input2!=None:
        user = User.query.filter_by(username=input1).first()
        print(user)
        if user:
            if check_password_hash(user.password, input2):
                login_user(user)
                return '/home'
            else:
                pass
        else:
            pass


@app.callback(Output('output-state', 'children'),
              [Input('login-button', 'n_clicks')],
              [State('uname-box', 'value'),
               State('pwd-box', 'value')])
def update_output(n_clicks, input1, input2):
    if n_clicks > 0:
        print("va a ahcer la consult")
        user = User.query.filter_by(username=input1).first()
        print(user)
        if user:
            if check_password_hash(user.password, input2):
                return ''
            else:
                return 'Usuario o Passwor Incorrectos'
        else:
            return 'Usuario o Passwor Incorrectos'
    else:
        return ''
