import threading, copy, sys
from State import *
from TemperatureConverter import *
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class TemperatureController:
    stateController = {}
    temperatureConverter = TemperatureConverter()
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1015(i2c)
    ads.gain = 2/3
    adcVoltageConstant = 5/26544 # Defined by the measurement without any probes attached
    meatChannel = AnalogIn(ads, ADS.P3) # Blauw-paarsje draadjes
    bbqChannel = AnalogIn(ads, ADS.P2) # Groen-gele draadjes

    def __init__(self, stateController):
        self.stateController = stateController
        threading.Timer(1, self.onTimer).start()

    def onTimer(self):
        threading.Timer(1, self.onTimer).start()
        bbqTemp = self.temperatureConverter.convertBbq(self.bbqChannel.value * self.adcVoltageConstant)
        meatTemp = self.temperatureConverter.convertMeat(self.meatChannel.value * self.adcVoltageConstant)
        self._updateState(bbqTemp, meatTemp)


    def _updateState(self, bbqTemp, meatTemp):
        # hou deze functie zo snel mogelijk, om te voorkomen dat we stae changes uit andere threads overschrijven
        oldState = self.stateController.getState()
        newState = copy.copy(oldState)
        newState.bbqTemp = bbqTemp
        newState.meatTemp = meatTemp
        self.stateController.updateState(newState)

