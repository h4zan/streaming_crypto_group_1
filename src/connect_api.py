from constants import COINMARKET_API
from requests import Session, RequestException
import json
import pprint


def get_latest_coin_data(symbol="ETH", endpoint="quotes"):

    base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/"

    api_endpoints = {
        "quotes": f"{base_url}quotes/latest",
        "listings": f"{base_url}listings/latest",
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    parameters = {"convert": "EUR"}

    endpoint_params = {
        "quotes": {"symbol": symbol},
        "listings": {"start": "1", "limit": "2"},
    }

    parameters.update(endpoint_params[endpoint])

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(api_endpoints[endpoint], params=parameters)
        data = json.loads(response.text)["data"]

        return data.get(symbol, None)

    except RequestException as e:
        pprint.pprint(f"An error occurred: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected API response structure: {e}")
