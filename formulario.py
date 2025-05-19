from dash import Dash, html, dcc, Input, Output
from dash.dependencies import State,Input, Output

app = Dash(__name__)
app.layout = html.Div([
    html.H1("Formulario de Entrada de Datos"),
    dcc.Input(id='input-edad', type='number', placeholder='Edad'),    
    html.Button('Enviar', id='submit-button', n_clicks=0),
    html.Div(id='output-container-button')
])

@app.callback(
    Output('output-container-button', 'children'),
    Input('submit-button', 'n_clicks'),
    State('input-edad', 'value')    
)
def calcula_edad(n_clicks, edad):
    if n_clicks > 0 or edad is not None:
        if edad is None:
            return 'Esperando entrada...'
        if edad < 0:
            return 'Edad no válida'
        if edad <= 18:
            return f'Edad: {edad * 12} meses'
        else:
            return f'Edad: {edad} años'
    else:
        return 'Esperando entrada...'
    
app.run_server(debug=True)