from dash import Dash, html, dcc
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
import plotly.graph_objects as go
from datetime import date
import math


df = pd.read_csv('app/dataframe/property_df.csv')
counties = pd.read_csv('app/dataframe/municipios.csv')

print(df)