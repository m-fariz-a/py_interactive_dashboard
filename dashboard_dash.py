import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from libs.create_data import create_data

# Create sample data
df = create_data()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("DataFrame Dashboard"),

    # Display DataFrame
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        fixed_rows={'headers': True}, # fix header
        page_size=20,
        style_table={'minWidth': '800px', 'width': '800px', 'maxWidth': '800px',
                    'height': '300px', 'overflowY': 'auto'},
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(245, 245, 245)',
            }
        ],
    ),


])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
