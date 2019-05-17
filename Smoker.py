from Display import *
from Encoder import *
from ScreenController import *
from TemperatureController import *
from StateController import *
# from NetworkController import *
from StorageController import *
from AirflowController import *
from Fan import *
# from Motor import *
import time
# from UploadController import *
# from CheckRemoteSettingsController import *

display = Display()
encoder = Encoder()
stateController = StateController()
storageController = StorageController(stateController)
temperatureController = TemperatureController(stateController)
# networkController = NetworkController(stateController)
screenController = ScreenController(display, encoder, stateController)
airflowController = AirflowController(stateController)
fan = Fan(stateController)
# motor = Motor(stateController)
# uploadController = UploadController(stateController)
# checkRemoteSettingsController = CheckRemoteSettingsController(stateController)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt: # Ctrl-C to terminate the program
    GPIO.cleanup()

