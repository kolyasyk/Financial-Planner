#  modified from
# https://stackoverflow.com/questions/33743273/multiple-x-axes-in-plotly
#  run using
#   python wvw_callback.py

import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)

trace1 = {
      'x': ["2019-01-10", "2019-02-10", "2019-03-10", "2019-04-10", "2019-05-10", "2019-06-10"],
      'y': [40, 50, 60, 30, 40, 50],
      'name': 'xaxis data',
      'type': 'scatter'
}

trace2 = {
      'x': ["2011-01-10", "2011-02-10", "2011-03-10", "2011-04-10", "2011-05-10", "2011-06-10"],
      'y': [4, 25, 6, 30, 20, 10],
      'name': 'xaxis2 data',
      'xaxis': 'x2',
      'type': 'scatter'
}

data_list = [trace1, trace2]

app.layout = html.Div([html.H1('Dash Demo Graph A',
                               style={
                                      'textAlign': 'center',
                                      "background": "yellow"}),
                        dcc.Graph(id="graph1",
                              figure={
                                    'data': data_list,
                                    'layout': {
                                          'yaxis': {'title': 'yaxis title'},
                                          'xaxis2': {
                                                'title': 'xaxis2 title',
                                                'titlefont': {'color': 'rgb(148, 103, 189)'},
                                                'tickfont':  {'color': 'rgb(148, 103, 189)'},
                                                'overlaying': 'x',
                                                'side': 'top'
                                                    }
                                            }
                                    }
                                )
                            ]
                            )


if __name__ == '__main__':
    app.run_server(debug=True)
