from financial_planner_dash.financial_planner_dash import FinancialPlannerDash


def main():
    app = FinancialPlannerDash(title='Financial Planner')
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
