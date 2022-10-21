import asyncio
import logging
import json
from typing import List, Union
from kafka3 import KafkaProducer
import websockets

BITSTAMP_URL = "https://www.bitstamp.net/s/webapp/examples/live_orders_v2.html"
CHANNEL = "live_orders_btcusd"
SUBSCRIPTION_JSON = json.dumps({
    "event": "bts:subscribe",
    "data": {
        "channel": CHANNEL
    }
})
BITSTAMP_WS_URL = "wss://ws.bitstamp.net/"
KAFKA_URL = "kafka:9092"

logging.basicConfig(level=logging.DEBUG)


def create_producer(servers: Union[List[str], str] = None) -> KafkaProducer:
    """ return istance of a kafkaproducer, with standard server address.
    To override starndard url or pass multiple servers,
     use the argument `servers`"""
    boot_servers = servers if servers else "localhost:9092"
    return KafkaProducer(bootstrap_servers=boot_servers)


async def main():
    """ Connect to Bitstamp web-socket and get the stream"""
    logging.debug("Connecting to message broker.")
    producer = create_producer(KAFKA_URL)
    logging.debug("Kafka connected")
    async with websockets.connect(BITSTAMP_WS_URL) as stream:
        await stream.send(SUBSCRIPTION_JSON)
        while True:
            event = await stream.recv()
            logging.debug(f"Received event from websocket: {event}")
            logging.debug("Sending received event")
            producer.send(
                topic="bitstamp",
                value=event,
            )
            logging.debug(f"Event sent to kafka successfully!")

if __name__ == "__main__":
    asyncio.run(main())
