from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import data

json_template = """
    [{
        "measurement": "{0}_{1}_{2}",
        "tags": {
            "name": {0},
            "phase": "{1}",
            "unit": {2}
        },
        "fields" : {
            "value": {3}
        }
    }]
"""

class InfluxDb:
    def __init__(self, conf) -> None:
        url = 'http://{0}:{1}'.format(conf['host'], conf['port'])
        token = InfluxDb._parseEnv(conf['token'])
        self.client = InfluxDBClient(url=url, token=token, org=conf['org'])
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
        self.bucket = conf['bucket']

    def insert(self, name, data: data.SmartMeterMeasurementV):
        for d in data:
            p = Point(f'{name}_{d.phaseLabel}')
            p.tag('name', name)
            p.tag('phase', d.phaseLabel)
            p.field('volt', d.volt)
            p.field('amp', d.amp)
            p.field('pow', d.pow)
            p.field('powFactor', d.powFactor)

            self.write_api.write(bucket=self.bucket, record=p)

    @staticmethod
    def _parseEnv(value):
        values = value.split(':')
        if len(values) == 2 and values[0] == 'env':
            return os.environ[values[1]]
        return value