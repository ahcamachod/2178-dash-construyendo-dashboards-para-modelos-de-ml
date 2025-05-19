from dash import Dash, html, dcc, Input, Output
from dash.dependencies import State,Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import joblib

modelo = joblib.load('modelo_xgboost.pkl')
medianas = joblib.load('medianas.pkl')

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

formulario = dbc.Container([
    html.P('Por favor, llene los siguientes campos con sus informaciones para utilizar el modelo y presione el botón Enviar.',className='text-center mb-5'),
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Label("Edad"),
                dbc.Input(id='age', type='number', placeholder='Digite su edad'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Sexo biológico"),
                dbc.Select(id='sex', options=[
                    {'label': 'Masculino', 'value': '1'},
                    {'label': 'Femenino', 'value': '0'}
                ]),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Tipo de dolor en el pecho"),
                dbc.Select(id='cp', options=[
                    {'label': 'Angina típica', 'value': '1'},
                    {'label': 'Angina atípica', 'value': '2'},
                    {'label': 'Dolor no anginoso', 'value': '3'},
                    {'label': 'Angina asintomática', 'value': '4'}
                ]),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Presión arterial en reposo"),
                dbc.Input(id='trestbps', type='number', placeholder='Digite su presión arterial en reposo'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Colesterol sérico"),
                dbc.Input(id='chol', type='number', placeholder='Digite el colesterol sérico'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Glucemia en ayunas"),
                dbc.Select(id='fbs', options=[
                    {'label': 'Menor de 120 mg/dl', 'value': '0'},
                    {'label': 'Mayor de 120 mg/dl', 'value': '1'}
                ]),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Electrocardiograma en reposo"),
                dbc.Select(id='restecg', options=[
                    {'label': 'Normal', 'value': '0'},
                    {'label': 'Anomalías en ST-T', 'value': '1'},
                    {'label': 'Hipertrofia ventricular izquierda', 'value': '2'}
                ]),
            ], className='mb-3'),
        ]),
        dbc.Col([
            dbc.CardGroup([
                dbc.Label("Frecuencia cardíaca máxima alcanzada"),
                dbc.Input(id='thalach', type='number', placeholder='Digite su frecuencia cardíaca máxima alcanzada'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Angina inducida por ejercicio"),
                dbc.Select(id='exang', options=[
                    {'label': 'Sí', 'value': '1'},
                    {'label': 'No', 'value': '0'}
                ]),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Depresión del segmento ST inducida por ejercicio"),
                dbc.Input(id='oldpeak', type='number', placeholder='Digite su depresión del segmento ST inducida por ejercicio'),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Pendiente del segmento ST"),
                dbc.Select(id='slope', options=[
                    {'label': 'Ascendente', 'value': '1'},
                    {'label': 'Plana', 'value': '2'},
                    {'label': 'Descendente', 'value': '3'}
                ]),
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Número de vasos principales coloreados por fluoroscopía"),
                dbc.Select(id='ca',
                    options = [
                        { 'label': '0', 'value': '0' },
                        { 'label': '1', 'value': '1' },
                        { 'label': '2', 'value': '2' },
                        { 'label': '3', 'value': '3' },
                    ]
                )
            ], className='mb-3'),
            dbc.CardGroup([
                dbc.Label("Centellografía miocárdica"),
                dbc.Select(id='thal', options=[
                    {'label': 'Normal', 'value': '3'},
                    {'label': 'Defecto fijo', 'value': '6'},
                    {'label': 'Defecto reversible', 'value': '7'}
                ]),
            ], className='mb-3'),
            dbc.Button('Enviar', id='submit-button', n_clicks=0,color='success',className='mb-3 mt-3')
        ])
    ])
],fluid=True)

app.layout = html.Div([
    html.H1("Formulario para la previsión de enfermedad coronaria",className='text-center mb-5 mt-5'),
    formulario,
    html.Div(id='prevision')
])

@app.callback(
    Output('prevision', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('age', 'value'),
     State('sex', 'value'),
     State('cp', 'value'),
     State('trestbps', 'value'),
     State('chol', 'value'),
     State('fbs', 'value'),
     State('restecg', 'value'),
     State('thalach', 'value'),
     State('exang', 'value'),
     State('oldpeak', 'value'),
     State('slope', 'value'),
     State('ca', 'value'),
     State('thal', 'value')]
)
def prever_enfermedad(n_clicks,age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal):
    if n_clicks == 0:
        return ''    
    entradas_usuario = pd.DataFrame(
     data = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
     columns= ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    )

    entradas_usuario = entradas_usuario.fillna(medianas)

    # convierte la columna oldpeak en float
    entradas_usuario['oldpeak'] = entradas_usuario['oldpeak'].astype(np.float64)

    # convierte las demás columnas en int
    for columna in entradas_usuario.columns:
        if columna != 'oldpeak':
            entradas_usuario[columna] = entradas_usuario[columna].astype(np.int64)

    prevision = modelo.predict(entradas_usuario)[0]

    if prevision == 1:
        mensaje = 'Hay enfermedad coronaria'
        color_alerta = 'danger'
    else:
        mensaje = 'No hay enfermedad coronaria'
        color_alerta = 'light'
    alerta = dbc.Alert(mensaje,color=color_alerta,className='d-flex justify-content-center mb-5')
    return alerta

app.run_server(debug=True)
# app.run_server(debug=True)