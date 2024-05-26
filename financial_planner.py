from financial_planner.financial_planner_dash.financial_planner_dash import FinancialPlannerDash
import dash_bootstrap_components as dbc


def main():
    app = FinancialPlannerDash(
        title='Financial Planner',
        external_stylesheets=[dbc.themes.SANDSTONE, dbc.icons.FONT_AWESOME],
    )
    app.config.external_stylesheets = [dbc.themes.SANDSTONE]
    app.run_server(debug=True, port=80, host='192.168.8.48')


if __name__ == '__main__':
    main()
