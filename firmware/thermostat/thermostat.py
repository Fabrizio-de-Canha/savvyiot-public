import ujson # type: ignore

class thermostatConfig():
    def __init__(self, upper_limit, lower_limit, max_temp, min_temp, heater):
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.heater = heater

class savvyThermostat():
    def __init__(self):
        with open('thermostat.json') as fp:
            data = ujson.loads(fp.read())
            
        self.config = thermostatConfig(**data)

        print(self.config.heater)

    def determainRelayState(self, temperature):
        if(temperature > self.config.max_temp):
                raise OverHeating
        
        if(self.config.heater):
            if(temperature < self.config.lower_limit):
                return 1
            if(temperature > self.config.upper_limit):
                return 0
            
            
        else:
            if(temperature > self.config.max_temp):
                raise OverHeating
            
            if(temperature < self.config.min_temp):
                raise OverCooling
            
            if(temperature < self.config.lower_limit):
                return 0
            if(temperature > self.config.upper_limit):
                return 1
            
class OverHeating(Exception):
    """Raised when there is an overheating or cooling event"""
    pass

class OverCooling(Exception):
    """Raised when there is an overheating or cooling event"""
    pass