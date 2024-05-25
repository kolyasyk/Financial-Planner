from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from financial_planner.data_processors.data_loaders import read_incomes
from financial_planner.data_classes.data_classes import Contributor
from financial_planner.data_processors.data_loaders import get_contributors


class FinancialPlannerDash(Dash):
    def __init__(self, title='My Dashboard', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.contributors = get_contributors()
        self.incomes_df = read_incomes()
        self.layout = self.create_layout()
        self.init_callbacks()

    def create_layout(self):
        list_of_contributors = get_contributors()
        list_of_contributor_divs = [html.Div(children=[dcc.Markdown(f"*{x.name}*\n\n{x.birthday}"), html.Button("Edit", id=f"contributor-edit:{x.name}")]) for x in list_of_contributors]
        return html.Div([
            html.H1(self.title),
            html.Div(id='output-text', children='waiting for input...'),
            dash_table.DataTable(
                self.incomes_df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in self.incomes_df.columns],
            ),
            *list_of_contributor_divs
        ])

    def init_callbacks(self):
        for contributor in get_contributors():
            @self.callback(
                Output(component_id='output-text', component_property='children', allow_duplicate=True),
                Input(component_id=f"contributor-edit:{contributor.name}", component_property="n_clicks"),
                prevent_initial_call=True
            )
            def update_output(_, editing_contributor=contributor):
                return f"Editing: {editing_contributor.name}"

