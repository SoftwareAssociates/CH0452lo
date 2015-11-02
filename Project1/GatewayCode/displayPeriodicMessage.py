#!/usr/bin/python
__author__ = 'root'

from const import Constant
from logMessages import LogMessage
from processSensorReading import ProcessSensorReading
from rpiLCD import RPILCD

import time


class DisplayPeriodicMessage:

    logMessage = ''
    const = ''
    processSensorData = ''
    lcd = ''

    def __init__(self):
        self.logMessage = LogMessage()
        self.const = Constant()
        self.processSensorData = ProcessSensorReading()
        if self.const.live:
            self.lcd = RPILCD()

    def run(self):
        try:
            if self.processSensorData.checkConfigFileExist():
                while True:
                    data = self.processSensorData.getSensorData()

                    currentTime = time.strftime("%d.%m.%Y %H:%M:%S")
                    self.displayOnLcd('ILLUMINUM \nGREEN HOUSE TECH')
                    time.sleep(5)
                    self.displayOnLcd('TAITA FARM')
                    time.sleep(5)
                    self.displayOnLcd('SMART MOBILE \nFARMING')
                    time.sleep(5)
                    self.displayOnLcd('TEMP : ' + str(data[0]) + ' CELSIUS')
                    time.sleep(3)
                    self.displayOnLcd('HUM : ' + str(data[1]) + ' %')
                    time.sleep(3)
                    self.displayOnLcd('SOIL MOISTURE \n ' + str(data[2]) + ' %')
                    time.sleep(3)
                    self.displayOnLcd('IRRIGATION : ' + str(data[5]))
                    time.sleep(3)
                    self.displayOnLcd('WATER USED : ' + str(data[3]))
                    time.sleep(3)
                    self.displayOnLcd('DATE : ' + str(currentTime))
                    time.sleep(3)
            else:
                self.logMessage.log('Invalid configuration data / No file found - Display Periodic Message')
                self.run()
        except:
            self.logMessage.log('Error in displaying periodic messages')
            self.run()

    # display text on LCD screen
    def displayOnLcd(self, text):
        if self.const.live:
            self.lcd.clear()
            time.sleep(1)
            self.lcd.message(text)
        else:
            print text

obDisplay = DisplayPeriodicMessage()
obDisplay.run()


