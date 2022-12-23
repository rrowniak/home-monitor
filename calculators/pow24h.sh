#!/bin/bash

. ../sensors/.credentials

python3 ./power_consumtion.py -o ../sensors/cfg/output.cfg.json -f 24h

# while true; do ./pow24h.sh; sleep 30; done