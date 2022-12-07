from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import data


class ConfigurationError(Exception):
    def __init__(self, *args: object) -> None:
         super().__init__(*args)

class ConnectionFailedError(Exception):
    pass

class InfluxDb:
    def __init__(self, conf) -> None:
        url = 'http://{0}:{1}'.format(conf['host'], conf['port'])
        token = InfluxDb._parseEnv(conf['token'])
        if token is None:
            raise ConfigurationError('Env variable {0} not defined'.format(conf['token']))

        self.client = InfluxDBClient(url=url, token=token, org=conf['org'])
        
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
    
        self.bucket = conf['bucket']

    def insert(self, name, data: data.SmartMeterMeasurementV):
        for d in data:
            p = Point(f'{name}')
            p.tag('type', 'smart_meter')
            p.tag('phase', d.phaseLabel)
            p.field('volt', d.volt)
            p.field('amp', d.amp)
            p.field('pow', d.pow)
            p.field('powFactor', d.powFactor)

            try:
                self.write_api.write(bucket=self.bucket, record=p)
            except Exception as ex:
                raise ConnectionFailedError(ex)

    @staticmethod
    def _parseEnv(value):
        try:
            values = value.split(':')
            if len(values) == 2 and values[0] == 'env':
                return os.environ[values[1]]
            return value
        except KeyError:
            return None