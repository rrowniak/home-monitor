import argparse
import json
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]",
        description="Calculate power usage in given time frame"
    )
    parser.add_argument(
        "-v", "--version", action="version", version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-o", "--out_cfg", type=str, help="path to output (data storage) configuration file"
    )
    parser.add_argument(
        "-f", "--fromT", type=str, help="take data for calculations <from>"
    )
    parser.add_argument(
        "-t", "--toT", type=str, help="take data for calculations <to>"
    )
    return parser


def parseEnv(value):
    try:
        values = value.split(':')
        if len(values) == 2 and values[0] == 'env':
            return os.environ[values[1]]
        return value
    except KeyError:
        return None

def main():
    parser = init_argparse()
    args = parser.parse_args()

    outConfig = {}
    with open(args.out_cfg) as f:
        outConfig = json.load(f)

    # connect influx database
    conf = outConfig['influxdb']
    url = 'http://{0}:{1}'.format(conf['host'], conf['port'])
    token = parseEnv(conf['token'])
    if token is None:
        print('Env variable {0} not defined'.format(conf['token']))
        exit(0)

    db = InfluxDBClient(url=url, token=token, org=conf['org'])
    query_api = db.query_api()
    
    bucket = conf['bucket']

    q = f'''
    from(bucket: "{bucket}")
  |> range(start: -{args.fromT})
  |> filter(fn: (r) => r["_measurement"] == "wejscie_siec")
  |> filter(fn: (r) => r["_field"] == "pow")
  |> filter(fn: (r) => r["phase"] == "A" or r["phase"] == "B" or r["phase"] == "C")
  |> aggregateWindow(every: 30s, fn: mean, createEmpty: false)
  |> yield(name: "mean")
    '''
    # read data
    tables = query_api.query(q)

    consumed = {}
    produced = {}
    for table in tables:
        for row in table.records:
            #print (row.values)
            phase = row['phase']
            wh = row['_value'] / 120
            if wh > 0:
                if phase not in produced.keys():
                    produced[phase] = 0
                produced[phase] = produced[phase] + wh
            else:
                if phase not in consumed.keys():
                    consumed[phase] = 0
                consumed[phase] = consumed[phase] + wh
    cons = (consumed['A'] + consumed['B'] + consumed['C']) / 1000
    prod = (produced['A'] + produced['B'] + produced['C']) / 1000
    print(f'Consumed = {cons:.3f} kWh ==> {consumed}')
    print(f'Produced = {prod:.3f} kWh ==> {produced}')
    tot = cons + prod / 2
    cost = cons * 0.7 + prod * 0.4
    print(f'Total balance = {tot:.3f} kWh, cost = {cost:.1f} PLN')

if __name__ == '__main__':
    main()