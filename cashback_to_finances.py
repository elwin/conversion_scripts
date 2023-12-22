#!/usr/bin/env python3
import datetime
import sys

import pandas as pd


def main():
    args = sys.argv
    if len(args) != 2:
        print("Must specify file name")
        exit(1)

    df = pd.read_csv(args[1])

    renaming_columns = {
        "Transaction date": "date",
        "Amount": "amount",
        "Description": "note",
        "Category": "category",
    }

    df = df[renaming_columns.keys()]
    df.rename(
        inplace=True,
        columns=renaming_columns,
    )
    df["date"] = pd.to_datetime(df["date"], dayfirst=True).map(lambda x: x.isoformat())

    df["account"] = "Personal"
    df["note"] = df["note"].map(lambda x: x.title())
    df["category"] = df["category"].astype(str).map(lambda x: x.title())
    df["amount"] *= -1

    print(df.to_csv(
        index=False,
    ))


if __name__ == '__main__':
    main()
