import asyncio
import websockets
import json
import influxdb_client
import os
from influxdb_client.client.write_api import SYNCHRONOUS
from collections.abc import MutableMapping
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()

#################################################################
# influx
influx_bucket = 'deribit-1'
client = influxdb_client.InfluxDBClient(
    url=os.getenv('INFLUX_URL'),
    token=os.getenv('INFLUX_TOKEN'),
    org=os.getenv('INFLUX_ORG')
)
write_api = client.write_api(write_options=SYNCHRONOUS)

# get tomorrow
dt = datetime.now() + timedelta(days=1)
tom = dt.strftime("%d%b%y").upper()

# 21JUL22
# get strike
strike = int(os.getenv('STRIKE'))
#################################################################
chans = [
    f'ticker.BTC-{tom}-{strike}-C.100ms',
    f'ticker.BTC-{tom}-{strike}-P.100ms',
]
msgSub = \
    {
        "jsonrpc": "2.0",
        "id": 3600,
        "method": "public/subscribe",
        "params": {
            "channels": chans
        }
    }


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def create_data_point(data):
    p = influxdb_client.Point("options").tag("version", "dev1.1")
    flat = flatten_dict(data)
    for f in flat:
        if isinstance(flat[f], str):
            p = p.tag(f, flat[f])
        elif type(flat[f]) == int or type(flat[f]) == float:
            p = p.field(f, flat[f])

    return p


def write_data(j):
    params = j['params']
    if params is None:
        return
    channel = params['channel']
    if channel is None or channel not in chans:
        return
    data = params['data']
    if data is None:
        return

    p = create_data_point(data)
    res = write_api.write(
        bucket='deribit-1', org='Orbs', record=p)

    if(res):
        print(res)

    print(data['instrument_name'], data['underlying_price'])


async def call_api(msg):
    async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
        await websocket.send(msg)
        while websocket.open:
            response = await websocket.recv()
            # do something with the response...
            # print(response)
            j = json.loads(response)
            try:
                write_data(j)
            except Exception as e:
                print('Exception:', e)

asyncio.get_event_loop().run_until_complete(call_api(json.dumps(msgSub)))
