from dash import Dash, html, dcc, dash_table, callback_context
import dash_bootstrap_components as dbc
from datetime import datetime
from dash.dependencies import Input, Output, State, MATCH, ALL
import plotly.graph_objs as go
import json

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
    def get_account_cards(accounts: [Account]) -> [dbc.Card]:
        return [account.get_account_card() for account in accounts]

    def create_layout(self):
        return dbc.Container(html.Div([
            Account.get_new_account_modal_form(),
            html.H1(self.title),
            dbc.Row([
                dbc.Col([
                    dbc.CardGroup(
                        self.get_account_cards([x for x in self.accounts.values()]),
                        style={"margin": "10px"},
                    ),
                    dbc.Button("Add New Account", id='add-account')],
                    id="account-cards",
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
            prevent_initial_call=True,
        )
        def update_account_selection(switch_ids, values):
            for switch_id, value in zip(switch_ids, values):
                self.accounts[switch_id['id']].enabled = value
            years, totals = self.calculate_accounts_total()
            self.fig = go.Figure(data=[go.Scatter(x=years, y=totals)])
            return self.fig

        @self.callback(
            Output("main-graph", "figure", allow_duplicate=True),
            Output("account-cards", "children", allow_duplicate=True),
            [Input({'type': 'delete-account', 'id': ALL}, "id")],
            [Input({'type': 'delete-account', 'id': ALL}, "n_clicks")],
            prevent_initial_call=True,
        )
        def delete_account(switch_ids, values):
            ctx = callback_context
            if not ctx.triggered:
                button_id = 'None'
            else:
                account_name = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])["id"].split(":")[1]
                if account_name in self.accounts:
                    del self.accounts[account_name]
            years, totals = self.calculate_accounts_total()
            self.fig = go.Figure(data=[go.Scatter(x=years, y=totals)])
            return self.fig, self.get_account_cards([x for x in self.accounts.values()])

        @self.callback(
            Output("add-account-modal", "is_open"),
            [Input("add-account", "n_clicks"), Input("close", "n_clicks")],
            [State("add-account-modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open
