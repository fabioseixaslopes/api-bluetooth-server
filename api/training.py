import dbus
import random
import sys
import json
import threading
import time
import os
import datetime
import struct
from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000
VALUE_TIMESTAMP = None
VALUE_LENGTH = None
VALUE_SCORE = None
VALUE_CALORIES = None
VALUE_REPETITIONS = None
VALUE_WEIGHT = None
json_file = open(os.path.dirname(__file__) + '/../variables.json', "r")
variables = json.load(json_file)
MACHINE_NAME = variables["machine_name"]
SERVICE_UUID = variables["service_uuid"]
CHARACTERISTIC_UUID = variables["characteristic_uuid"]
DESCRIPTOR_UUID = variables["descriptor_uuid"]
DESCRIPTOR_VALUE = variables["descriptor_value"]
json_file.close()

class TrainingAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name(MACHINE_NAME)
        self.add_service_uuid(SERVICE_UUID)
        self.include_tx_power = True

class TrainingService(Service):
    def __init__(self, index):
        Service.__init__(self, index, SERVICE_UUID, True)
        self.add_characteristic(TrainingCharacteristic(self))

class TrainingCharacteristic(Characteristic):
    def __init__(self, service):
        self.notifying = False
        Characteristic.__init__(
                self, CHARACTERISTIC_UUID,
                ["notify", "read"], service)
        self.add_descriptor(TrainingDescriptor(self))

    def get_training(self):
        value = []
        print('Values from Request: ' + str(VALUE_TIMESTAMP) + ', ' + str(VALUE_LENGTH) + ', ' + str(VALUE_SCORE) + ', ' + str(VALUE_CALORIES) + ', ' + str(VALUE_REPETITIONS) + ', ' + str (VALUE_WEIGHT))
        x = struct.pack("!l", VALUE_TIMESTAMP)
        for y in x:
                 value.append(dbus.Byte(y))
        x = struct.pack("!l", VALUE_LENGTH)
        for y in x:
                 value.append(dbus.Byte(y))
        x = struct.pack('!f',VALUE_SCORE)
        for y in x:
                 value.append(dbus.Byte(y))
        x = struct.pack('!f',VALUE_CALORIES)
        for y in x:
                 value.append(dbus.Byte(y))
        x = struct.pack("!i", VALUE_REPETITIONS)
        for y in x:
                 value.append(dbus.Byte(y))
       
        x = struct.pack("!i", VALUE_WEIGHT)
        for y in x:
                 value.append(dbus.Byte(y))
        print('Values sent to Phone Application.')
        return value

    def set_training_callback(self):
        if self.notifying:
            value = self.get_training()
            self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        return self.notifying

    def StartNotify(self):
        if self.notifying:
            return
        print('Device Connected to Host - Phone Application.')
        self.notifying = True
        print('Notifications/Readings Enabled.')
        value = self.get_training()
        self.PropertiesChanged(GATT_CHRC_IFACE, {"Value": value}, [])
        self.add_timeout(NOTIFY_TIMEOUT, self.set_training_callback)

    def StopNotify(self):
        self.notifying = False
        print('Notifications/Readings Disabled.')
        print('Device Disconnected from Host - Phone Application.')
        sys.exit("Bluetooth Peripheral ended.") # exits

    def ReadValue(self, options):
        value = self.get_training()
        self.t = threading.Timer(2.0, self.quit) # allow for read to terminate
        self.t.start()
        return value

    def quit(self):
        print('GATT application terminated.')
        print('Bluetooth Peripheral ended.')
        print('Device Disconnected from Host - Phone Application.')
        os._exit(1)

class TrainingDescriptor(Descriptor):
    def __init__(self, characteristic):
        Descriptor.__init__(
                self, DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.DESCRIPTOR_VALUE
        for c in desc:
            value.append(dbus.Byte(c.encode()))
        return value

class main():
    def run_peripheral(self, value_timestamp, value_length, value_score, value_calories, value_repetitions, value_weight):
        global VALUE_TIMESTAMP
        VALUE_TIMESTAMP = value_timestamp
        global VALUE_LENGTH
        VALUE_LENGTH = value_length
        global VALUE_SCORE
        VALUE_SCORE = value_score
        global VALUE_CALORIES
        VALUE_CALORIES = value_calories
        global VALUE_REPETITIONS
        VALUE_REPETITIONS = value_repetitions
        global VALUE_WEIGHT
        VALUE_WEIGHT = value_weight
        app = Application()
        app.add_service(TrainingService(0))
        app.register()
        adv = TrainingAdvertisement(0)
        adv.register()
        try:
            app.run()
        except KeyboardInterrupt:
            app.quit()