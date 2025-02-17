from quixstreams import Application
from connect_api import get_latest_coin_data, get_topic
import time

def main():
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    eth_topic = get_topic("ETH")

    with app.get_producer() as producer:
        while True:

            coin_latest = get_latest_coin_data("ETH")

            kafka_message = eth_topic.serialize(
                key=coin_latest["symbol"], value=coin_latest
            )

            print(
                f"Producer ETH: Sending {kafka_message.key} - Price: {coin_latest['quote']['SEK']['price']:.2f} Kr"
            )

            producer.produce(topic=eth_topic.name, key=kafka_message.key, value=kafka_message.value)

            time.sleep(30)

if __name__ == "__main__":
    main()