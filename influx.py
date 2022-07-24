import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS


#################################################################
# influx
influx_bucket = 'deribit-1'
client = influxdb_client.InfluxDBClient(
    url=os.getenv('INFLUX_URL'),
    token=os.getenv('INFLUX_TOKEN'),
    org=os.getenv('INFLUX_ORG')
)
write_api = client.write_api(write_options=SYNCHRONOUS)


def get_influx_client():
    return influxdb_client


def get_influx_write_api():
    return write_api
