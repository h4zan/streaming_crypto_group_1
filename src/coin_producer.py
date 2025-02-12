from quixstreams import Application
from connect_api import get_latest_coin_data
import time

def main():
    # Skapa en Quix Streams-applikation och definiera Kafka-topic
    app = Application(broker_address="localhost:9092", consumer_group="coin_group")
    coins_topic = app.topic(name="coins", value_serializer="json")

    # Använd producenten för att skicka data till Kafka
    with app.get_producer() as producer:
        while True:
            # Hämta senaste kryptodata för ETH
            coin_latest = get_latest_coin_data("ETH")

            # Serialiserar meddelandet
            kafka_message = coins_topic.serialize(
                key=coin_latest["symbol"], value=coin_latest
            )

            # Printar logg om vad som har producerats
            print(
                f"Producer: Skickar {kafka_message.key} - Pris: {coin_latest['quote']['SEK']['price']:.2f} Kr"
            )

            # Skickar meddelandet till Kafka topic
            producer.produce(topic=coins_topic.name, key=kafka_message.key, value=kafka_message.value)

            # Väntar 10 sekunder innan nästa meddelande skickas
            time.sleep(30)

if __name__ == "__main__":
    main()