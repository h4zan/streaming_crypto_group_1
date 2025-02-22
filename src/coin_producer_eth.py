from quixstreams import Application
from connect_api import get_latest_coin_data
import time

def main():
    app = Application(broker_address="localhost:9092", consumer_group="coin_group_eth")
    eth_topic = app.topic(name="eth", value_serializer="json")

    with app.get_producer() as producer:
        while True:

            coin_latest = get_latest_coin_data("ETH")

            kafka_message = eth_topic.serialize(
                key=coin_latest["symbol"], value=coin_latest
            )

            print(
                f"Producer ETH: Sending {kafka_message.key} - Price: €{coin_latest['quote']['EUR']['price']:.2f}"
            )

            producer.produce(topic=eth_topic.name, key=kafka_message.key, value=kafka_message.value)

            time.sleep(30)

if __name__ == "__main__":
    main()