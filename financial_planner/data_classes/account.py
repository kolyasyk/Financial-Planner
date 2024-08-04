from dataclasses import dataclass
from datetime import datetime
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from datetime import date


@dataclass
class Account:
    name: str
    start_date: datetime
    start_amount: float = 0.0
    gain_rate: float = 0.02
    enabled: bool = True

    def get_account_card(self) -> dbc.Card:
        return dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                        html.H4(self.name, className="card-title", style={"display": "inline-block"}),
                        dbc.Switch(
                            id={'type': 'account-selection', 'id': self.name},
                            label="",
                            value=self.enabled,
                            className="float-right",
                            style={"display": "inline-block", "float": "right"},
                        ),
                    ]),
                    html.I(f"Start Date: {self.start_date.strftime('%m/%m/%Y')}"),
                    html.Br(),
                    html.I(f"Start Amount: ${self.start_amount:,.2f}"),
                    html.Br(),
                    html.I(f"Gain Rate: {self.gain_rate * 100:.2f}%"),
                    html.Br(),
                    dbc.Button("Delete", id={'type': 'delete-account', 'id': f'delete-account:{self.name}'})
                ]
            ),
            style={"width": "20rem"},
        )

    @staticmethod
    def get_new_account_modal_form():
        name_input = html.Div(
            [
                dbc.Label("Account Name"),
                dbc.Input(id="new-account-name", placeholder="New account name"),
                dbc.FormText("Keep under 30 characters", color="secondary"),
            ], className="mb-3")
        start_date_input = html.Div(
            [
                dbc.Label("Start Date", html_for="example-account-start-date"),
                dcc.DatePickerSingle(
                    id='new-account-start-date',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2017, 9, 19),
                    initial_visible_month=date(2017, 8, 5),
                    date=date(2017, 8, 25)
                ),
            ], className="mb-3",
        )
        start_amount_input = html.Div(
            [
                dbc.Label("Starting Amount [$USD]"),
                dbc.Input(id="new-account-start-amount", placeholder="0.00"),
            ], className="mb-3")
        gain_input = html.Div(
            [
                dbc.Label("Account Fain [%]"),
                dbc.Input(id="new-account-gain", placeholder="0.0"),
            ], className="mb-3")
        return dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Add Another Account")),
                dbc.ModalBody([name_input, start_date_input, start_amount_input, gain_input]),
                dbc.ModalFooter(
                    dbc.Row([
                        dbc.Col(dbc.Button("Add", id="add-account", className="ms-auto", n_clicks=0)),
                        dbc.Col(dbc.Button("Cancel", id="close", className="ms-auto", n_clicks=0))
                        ], className="mt-3")
                    )
            ],
            id="add-account-modal",
            is_open=False,
        )
