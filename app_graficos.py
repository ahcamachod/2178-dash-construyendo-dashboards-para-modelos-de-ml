import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc

datos = pd.read_csv('datos.csv')
datos['disease'] = (datos.num > 0) * 1
# print(datos.head())
histograma = px.histogram(datos,x='age',title='Histograma de Edades',color='disease')

div_histograma = html.Div([
        html.H2("Frecuencia de Edades"),
       dcc.Graph(
        id='histograma',
        figure=histograma
    )
    ])

boxplot = px.box(datos, x="disease", y="age", color="disease",
             title="Boxplot de la edad por diagnóstico",
             labels={"disease": "Diagnóstico (0: No, 1: Sí)", "age": "Edad"})
div_boxplot = html.Div([
        html.H2("Boxplot de Edades por Diagnóstico"),
        dcc.Graph(
        id='boxplot',
        figure=boxplot
    )
    ])

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Datos del UCI Machine Learning Repository"),
    div_histograma,
    div_boxplot
])

# app.layout.children.append(div_histograma)

app.run_server(debug=True)