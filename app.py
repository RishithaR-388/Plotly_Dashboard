import pandas as pd
import numpy as np
import math
import plotly.express as px  # (version 4.7.0 or higher)
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd



df = pd.read_csv("data/preprocess/Processed_Temperature_change_Data.csv")
countries = df["Country Name"]


app = dash.Dash(__name__)


app.layout = html.Div([
    
            html.Div([
                    html.H2("CLIMATE CHANGE DASHBOARD",className = "title"),
                    html.H5('From 1970 - To 2019',className="description title"),
                ],
                className="header",style = {"margin-bottom": "25px"},
            ),

            html.Div([
                html.P('Select Country:',className="text"),
            ],),

            html.Div(
                html.Div(
                    dcc.Dropdown(
                        id = "select_country",
                        options = [
                            {"label":country,"value" : country} for country in countries
                            ],
                        multi = False,
                        value = "India",  
                        className= "dcc_comp"
                ) ),
                className= "dropdown"
            ),
                                     
            html.Div(
                dcc.Graph(
                    id='graph', 
                    figure={},
                ),
                className="graph"
            ),

            html.Div([
                html.P('Select Year:',className="text"),
            ],),

            html.Div(
                dcc.Dropdown(
                    id = "select_year",
                    options = [ 
                        {"label":year,"value":year} for year in range(1961,2020)
                        ],
                    multi = False,
                    value = 1993,
                    className= "dcc_comp"
                    ),className="dropdown"
                ),
            
            html.Div(
                dcc.Graph(
                    id='map', 
                    figure={},
                ),className="graph"
            )
    ])



      
      
@app.callback(
    [Output(component_id='map', component_property='figure')],
    Output(component_id='graph', component_property='figure'),
    [
        Input(component_id='select_year', component_property='value'),
        Input(component_id='select_country', component_property='value')
        ]
    
)      


def update_graph(year,country):
   

    # container = "The year chosen by user was: {}".format(year)
    df1 = df.copy()
    df1 = df1[df1["year"] == year]

    # # Plotly Express for map for selected year
    fig = px.choropleth(
        data_frame = df1,
        locations = df1["Country Code"],
        color = 'scaled_temp',
        hover_data = ['Country Name', 'scaled_temp'],
        color_continuous_scale = px.colors.sequential.YlOrRd,
        template = 'plotly_dark'
    )
    
    df2 = df.copy()
    df3 = df2[df2["Country Name"] == country] 
    
    #plotly express for line graphs for selected country
    fig1 = px.line(
        df3, 
        x=df3["year"],
        y=df3["scaled_temp"], 
        color='Country Name'
    )
    
    

    return fig,fig1 




# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

