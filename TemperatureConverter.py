import math

class TemperatureConverter:

    resistorValueBbq = 10000 # We use 10k resistors for both probes but they measured differently
    resistorValueMeat = 10020 

    curvedProbeBeta = 4008 
    curvedProbeR25 = 91240
    straightProbeBeta = 4329
    straightProbeR25 = 232300

    def convertBbq(self, voltage):
        return self._convert(voltage, self.curvedProbeBeta, self.curvedProbeR25)


    def convertMeat(self, voltage):
        return self._convert(voltage, self.straightProbeBeta, self.straightProbeR25)

    def _convert(self, voltage, beta, r25):
        T25 = 273.15 + 25
        resistance = self._getResistance(voltage)
        
        if(resistance is None):
            return None

        temp = 1 / (math.log(resistance/r25)/beta + (1/T25))

        return temp - 273.15

    def _getResistance(self, voltage):
        if(voltage >= 5):
            return None
        return (10000 * voltage) / (5 - voltage) 
