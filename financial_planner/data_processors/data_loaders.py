import pandas as pd
from financial_planner.data_classes.data_classes import Contributor
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


def main():
    df = read_incomes()
    print(df.head())
    contributors = get_contributors()
    print(contributors)


if __name__ == '__main__':
    main()
