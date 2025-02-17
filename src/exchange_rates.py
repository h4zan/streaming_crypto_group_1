import pprint
from constants import EXCHANGE_RATE_API
from requests import Session
import json

CURRENCIES = {"EUR": 0.95, "SEK": 10.70, "NOK": 11.10, "DKK": 7.10}

def get_exchange_rates():

    convertion_api = f"http://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_RATE_API}&symbols=SEK,NOK,DKK,ISK,EUR"

    session = Session()
    response = session.get(convertion_api)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data["rates"]
    else:
        print(f"Error fetching exchange rates: {response.status_code}")
        return None


def convert_currency(amount_to_convert, target_currency, exchange_rates):
    if target_currency not in exchange_rates:
        print(f"Error: {target_currency} rate not available.")
        return None
    else:
        return amount_to_convert * exchange_rates[target_currency]


def convert_all_quotes(coin_data, target_currency, exchange_rates):
    if target_currency not in coin_data["quote"]:
        coin_data["quote"][target_currency] = {}

    for currency, quote_data in coin_data["quote"].items():
        if currency == target_currency:
            continue

        for field in [
            "price",
            "market_cap",
            "volume_24h",
            "volume_change_24h",
            "percent_change_24h",
            "market_cap",
        ]:
            if field in quote_data:
                original_value = quote_data[field]
                converted_value = convert_currency(
                    original_value, target_currency, exchange_rates
                )
                coin_data["quote"][target_currency][field] = converted_value

    return coin_data
