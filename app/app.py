from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.graph_objects as go
from datetime import date
import math

from .categorizing import categorizing
from .distance_calc import calculate_distance, producers_number
from .func_map import figure_criation


df = pd.read_csv('app/dataframe/property_df.csv')
counties = pd.read_csv('app/dataframe/municipios.csv')

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_numeric = df.drop(["Latitude", "Longitude"], axis=1)
df_numeric = df_numeric.select_dtypes(include=numerics)
for i in df_numeric.columns:
    df_categorys = categorizing(df_numeric, i)

df = df.merge(df_categorys, how='inner', on=['Area (hectares)', 'Number of Cows', 'Milk Collection (liters/day)'])

counties['MUNICIPIO_UF'] = counties.MUNICIPIO +"-"+ counties.UF
counties_list = list(counties.MUNICIPIO_UF.unique())

groupby_list = ["Solar Energy", "Veterinarian", "Milk Collection (liters/day)_cat"]

options_counties = [{'label': item.upper(), 'value': item} for item in counties_list]

options_groupby = [{'label': item.upper(), 'value': item} for item in groupby_list]

dropdown_counties = dcc.Dropdown(
    id = 'dropdown_counties',
    options=options_counties,
    value="",
    style={'font-size': 15}
)

dropdown_groupby = dcc.Dropdown(
    id = 'dropdown_groupby',
    options=options_groupby,
    value="Veterinarian",
    style={'font-size': 15}
)

fig = figure_criation(df, "Veterinarian")

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([

             html.Div([
                        html.H5('Group by:'),
                        dropdown_groupby
                        ], style={"width":"250px", "margin":'30px', "padding":"0", 'display':'Block'}, id="groupby"),

            dcc.Checklist(
                id = 'checklist',
                options=[
                    {"label":'Por lat long', "value":'lat_long'}
                    ],
                inline=True,
                labelStyle={"margin-right": "10px", "display":"inline-block", 'font-size':"30px"}
            ),

            dbc.Row([
                html.Div([
                        html.H5('Municípios'),
                        dropdown_counties
                        ], style={"width":"150px", "margin":'30px', "padding":"0", 'display':'Block'}, id="counties"),

                html.Div([

                    html.H5('Latitude'),
                    dcc.Input(id="input_lat", type="number", placeholder="", debounce=True),
                    html.H5('Longitude'),
                    dcc.Input(id="input_long", type="number", placeholder="", debounce=True),

                ], style={"width":"200px", "margin":'0px', "padding":"5px", 'display':''}, id = "inputs_lat_long"),
                
                html.Div([
                    html.H5('Raio'),
                    dcc.Input(id="input_raio", type="number", placeholder="", debounce=True)
                ])
            ], style={'margin':'10px', 'width': '400px'}),

            dbc.Row([
                html.H5("Número de produtores:", className="card-text"),
                html.H5(style={"color": "#38B698"}, id="producers"),
                ]),

            html.Div([
                    html.Button("Download Excel", id="btn_xlsx"),
                    dcc.Download(id="download-dataframe-xlsx"),
                ]),
        ], md=4),

        dbc.Col([
            dcc.Graph(id="choropleth-map", figure=fig, style={'height': '100vh', 'margin-right': '0px', 'padding': '0px', "width":"1000px"})
        ], md=8),
        
        
    ]), style={'margin':'0px', 'flex-wrap': 'nowrap'}
)

@app.callback(
    Output('inputs_lat_long', 'style'),
    [Input('checklist', 'value')]
)
def update_checklist(value):
    if value is None:
        value = []

    if 'lat_long' in value:
        return {'display': 'block'} 
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('counties', 'style'),
    [Input('checklist', 'value')]
)
def update_checklist(value):
    if value is None:
        value = []
    
    if 'lat_long' in value:
        return {'display': 'none'} 
    else:
        return {'display': 'block'}
    
@app.callback(
    [
        Output("producers", 'children')
    ],
    [
        Input(component_id="input_lat", component_property='value'),
        Input(component_id="input_long", component_property='value'),
        Input(component_id="input_raio", component_property='value'),
    ]
)
def update_numero_produtores(input_latitude, input_longitude, input_raio): 
    if bool(bool(input_latitude)*bool(input_longitude)*bool(input_raio)):
        df['distance'] = df.apply(lambda row: calculate_distance(float(row['Latitude']), float(row['Longitude']), input_latitude, input_longitude), axis=1)
        dict_numero_produtores = producers_number(df, input_raio)
        retorno_numero_produtores = f'''{input_raio}km: {dict_numero_produtores[input_raio]}'''
        return [retorno_numero_produtores]
    else:
        return ["NA"]

@app.callback(
    [
        Output("input_lat", "value"),
        Output("input_long", "value"),
    ],
    [
        Input(component_id='dropdown_counties', component_property='value'),
    ]
)
def update_inputs(dropdown_counties):
    if dropdown_counties:
        lat = counties[counties.MUNICIPIO_UF == dropdown_counties].latitude.unique()[0]
        long = counties[counties.MUNICIPIO_UF == dropdown_counties].longitude.unique()[0]
        return (lat, long)
    else:
        return ([], [])

@app.callback(
    Output("choropleth-map", "figure"),
    [
        Input("input_lat", "value"),
        Input("input_long", "value"),
        Input("input_raio", "value"),
        Input("dropdown_groupby", 'value')     
    ]
)
def update_map(input_lat, input_long, input_raio, groupby):

    if bool(bool(input_lat)*bool(input_long)*bool(input_raio)):
        circle_radius_km = float(input_raio)  # Define the radius of the circle in kilometers
        circle_points = 100  # Define the number of points that form the circle

        lat_center, lon_center = input_lat, input_long

        circle_coordinates = [] # Generate latitude and longitude coordinates for the circle
        for i in range(circle_points + 1):
            angle = math.pi * 2 * i / circle_points
            lat = lat_center + (circle_radius_km / 111.32) * math.cos(angle)  # Convert km to degrees latitude
            lon = lon_center + (circle_radius_km / (111.32 * math.cos(math.radians(lat_center)))) * math.sin(angle)  # Convert km to degrees longitude
            circle_coordinates.append((lat, lon))

        circle_lat, circle_lon = zip(*circle_coordinates)
        
        fig = figure_criation(df, groupby)

        fig.add_trace(
            go.Scattermapbox(
                lat=circle_lat,
                lon=circle_lon,
                mode='lines',
                line=dict(color='blue', width=2),
                showlegend=False
            )
        )
    
        return fig
    else:
        fig = figure_criation(df, groupby)
        
        return fig
    
    
@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input('btn_xlsx', 'n_clicks'),
    State('input_lat', 'value'),
    State('input_long', 'value'),
    State('input_raio', 'value'),
    prevent_initial_call=True
)
def saveExcel(n_clicks, input_latitude, input_longitude, input_raio):
    if n_clicks is not None:
        df['distance'] = df.apply(lambda row: calculate_distance(float(row['Latitude']), float(row['Longitude']), input_latitude, input_longitude), axis=1)
        df_download = df[df.distance <= input_raio]

        file_path = f'df_{input_latitude},{input_longitude}_{input_raio}_{date.today()}.csv'
        
        return dict(content=df_download.to_csv(sep =";", index=False, decimal=','), filename=file_path)


if __name__ == '__main__':
    debug = os.getenv("PORT", None)
    print(debug)
    app.run_server(
        debug=True if debug is None else False,
        host = os.getenv('HOST', '127.0.0.1'),
        port = os.getenv('PORT', '8050'),
    )
