import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

datos = pd.read_csv('datos.csv')
datos['disease'] = (datos.num > 0) * 1
histograma = px.histogram(datos,x='age',title='Histograma de Edades',color='disease')

div_histograma = html.Div([
    # html.H2("Frecuencia de Edades"),
       dcc.Graph(
        id='histograma',
        figure=histograma
    )
    ])

boxplot = px.box(datos, x="disease", y="age", color="disease",
             title="Boxplot de la edad por diagnóstico",
             labels={"disease": "Diagnóstico (0: No, 1: Sí)", "age": "Edad"})
div_boxplot = html.Div([
        # html.H2("Boxplot de Edades por Diagnóstico"),
        dcc.Graph(
        id='boxplot',
        figure=boxplot
    )
    ])
layout = html.Div([
    html.H1("Datos del UCI Machine Learning Repository"),
    dbc.Container([
        dbc.Row([
            dbc.Col([div_histograma],md=6),
            dbc.Col([div_boxplot],md=6)
        ])
    ])    
])