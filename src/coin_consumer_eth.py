from quixstreams import Application
from constants import (
    POSTGRES_DBNAME,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)
from quixstreams.sinks.community.postgresql import PostgreSQLSink


def extract_coin_data(message):

    latest_quote = message["quote"]["EUR"]
    return {
        "coin": message["name"],
        "price_eur": latest_quote["price"],
        "volume_24h": latest_quote["volume_24h"],
        "market_cap": latest_quote["market_cap"],
        "percent_change_24h": latest_quote["percent_change_24h"],
        "percent_change_30d": latest_quote["percent_change_30d"],
        "updated": latest_quote["last_updated"],
    }


def create_postgres_sink():

    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="ethereum",
        schema_auto_update=True,
    )
    return sink


def main():

    app = Application(
        broker_address="localhost:9092",
        consumer_group="coin_group_eth",
        auto_offset_reset="earliest",
    )

    eth_topic = app.topic(name="eth", value_deserializer="json")

    sdf = app.dataframe(topic=eth_topic)

    sdf = sdf.apply(extract_coin_data)
    sdf.update(lambda coin_data: print(f"Consumer ETH: {coin_data}"))

    postgres_sink = create_postgres_sink()
    sdf.sink(postgres_sink)

    app.run()


if __name__ == "__main__":
    main()
