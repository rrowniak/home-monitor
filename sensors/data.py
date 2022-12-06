class SmartMeterMeasurement:
    def __init__(self, volt, amp, pow, powFactor, phase='A'):
        self.volt = volt
        self.amp = amp
        self.pow = pow
        self.powFactor = powFactor
        self.phaseLabel = phase

    def __repr__(self) -> str:
        return f'<{self.phaseLabel}: {self.pow}W, {self.volt}V, {self.amp}A, {self.powFactor}pf>'

SmartMeterMeasurementV = list[SmartMeterMeasurement]