from quixstreams import Application
from connect_api import get_latest_coin_data, get_topic
import time

def main():
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    sol_topic = get_topic("SOL")

    with app.get_producer() as producer:
        while True:

            coin_latest = get_latest_coin_data("SOL")

            kafka_message = sol_topic.serialize(
                key=coin_latest["symbol"], value=coin_latest
            )

            print(
                f"Producer SOL: Skickar {kafka_message.key} - Pris: {coin_latest['quote']['SEK']['price']:.2f} Kr"
            )

            producer.produce(topic=sol_topic.name, key=kafka_message.key, value=kafka_message.value)

            time.sleep(30)

if __name__ == "__main__":
    main()