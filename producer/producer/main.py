import asyncio
import json
from typing import Callable, List, Union
from kafka3 import KafkaProducer
# import requests
import websockets

BITSTAMP_URL = "https://www.bitstamp.net/s/webapp/examples/live_orders_v2.html"
CHANNEL = "live_orders_v2"
SUBSCRIPTION_JSON = json.dumps({
    "event": {"bts": "subscribe"},
    "data": {
        "channel": CHANNEL
    }
})
BITSTAMP_WS_URL = "wss://ws.bitstamp.net/"


def create_producer(servers: Union[List[str], str] = None) -> KafkaProducer:
    """ Return istance of a KafkaProducer, with standard server address.
    To override starndard url or pass multiple servers, use the argument `servers`"""
    boot_servers = servers if servers else "localhost:9092"
    return KafkaProducer(bootstrap_servers=boot_servers)


async def get_order_stream():
    """ Connect to Bitstamp web-socket and get the stream"""
    async with websockets.connect(BITSTAMP_WS_URL) as wbs:
        await wbs.send(SUBSCRIPTION_JSON)
        res = await wbs.recv()
        return res


async def timed_execution(func: Callable, time: int):
    """ Run an async `func` for `time` seconds. """
    await asyncio.sleep(time)
    result = await asyncio.get_event_loop().run_in_executor(None, func)
    return result


async def main():
    # res = requests.get(BITSTAMP_URL)
    # print(res.text)
    # print(json.dumps(res.json()))
    stream = asyncio.get_event_loop()\
        .run_until_complete(
        timed_execution(get_order_stream, 30))
    print(stream)

if __name__ == "__main__":
    main()
