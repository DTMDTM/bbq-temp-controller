from datetime import datetime
from InputListener import *
from StateListener import *
from Display import *
import threading, copy

class ScreenController(InputListener, StateListener):
    _display = {}
    _stateController = {}
    _currentState = {}
    _lock = threading.Lock()
    _screenNr = 0

    def __init__(self, display, encoder, stateController):
        self._display = display
        self._stateController = stateController
        stateController.addStateListener(self)
        self._display.clearDisplay()
        encoder.addInputListener(self)

    def stateChanged(self, state):
        self._currentState = state
        self.drawScreen()

    def buttonTimeout(self):
        self._screenNr = 0
        self.drawScreenMenu()

    def buttonUp(self):
        if (self._screenNr==1):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.bbqTempSet = newState.bbqTempSet+1
            self._stateController.updateState(newState)
        if (self._screenNr==2):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.meatTempSet = newState.meatTempSet+1
            self._stateController.updateState(newState)
        if (self._screenNr==3):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.forceCloseAirflow = not newState.forceCloseAirflow
            self._stateController.updateState(newState)
        if (self._screenNr==4):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.forceFullAirflow = not newState.forceFullAirflow
            self._stateController.updateState(newState)

    def buttonDown(self):
        if (self._screenNr==1):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.bbqTempSet = newState.bbqTempSet-1
            self._stateController.updateState(newState)
        if (self._screenNr==2):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.meatTempSet = newState.meatTempSet-1
            self._stateController.updateState(newState)
        if (self._screenNr==3):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.forceCloseAirflow = not newState.forceCloseAirflow
            self._stateController.updateState(newState)
        if (self._screenNr==4):
            oldState = self._stateController.getState()
            newState = copy.copy(oldState)
            newState.forceFullAirflow = not newState.forceFullAirflow
            self._stateController.updateState(newState)

    def buttonPressed(self):
        self._screenNr = self._screenNr+1
        if (self._screenNr>5):
            self._screenNr = 0
        self.drawScreenMenu()

    def drawScreen(self):
        self._lock.acquire()
        try:
            self._drawScreen()
        finally:
            self._lock.release() # release lock, no matter what

    def drawScreenBbqTemp(self):
        self._lock.acquire()
        try:
            self._drawScreenBbqTemp()
        finally:
            self._lock.release() # release lock, no matter what

    def drawScreenMeatTemp(self):
        self._lock.acquire()
        try:
            self._drawScreenMeatTemp()
        finally:
            self._lock.release() # release lock, no matter what

    def drawScreenMenu(self):
        self._lock.acquire()
        try:
            self._drawScreenMenu()
        finally:
            self._lock.release() # release lock, no matter what

    def _drawScreen(self):
        self._drawScreenBbqTemp()
        self._drawScreenMeatTemp()
        self._drawScreenMenu()
        self._drawScreenAirflow()

    def _drawScreenBbqTemp(self):
        state = self._currentState
        toDisplay = "-" if(state.bbqTemp is None) else "{0:.2f}".format(state.bbqTemp)
        self._display.display("BBQ  : "+ toDisplay + " ("+str(state.bbqTempSet)+")", 1)

    def _drawScreenMeatTemp(self):
        state = self._currentState
        toDisplay = "-" if(state.meatTemp is None) else "{0:.2f}".format(state.meatTemp)
        self._display.display("Vlees: "+ toDisplay + " ("+str(state.meatTempSet)+")", 2)

    def _drawScreenAirflow(self):
        state = self._currentState
        self._display.display("Luchttoevoer "+str(state.airflowPerc)+"%", 3)

    def _drawScreenMenu(self):
        state = self._currentState
        if (self._screenNr == 0 and state.forceCloseAirflow):
            self._display.display("Running (dicht)", 4)
        if (self._screenNr == 0 and not state.forceCloseAirflow):
            self._display.display("Running (auto)", 4)
        if (self._screenNr == 1 ):
            self._display.display("Set bbq temp", 4)
        if (self._screenNr == 2 ):
            self._display.display("Set meat temp", 4)
        if (self._screenNr == 3 and state.forceCloseAirflow):
            self._display.display("Toevoer dicht", 4)
        if (self._screenNr == 3 and not state.forceCloseAirflow):
            self._display.display("Toevoer automatisch", 4)
        if (self._screenNr == 4 and state.forceCloseAirflow):
            self._display.display("Toevoer 100%", 4)
        if (self._screenNr == 4 and not state.forceFullAirflow):
            self._display.display("Toevoer automatisch", 4)
        if (self._screenNr == 5 ):
            self._display.display(self._currentState.ipadress, 4)
