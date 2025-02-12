import pprint
from quixstreams import Application
from constants import COINMARKET_API
from requests import Session, RequestException

import json

app = Application(
    broker_address="localhost:9092",
    consumer_group="coin_group",
)

coins_topic = app.topic(name="coins", value_serializer="json")


def get_latest_coin_data(symbols="ETH", endpoint="quotes"):

    base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/"

    api_endpoints = {
        "quotes": f"{base_url}quotes/latest",
        "listings": f"{base_url}listings/latest",
    }

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    parameters = {"convert": "SEK"}

    endpoint_params = {
        "quotes": {"symbol": symbols},
        "listings": {"start": "1", "limit": "10"},
    }

    parameters.update(endpoint_params[endpoint])

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(api_endpoints[endpoint], params=parameters)
        data = json.loads(response.text)["data"]
        return data
    except RequestException as e:
        pprint.pprint(f"An error occurred: {e}")
        return None
    except KeyError as e:
        print(f"Unexpected API response structure: {e}")
