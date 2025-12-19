import math
import requests


def get_tax(income):
    url = "https://webcalc.services.zh.ch/ZH-Web-Calculators/calculators/INCOME_ASSETS/calculate"
    data = {
        "taxYear": "2024",
        "maritalStatus": "single",
        "taxScale": "BASIC",
        "religionP1": "OTHERS",
        "municipality": "261",
        "taxableIncome": income,
        "taxableAssets": 0
    }

    out = requests.post(url, json=data).json()
    staats_steuer = out["cantonalSimpleTax"]["value"]
    gemeinde_steuer = out["municipalityTax"]["value"]

    url = "https://webcalc.services.zh.ch/ZH-Web-Calculators/calculators/FEDERAL/calculate"
    data = {
        "taxYear": "2024",
        "taxScale": "SINGLE",
        "taxableIncome": income
    }

    out = requests.post(url, json=data).json()
    federal_tax = out["totalFederalTax"]["value"]

    return staats_steuer + gemeinde_steuer + federal_tax


def get_incomes(start, roof):
    current = start
    while current <= roof:
        # For 100s, increase 10 (always 1/10th less)
        yield current
        current += 10 ** (int(math.log10(current)) - 1) * 10


def main():
    # incomes = [
    #     6700,
    #     11400,
    #     16100,
    #     23700,
    #     33000,
    #     43700,
    #     56100,
    #     73000,
    #     105500,
    #     137700,
    #     188700,
    #     254900,
    # ]

    print("income,tax")
    for income in get_incomes(5000, 1000000):
        print(f"{income},{get_tax(income)}")


if __name__ == '__main__':
    main()
