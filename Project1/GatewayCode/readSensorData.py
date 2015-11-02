#!/usr/bin/python
__author__ = 'root'

from const import Constant
from logMessages import LogMessage
from processSensorReading import ProcessSensorReading
from processConfigFile import ProcessConfigFile
from GPIOPin import GPIOPin

import smbus
import time


class ReadSensorData:

    logMessage = ''
    const = ''
    processSensorData = ''
    processConfigFile = ''
    GPIOPins = ''
    bus = ''
    address = 0x04

    def __init__(self):
        self.logMessage = LogMessage()
        self.const = Constant()
        self.processSensorData = ProcessSensorReading()
        self.processConfigFile = ProcessConfigFile()
        self.GPIOPins = GPIOPin()
        self.bus = smbus.SMBus(1)

    def run(self):
        try:
            if self.processConfigFile.checkValuesInConfigFile():
                self.i2cRead()
            else:
                self.logMessage.log('Invalid configuration data / No file found - Read Sensor Data')
                time.sleep(40)
                self.run()
        except:
            self.logMessage.log('Error on reading sensor data frequently')
            time.sleep(40)
            self.run()

    def i2cRead(self):
        try:
            while True:

                self.writeNumber(self.const.SENSOR_CODE_TEMPERATURE)
                time.sleep(1)
                temperature = self.readNumber()
                self.processSensorData.updateTemperature(str(temperature))

                self.writeNumber(self.const.SENSOR_CODE_HUMIDITY)
                time.sleep(1)
                humidity = self.readNumber()
                self.processSensorData.updateHumidity(str(humidity))

                self.writeNumber(self.const.SENSOR_CODE_MOISTURE)
                time.sleep(1)
                moisture = self.readNumber()		
                self.processSensorData.updateMoisture(str(moisture))

                self.writeNumber(self.const.SENSOR_CODE_WATER)
                time.sleep(1)
                water = self.readNumber()		
                self.processSensorData.updateWaterUsed(str(water))

                self.writeNumber(self.const.SENSOR_CODE_BATTERY)
                time.sleep(1)
                battery = self.readNumber()
                self.processSensorData.updateBattery(str(battery))

                # power valve based on soil moisture
                self.checkSoilMoisture(moisture)
        except:
            self.logMessage.log('Error on sending request to Arduino - Read Sensor Data')
            pass

    def checkSoilMoisture(self, moisture):
        try:
            if moisture > 0:
                lowerLimit = self.processConfigFile.readLowerLimit()
                higherLimit = self.processConfigFile.readUpperLimit()
                if moisture < lowerLimit:
                    self.GPIOPins.powerOnValve()
                    self.processSensorData.updateStateOfValve('ON')
                elif moisture > higherLimit:
                    self.GPIOPins.powerOffValve()
                    self.processSensorData.updateStateOfValve('OFF')
        except:
            self.logMessage.log('Error on checking soil moisture - Read Sensor Data')
            pass

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

objReadSensorData = ReadSensorData()
objReadSensorData.run()


