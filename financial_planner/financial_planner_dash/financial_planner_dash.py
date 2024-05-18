from dash import Dash, html, dcc
from dash.dependencies import Input, Output


class FinancialPlannerDash(Dash):
    def __init__(self, title='My Dashboard', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.layout = self.create_layout()
        self.init_callbacks()

    def create_layout(self):
        return html.Div([
            html.H1(self.title),
            dcc.Input(id='input-text', type='text', value=''),
            html.Div(id='output-text')
        ])

    def init_callbacks(self):
        @self.callback(
            Output('output-text', 'children'),
            Input('input-text', 'value')
        )
        def update_output(value):
            return f'You have entered: {value}'
