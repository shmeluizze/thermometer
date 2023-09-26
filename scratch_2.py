import dash
from dash import Dash, callback, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        html.H1("Temperature Converter"),
        html.Div(
            [
                html.Label("Enter temperature in Celsius: "),
                dcc.Input(id='input-celsius', type='number', value=0, disabled=True, style={
                    'marginRight': '10px', 'padding': '5x', 'fontSize': '14px', 'width': '150px'}),
                html.Button('Convert', id='button-convert', n_clicks=0, disabled=True, style={
                    'padding': '5px',
                    'width': '100px',
                    'fontSize': '14px',
                    'border': 'none',
                    'cursor': 'pointer',
                    'color': 'blue'}),

            ],
            className="input-container",
        ),
        html.Div(
            [
                dbc.Button("Kelvin", id="btn-kelvin", color="secondary", size="sm", className="mr-2", style={
                    'padding': '5px',
                    'fontSize': '14px',
                    'width': '100px',
                    'border': 'none',
                    'cursor': 'pointer'},

                           ),

                dbc.Button("Fahrenheit", id="btn-fahrenheit", color="secondary", size="sm", className="mr-2",
                           style={
                               'margin': '20px',
                               'marginLeft': '10px',
                               'padding': '5px',
                               'fontSize': '14px',
                               'width': '100px',
                               'border': 'none',
                               'cursor': 'pointer'}),
                dcc.Input(id="hidden-btn-kelvin", type="hidden", value=0),
                dcc.Input(id="hidden-btn-fahrenheit", type="hidden", value=0)
            ],

            className="unit-buttons-container",
        ),
        daq.Thermometer(
            id='my-thermometer-1',
            value=0,
            min=0,
            max=100,
            label="Temperature",
            showCurrentValue=True,
            units="C",
            style={
                'marginBottom': '5%'
            }

        ),
        html.Div(id='output-container')
    ]
)


# callback to enable input and 'btn-convert'
@app.callback(
    [Output("input-celsius", "disabled"), Output("button-convert", "disabled")],
    [Input("hidden-btn-fahrenheit", "value"), Input("hidden-btn-kelvin", "value")]

)
def enable_input(btn_fahrenheit_clicks, btn_kelvin_clicks):
    return (False, False) if btn_fahrenheit_clicks or btn_kelvin_clicks else (True, True)


@app.callback(
    Output("hidden-btn-kelvin", "value"),
    [Input("btn-kelvin", "n_clicks")]
)
def update_kelvin_clicks(n_clicks):
    return n_clicks


@app.callback(
    Output(component_id="hidden-btn-fahrenheit", component_property="value"),
    [Input(component_id="btn-fahrenheit", component_property="n_clicks")]
)
def update_fahrenheit_clicks(n_clicks):
    return n_clicks


@app.callback(
    [Output(component_id="input-celsius", component_property="units"),
     Output(component_id="output-container", component_property="children"),
     Output(component_id="my-thermometer-1", component_property="value")],

    [Input(component_id="button-convert", component_property="n-clicks")],

    [State(component_id="input-celsius", component_property="value"),
     State(component_id="hidden-btn-fahrenheit", component_property="value"),
     State(component_id="hidden-btn-kelvin", component_property="value")],
)
def convert_temperature(n_clicks, celsius, btn_fahrenheit_clicks, btn_kelvin_clicks):
    if n_clicks and celsius is not None:
        ctx = dash.callback_context
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if trigger_id == 'button-convert':
            if btn_fahrenheit_clicks:
                fahrenheit = 1.8 * celsius + 32
                return fahrenheit, f"Converted value: {fahrenheit:.2f}F", round(fahrenheit, 2)
            elif btn_kelvin_clicks:
                kelvin = celsius + 273.15
                return kelvin, f"Converted value: {kelvin:.2f}K", round(kelvin, 2)
    return 0, "", "C"


# run app
if __name__ == '__main__':
    app.run_server(debug=True)
