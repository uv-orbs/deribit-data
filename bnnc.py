
from influxdb_client.client.write_api import SYNCHRONOUS
from binance import AsyncClient, BinanceSocketManager
import os
import asyncio
from influx import get_influx_client, get_influx_write_api

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SEC')


def send_data_point(price):
    p = get_influx_client().db_client.Point("spot").tag(
        "version", "dev1.1").tag("exchange", "binance").tag("pair", "BTCUSDT")

    p.field("price", price)
    res = get_influx_write_api().write(
        bucket='deribit-1', org='Orbs', record=p)


async def main():
    last_price = 1
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket('BTCUSDT')
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            price = float(res['p'])
            if abs(price / last_price - 1) > .0001:
                print(price)
                last_price = price
                send_data_point(price)

    await client.close_connection()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
