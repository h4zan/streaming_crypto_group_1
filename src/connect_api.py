from quixstreams import Application
from constants import COINMARKET_API
from requests import Session
import json

app = Application(
    broker_address="localhost:9092",
    consumer_group="coin_group",
)

coins_topic = app.topic(name="coins", value_serializer="json")


def get_latest_coin_data(symbol="ETH"):
    api_url_quotes = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    api_url_listings = (
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    )

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKET_API,
    }

    parameters = {
        "symbol": symbol,
        "convert": "SEK",
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(api_url_quotes, params=parameters)
    return json.loads(response.text)["data"][symbol]
