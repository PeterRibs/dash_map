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
print(df.columns)
print("-"*40)
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
df_numeric = df.drop(["Latitude", "Longitude"], axis=1)
df_numeric = df_numeric.select_dtypes(include=numerics)
for i in df_numeric.columns:
    df_categorys = categorizing(df_numeric, i)

df = df.merge(df_categorys, how='inner', on=['Area (hectares)', 'Number of Cows', 'Milk Collection (liters/day)'])
print(df.columns)

counties['MUNICIPIO_UF'] = counties.MUNICIPIO +"-"+ counties.UF

counties_lista = list(counties.MUNICIPIO_UF.unique())

groupby_list = ["Solar Energy", "Veterinarian", "Milk Collection (liters/day)"]

options_counties = [{'label': item.upper(), 'value': item} for item in counties_lista]

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
                        html.H5('Agrupamento por:'),
                        dropdown_groupby
                        ], style={"width":"250px", "margin":'30px', "padding":"0", 'display':'Block'}, id="agrupamentos"),

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
                        ], style={"width":"150px", "margin":'30px', "padding":"0", 'display':'Block'}, id="municipios"),

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
                html.H5(style={"color": "#38B698"}, id="produtores"),
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

if __name__ == '__main__':
    debug = os.getenv("PORT", None)
    print(debug)
    app.run_server(
        debug=True if debug is None else False,
        host = os.getenv('HOST', '127.0.0.1'),
        port = os.getenv('PORT', '8050'),
    )
