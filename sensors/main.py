import argparse
import json
import schedule
import time

import discovery
import smart_meters
import storage

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTIONS]",
        description="Process sensors data."
    )
    parser.add_argument(
        "-v", "--version", action="version", version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-c", "--sens_cfg", type=str, help="path to sensor configuration file"
    )
    parser.add_argument(
        "-o", "--out_cfg", type=str, help="path to output (data storage) configuration file"
    )
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()

    if args.sens_cfg:
        macDiscovery = discovery.MacDiscovery()
        sensorsConfig = {}
        with open(args.sens_cfg) as f:
            sensorsConfig = json.load(f)

        outConfig = {}
        with open(args.out_cfg) as f:
            outConfig = json.load(f)

        influx = storage.InfluxDb(outConfig['influxdb'])
    
        for emeter in sensorsConfig['emeters']:
            sm = smart_meters.buildSmartMeter(emeter, macDiscovery)
            def do():
                sm.pool()
                print(sm.getData())
                influx.insert(sm.getName(), sm.getData())

            schedule.every(emeter['probe_every_s']).seconds.do(do)
        
    while True:
        schedule.run_pending()
        time.sleep(1)
            
if __name__ == '__main__':
    main()