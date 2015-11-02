#!/usr/bin/python
__author__ = 'root'

from const import Constant
from logMessages import LogMessage
from simOperations import SIMOperations
from message import Message
from processSensorReading import ProcessSensorReading
from processConfigFile import ProcessConfigFile

import smbus
import time


class DailyReport:

    logMessage = ''
    const = ''
    sim = ''
    messages = ''
    processSensorData = ''
    processConfigFile = ''
    bus = ''
    address = 0x04

    def __init__(self):
        self.logMessage = LogMessage()
        self.const = Constant()
        self.sim = SIMOperations()
        self.messages = Message()
        self.processConfigFile = ProcessConfigFile()
        self.processSensorData = ProcessSensorReading()
        self.bus = smbus.SMBus(1)

    def run(self):
        try:
            if self.sim.checkSIMCard():
                if self.processConfigFile.checkValuesInConfigFile():
                    data = self.processSensorData.getSensorData()
                    if len(data) > 0:
                        currentTime = time.strftime("%d.%m.%Y %H:%M:%S")
                        message1 = 'Dear Digital Farmer, here is your farm’s status;'
                        message2 = 'Device ID: %s \n Temperature: %s \n Humidity: %s ' % ('SMF001', str(data[0]), str(data[1]))
                        message3 = 'Soil Moisture: %s \n Liters of water irrigated: %s ' % (str(data[2]), str(data[3]))
                        message4 = 'State of Valve: %s \n Battery voltage: %s \n Date and Time: %s' % (str(data[5]), str(data[4]), str(currentTime))
                        self.sim.sendSMS(message1)
                        time.sleep(2)
                        self.sim.sendSMS(message2)
                        time.sleep(2)
                        self.sim.sendSMS(message3)
                        time.sleep(2)
                        self.sim.sendSMS(message4)
                        self.logMessage.log('Running daily schedule : (message : ' + str(message1) + str(message2) + str(message3) + str(message4) + ' )')
                        self.processSensorData.updateWaterUsed('0')
                        # send alert to arduino to reset water usage value
                        self.writeNumber(self.const.SENSOR_CODE_WATER_RESET)
                        time.sleep(1)
                        water = self.readNumber()
                        self.processSensorData.updateWaterUsed(water)
                    else:
                        self.logMessage.log('No sensor data saved')
                else:
                    self.logMessage.log('Invalid configuration data / No file found - Daily report')
            else:
                self.logMessage.log('Error No SIM Card detected - Daily report')
        except:
            self.logMessage.log('Error in Daily Report')

    def writeNumber(self, value):
        try:
            self.bus.write_byte(self.address, value)
        except:
            pass
        return -1

    def readNumber(self):
        number = 0
        try:
            number = self.bus.read_byte(self.address)
        except:
            pass
        return number

objDailyReport = DailyReport()
objDailyReport.run()

