# Home Monitor project

This is Home Monitor project. The main purpose this software is to gather, interpret and store various information coming from different sensors.
Gathered and stored data will be used for further analysis and energy consumption optimization.

![Power consumption example](/doc/screen1.jpg)


## Architecture

![Power consumption example](/doc/architecture.png)

## Sensors
This module is responsible for gathering data from configured sensors and then the data is stored in specified data source like InfluxDB for further analysis.
In order to run the module execute the following commands:
```
$ cd sensors
$ python3 ./main.py -c ./cfg/sensors.cfg.json -o
```
## Requirements
Required Python modules are listed in [requirements.txt](sensors/requirements.txt).
System requirements:
- `fping` for discovering devices in the local area network using MAC addresses
`$ sudo apt install fping`
### Supported sensors 
- Smart meter Shelly EM3