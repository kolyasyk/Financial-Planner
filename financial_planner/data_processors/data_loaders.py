import pandas as pd
from financial_planner.data_classes.contributor import Contributor
from financial_planner.data_classes.account import Account
from datetime import datetime

INCOME_DATA_PATH = 'data/incomes.csv'


def read_incomes() -> pd.DataFrame:
    df = pd.read_csv(INCOME_DATA_PATH)
    return df


def get_contributors() -> list[Contributor]:
    return [
        Contributor('Alice', datetime(year=1990, month=1, day=1), 65),
        Contributor('Bob', datetime(year=1990, month=1, day=1), 65),
    ]


def get_accounts() -> dict[str: Account]:
    account_list = [
        Account('Qorvo 401K', datetime(year=1990, month=1, day=1), 400_000.0),
        Account('Mnemonics 401K', datetime(year=1990, month=1, day=1), 50_000.0),
    ]
    return {account.name: account for account in account_list}


def main():
    df = read_incomes()
    print(df.head())
    contributors = get_contributors()
    print(contributors)
    accounts = get_accounts()
    print(accounts)


if __name__ == '__main__':
    main()
