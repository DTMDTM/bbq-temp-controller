import pigpio
from StateListener import *
from time import *
import time,threading



class Fan(StateListener):
    pi = pigpio.pi()
    airflowPerc = 0

    def __init__(self, stateController):
        stateController.addStateListener(self)
        self.pi.write(16, 1) # Zet H-brug aan via GPIO-16

    def stateChanged(self, state):
        self.airflowPerc = state.airflowPerc

        if(self.airflowPerc < 15):
            self.pi.write(16, 0)
        else:
            self.pi.write(16, 1)
  
        self.pi.hardware_PWM(12, 100, 10000 * self.airflowPerc)
