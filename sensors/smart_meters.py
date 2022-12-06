import requests
import data

class SmartMeter:
    def pool(self):
        raise NotImplementedError()

    def getData(self) -> data.SmartMeterMeasurementV:
        raise NotImplementedError()

    def getName(self) -> str:
        raise NotImplementedError()

def buildSmartMeter(cfg, macDisc) -> SmartMeter:
    if cfg['type'] == 'Shelly3EM':
        ip = macDisc.getIpFromMac(cfg['mac'])
        return Shelly3EM(ip, cfg['name'])

class Shelly3EM(SmartMeter):
    def __init__(self, dest, name) -> None:
        super().__init__()
        self.devDest = dest
        self.url = f"http://{self.devDest}/status"
        self.json_response = None
        self.name = name
    # SmartMeter methods
    def pool(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.json_response = response.json()
        else:
            self.json_response = None

    def getData(self) -> data.SmartMeterMeasurementV:
        if self.json_response is None:
            return None
        ret = []
        for z in zip([0, 1, 2], ['A', 'B', 'C']):
            i = z[0]
            d = data.SmartMeterMeasurement(
                self.json_response["emeters"][i]["voltage"],
                self.json_response["emeters"][i]["current"],
                self.json_response["emeters"][i]["power"],
                self.json_response["emeters"][i]["pf"],
                z[1]
            )
            ret.append(d)
        return ret
    
    def getName(self) -> str:
        return self.name

class Afore(SmartMeter):
    def __init__(self) -> None:
        super().__init__()
        # curl 192.170.8.108/status.html -u "admin:admin" | grep "var " | grep -v function