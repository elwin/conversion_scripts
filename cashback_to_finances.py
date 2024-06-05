#!/usr/bin/env python3
import datetime
import sys

import pandas as pd

mapping = {
    "Buying/Shopping Clubs, Services": "Groceries",
    "Card, Gift And Novelty Stores": "Gifts",
    "Catalog Merchants": "Electronics",
    "Department Stores": "Groceries",
    "Eating Places, Restaurants": "Eating Out",
    "Equipment, Furniture Stores": "Appartment",
    "Fabric, Needlework, And Sewing Stores": "Personal",
    "Grocery Stores, Supermarkets": "Groceries",
    "Miscellaneous Food Stores, Markets": "Groceries",
    "Motor Vehicle Supplies And New Parts": "Transport",
    "Passenger Railways": "Public Transport",
    "Tourists Attractions": "Entertainment",
}

mapping = {k.lower(): v for k, v in mapping.items()}

capturing_keywords = [
    "Spar", "Denner", "Migros", "Coop", "EY"
]

mapping_description = {
    "Gupta-Gastro-Line": "Indian Store Oerlikon",
    "Züri Bistro": "Züri Bistro (Döner)"
}
mapping_description.update({key: key for key in capturing_keywords})

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

    df["category"] = df["category"].str.lower().replace(mapping)
    for from_value, to_value in mapping_description.items():
        df["note"] = df["note"].str.lower().replace(rf'(^.*{from_value.lower()}.*$)', f'{to_value}', regex=True)

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
