from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.graph_objs as go

from financial_planner.data_processors.data_loaders import read_incomes
from financial_planner.data_classes.contributor import Contributor
from financial_planner.data_classes.account import Account
from financial_planner.data_processors.data_loaders import get_contributors
from financial_planner.data_processors.data_loaders import get_accounts


class FinancialPlannerDash(Dash):
    def __init__(self, title='My Dashboard', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        # self.contributors: {str: Contributor} = get_contributors()
        self.accounts: {str: Account} = get_accounts()
        years, totals = self.calculate_accounts_total()
        self.fig = go.Figure(data=[go.Scatter(x=years, y=totals)])
        # self.incomes_df = read_incomes()
        self.layout = self.create_layout()
        self.init_callbacks()

    def calculate_accounts_total(self) -> ([float], [float]):
        years = [x for x in range(0, 50)]
        total = [0] * 50
        for account in self.accounts.values():
            if account.enabled:
                for year in years:
                    total[year] += account.start_amount * (1 + account.gain_rate) ** year
        return years, total

    @staticmethod
    def get_account_card(account: Account) -> html.Div:
        return html.Div(dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        html.H4(account.name, className="card-title", style={"display": "inline-block"}),
                        dbc.Switch(
                            id={'type': 'account-selection', 'id': account.name},
                            label="",
                            value=account.enabled,
                            className="float-right",
                            style={"display": "inline-block", "float": "right"},
                        ),
                    ]),
                    html.I(f"Start Date: {account.start_date.strftime('%m/%m/%Y')}"),
                    html.Br(),
                    html.I(f"Start Amount: ${account.start_amount:,.2f}"),
                    html.Br(),
                    html.I(f"Gain Rate: {account.gain_rate * 100:.2f}%"),
                    html.Br(),
                    dbc.Button("Delete", id={'type': 'delete-account', 'id': account.name})
                ]
            ),
            style={"width": "20rem"},
        ),
        className="mb-3")

    @staticmethod
    def get_account_cards(accounts: [Account]) -> html.Div:
        return html.Div([FinancialPlannerDash.get_account_card(account) for account in accounts])

    def create_layout(self):
        return dbc.Container(html.Div([
            html.H1(self.title),
            dbc.Row([
                dbc.Col(
                    self.get_account_cards([x for x in self.accounts.values()]),
                ),
                dbc.Col([
                    dcc.Graph(id="main-graph", figure=self.fig)
                ]),
            ]),
            html.Div(id='output-text', children='waiting for input...'),
        ],
        ), className="mt-5")

    def init_callbacks(self):
        @self.callback(
            Output("main-graph", "figure", allow_duplicate=True),
            [Input({'type': 'account-selection', 'id': ALL}, "id")],
            [Input({'type': 'account-selection', 'id': ALL}, "value")],
            prevent_initial_call = True,
        )
        def update_account_selection(switch_ids, values):
            for switch_id, value in zip(switch_ids, values):
                self.accounts[switch_id['id']].enabled = value
            years, totals = self.calculate_accounts_total()
            self.fig = go.Figure(data=[go.Scatter(x=years, y=totals)])
            return self.fig

        @self.callback(
            Output("output-text", "children", allow_duplicate=True),
            Output("main-graph", "figure", allow_duplicate=True),
            [Input({'type': 'delete-account', 'id': ALL}, "id")],
            [Input({'type': 'delete-account', 'id': ALL}, "active")],
            prevent_initial_call=True,
        )
        def delete_account(switch_ids, values):
            for switch_id, value in zip(switch_ids, values):
                self.accounts[switch_id['id']].enabled = value
            years, totals = self.calculate_accounts_total()
            self.fig = go.Figure(data=[go.Scatter(x=years, y=totals)])
            return f"ids: {switch_ids}, values: {values}", self.fig
