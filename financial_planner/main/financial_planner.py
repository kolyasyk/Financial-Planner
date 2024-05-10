# Import Dash and its components
import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
import yaml
import numpy as np
import pandas as pd
from dataclasses import dataclass


import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

# Sample data to populate the table
data = pd.DataFrame({
    "ID": ["Spouse 1", "Spouse 2"],
    "Base Salary": [10_0000, 120_000],
    "Bonus": [20_000, 24_000],
    "Stocks": [50_000, 60_000],
    "401k Contribution": [23_000, 23_000],
    "Investment": [0.05, 0.05],
    "Start Date": [np.datetime64("2024-01-01"), np.datetime64("2024-01-01")],
    "End Year": [np.datetime64("2044-01-01"), np.datetime64("2044-01-01")],
})

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Button("Add Row", id="adding-row-btn", n_clicks=0),
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            [{'id': 'ID', 'name': 'ID', 'type': 'text'}] +
            [{'id': p, 'name': p, 'type': 'text'} for p in data.columns if p != "ID"]
        ),
        data=data.to_dict('records'),
        editable=True,              # Allow cell editing
        row_deletable=True          # Allow row deleting
    ),
    html.Button("Save Changes", id="save-changes-btn", n_clicks=0),
    html.Div(id='save-output')   # This Div will be used to display save messages
])
# Callback to add a new row
@app.callback(
    Output('table-editing-simple', 'data'),
    [Input('adding-row-btn', 'n_clicks')],
    [State('table-editing-simple', 'data'),
     State('table-editing-simple', 'columns')],
    prevent_initial_call=True)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

# Callback to save data or implement other logic
@app.callback(
    Output('save-output', 'children'),
    [Input('save-changes-btn', 'n_clicks')],
    [State('table-editing-simple', 'data')],
    prevent_initial_call=True)

def save_changes(n_clicks, rows):
    # Here you can add code to save the data to a database or perform other operations
    return f"Data saved: {n_clicks} times!"


if __name__ == '__main__':
    app.run_server(debug=True)

# @dataclass
# class YearlyData:
#     year: int
#     savings: float
#
#
# YEARS = 25
# INTEREST_RATE = 0.05
# CURRENT_SAVINGS = 400_000 * 2
# ANNUAL_CONTRIBUTION = 23_000 * 4
#
# if __name__ == '__main__':
#     # Create a Dash application
#     app = dash.Dash(__name__)
#
#     # Assume you have some data to plot (e.g., a simple DataFrame)
#
#     years: [YearlyData] = [
#         YearlyData(2024, CURRENT_SAVINGS),
#     ]
#
#     for x in range(1, YEARS):
#         years.append(YearlyData(2024 + x, years[x - 1].savings * (1 + INTEREST_RATE) + ANNUAL_CONTRIBUTION))
#
#     df = pd.DataFrame([{'Year': year.year, 'Savings': year.savings} for year in years])
#     # df2 = pd.DataFrame([{'Year': year.year - 1981, 'Savings': year.savings} for year in years])
#
#     year_list = df['Year'].tolist()
#     age_list = [year - 1981 for year in year_list]
#
#
#
#
#     # Create a Plotly Express chart
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df['Year'], y=df['Savings'], mode='lines+markers', name='Savings'))
#
#     fig.update_layout(    title="Savings vs Year with Age as Secondary X-axis",
#     xaxis_title="Year",
#     yaxis_title="Savings ($)",
#     xaxis=dict(
#         domain=[0.1, 0.95]
#     ),
#     xaxis2=dict(
#         overlaying='x',
#         side='top',
#         tickmode='array',
#         tickvals=year_list,
#         ticktext=age_list,
#         title="Age"
#     ))
#
#
#     # Define the layout of your app
#     app.layout = html.Div(children=[
#         html.H1(children='Hello Dash'),
#         html.Div(children='''Dash: A web application framework for Python.'''),
#         dcc.Graph(
#             id='example-graph',
#             figure=fig
#         )
#     ])
#
#     app.run_server(debug=True)