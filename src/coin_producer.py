from quixstreams import Application
from connect_api import get_latest_coin_data
import time

def main():
    # creating Quixstreams application and defining Kafka topic
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    coins_topic = app.topic(name="coins", value_serializer="json")

    # using producer to send cryptodata to Kafka
    with app.get_producer() as producer:
        while True:
            # collecting latest cryptodata for Ethereum
            coin_latest = get_latest_coin_data("ETH")

            # serializing Kafka message
            kafka_message = coins_topic.serialize(
                key=coin_latest["symbol"], value=coin_latest
            )

            # prints log on what's been produced
            print(
                f"Producer: Skickar {kafka_message.key} - Pris: {coin_latest['quote']['SEK']['price']:.2f} Kr"
            )

            # sends message to Kafka topic
            producer.produce(topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value)

            # waits 30 sec until sending next message
            time.sleep(30)

if __name__ == "__main__":
    main()