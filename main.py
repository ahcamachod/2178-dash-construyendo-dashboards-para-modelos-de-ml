from dash import Dash, html, dcc
from dash.dependencies import State,Input, Output
import dash_bootstrap_components as dbc
import paginas
from app import app

navegacion = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Gráficos", href="/graficos")),
        dbc.NavItem(dbc.NavLink("Formulario", href="/formulario")),        
    ],
    brand="Dashboard",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
           dcc.Location(id='url',refresh=False),
           navegacion,
           html.Div(id='contenido')
])

@app.callback(
    Output('contenido','children'),
    [Input('url','pathname')]
)
def mostrar_pagina(pathname):
    if pathname=='/graficos':
        # return html.P('Gráficos')
        return paginas.graficos.layout
    elif pathname=='/formulario':
        # return html.P('Formulario')
        return paginas.formulario.layout
    else:
        return html.P('Inicio')
    
app.run_server(debug=True)