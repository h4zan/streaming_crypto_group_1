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
# extract cryptodata collected by coin_producer.py
    latest_quote = message["quote"]["SEK"]
    return {
        "coin": message["name"],
        "price_sek": latest_quote["price"],
        "volume": latest_quote["volume_24h"],
        "updated": message["last_updated"]
    }

def create_postgres_sink():
# create connection to PostgresSQL to save crypyodata in Postgres sink
    sink = PostgreSQLSink(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DBNAME,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        table_name="ethereum",
        schema_auto_update=True
    )
    return sink

def main():
# extract data from Kafka "coins" topic and store in Postgres sink
    app = Application(
        broker_address="localhost:9092",
        consumer_group="coin_group",
        auto_offset_reset="earliest",
    )

    # connection to "coins" topic in Kafka
    coins_topic = app.topic(name="coins", value_deserializer="json")

    # creating streaming-datafram from Kafka topic
    sdf = app.dataframe(topic=coins_topic)

    # extract data and show in terminal
    sdf = sdf.apply(extract_coin_data)
    sdf.update(lambda coin_data: print(f"Consumer: {coin_data}"))

    # saving cryptodata to PostgresSQL
    postgres_sink = create_postgres_sink()
    sdf.sink(postgres_sink)

    # run program
    app.run()

if __name__ == "__main__":
    main()