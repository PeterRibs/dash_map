import plotly.graph_objects as go
import plotly.express as px

def figure_criation(subset_data, agrupamento):
    colors = ['#c04641', '#00035b', '#008a60', '#942193', '#e56d00', '#bb1133', '#f81404', '#da995f', '#7249d6', '#30ff21', '#46adf9', '#dc41f1', '#feaea5', '#20726a', '#6eb478', '#8b97a5', '#15151c']

    categories = subset_data[agrupamento].unique()

    color_dict = {} # Create a dictionary to store color assignments for each category
    for i, cat in enumerate(categories):
        color_dict[cat] = colors[i % len(colors)]

    fig = px.choropleth_mapbox(center={"lat": -15.7801, "lon": -47.9292},
                            mapbox_style="open-street-map", zoom=5)

    for index, row in subset_data.iterrows():    
        popup_rows = []
        for col in ["Property Name", "Latitude", "Longitude", "Area (hectares)", "Solar Energy", "Number of Cows", "Owner Name", "Veterinarian", "Milk Collection (liters/day)"]:
            popup_rows.append(f"{col}: {row[col]}")
        
        popup_text = "<br>".join(popup_rows) # Join the list of popup rows into a single string separated by <br> tags
        fig.add_trace(
            go.Scattermapbox(
                lat=[row['Latitude']],
                lon=[row['Longitude']],
                mode='markers',
                text= popup_text,
                hoverinfo='text',
                marker_size=25,
                marker_color= color_dict[row[agrupamento]],
                showlegend=False,
            )
        )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(showlegend=False, selector=dict(type='choroplethmapbox'))
    
    return fig
