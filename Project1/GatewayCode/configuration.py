#!/usr/bin/python
__author__ = 'root'

from const import Constant
from logMessages import LogMessage
from simOperations import SIMOperations
from message import Message
from messageFilter import MessageFilter
from processConfigFile import ProcessConfigFile
from rpiLCD import RPILCD
from GPIOPin import GPIOPin

import time


class Configuration:

    logMessage = ''
    const = ''
    sim = ''
    messages = ''
    messageFilter = ''
    processConfigFile = ''
    lcd = ''
    GPIOPins = ''

    def __init__(self):
        self.logMessage = LogMessage()
        self.const = Constant()
        self.sim = SIMOperations()
        self.messages = Message()
        self.processConfigFile = ProcessConfigFile()
        self.messageFilter = MessageFilter()
        self.GPIOPins = GPIOPin()
        if self.const.live:
            self.lcd = RPILCD()

    def run(self):
        try:
            if not self.sim.checkSIMCard():
                self.logMessage.log(self.messages.ERROR_INSERT_SIM)		
                self.displayOnLcd('ERROR100.')
                time.sleep(1)
                self.displayOnLcd('Please insert\nyour SIM')
                time.sleep(1)
                self.GPIOPins.ErrorLED()
            else:		
                if not self.processConfigFile.checkValuesInConfigFile():
                    self.logMessage.log(self.messages.ERROR_CONFIG)
                    self.displayOnLcd('Hello \nDigital farmer')
                    time.sleep(3)
                    self.displayOnLcd('ILLUMINUM \nGREEN HOUSE TECH')
                    time.sleep(3)
                    self.displayOnLcd('ERROR101')
                    time.sleep(1)
                    self.displayOnLcd('Kindly\nconfigure')
                    time.sleep(1)
                    self.displayOnLcd('your system')
                    self.GPIOPins.ErrorLED()
                    self.setConfigData()
        except:
            self.logMessage.log('Error in main configuration section')
            pass

    def setConfigData(self):
        try:
            setContactNumber = False
            setLowerLimit = False
            setUpperLimit = False
            while True:
                if setContactNumber and setLowerLimit and setUpperLimit:
                    self.GPIOPins.FullyFunctionalLED()
                    break

                if not setContactNumber:
                    if self.setContactNumberToConfigFile():
                        setContactNumber = True
                        phone = self.processConfigFile.readPhoneNumber()
                        message = self.messages.SMS_SET_MOBILE % (str(phone))
                        self.sim.sendSMS(message)
                        time.sleep(1)
                        # self.sim.sendSMS(self.messages.SMS_SETUP_LOWER_LIMIT)
                        time.sleep(1)
                        self.sim.sendSMS('Kindly set up your Lower limit Setting for Soil Moisture')
                        time.sleep(1)
                        self.sim.deleteReadMessages()
                        time.sleep(1)

                elif setContactNumber and not setLowerLimit and not setUpperLimit:
                    if self.setLowerLimitToConfigFile():
                        setLowerLimit = True
                        lowerLimit = self.processConfigFile.readLowerLimit()
                        message = self.messages.SMS_CONFIRM_LOWER_LIMIT % (str(lowerLimit))
                        self.sim.sendSMS(message)
                        time.sleep(2)
                        # self.sim.sendSMS(self.messages.SMS_SETUP_UPPER_LIMIT)
                        self.sim.sendSMS('Kindly set up your Upper limit')
                        time.sleep(2)
                        self.sim.deleteReadMessages()
                        time.sleep(1)

                elif setLowerLimit and setContactNumber:
                    if setLowerLimit and self.setUpperLimitToConfigFile():
                        setUpperLimit = True
                        upperLimit = self.processConfigFile.readUpperLimit()
                        message = self.messages.SMS_CONFIRM_UPPER_LIMIT % (str(upperLimit))
                        self.sim.sendSMS(message)
                        time.sleep(2)
                        # self.sim.sendSMS(self.messages.SMS_CONGRATULATIONS)
                        self.sim.sendSMS('CONGRATULATIONS! You have now set up your Smart Mobile Farm')
                        time.sleep(1)
                        self.sim.deleteReadMessages()
                        time.sleep(1)
        except:
            self.logMessage.log('Error in setting configuration')
            pass
        return True

    def setContactNumberToConfigFile(self):
        status = False
        try:
            messages = self.sim.readUnreadMessages()
            contactNumber = self.messageFilter.readContactNumber(messages)
            if contactNumber:
                self.logMessage.log('Contact number found : ' + str(contactNumber))
                self.processConfigFile.updateContactNumber(contactNumber)
                status = True
        except:
            self.logMessage.log('Error in setting contact number')
            pass
        return status

    def setLowerLimitToConfigFile(self):
        status = False
        try:
            messages = self.sim.readUnreadMessages()
            lowerLimit = self.messageFilter.readLowerLimit(messages)
            if lowerLimit:
                self.logMessage.log('lower limit found : ' + str(lowerLimit))
                self.processConfigFile.updateLowerLimitNumber(str(lowerLimit))
                status = True
        except:
            self.logMessage.log('Error in setting lower limit')
            pass
        return status

    def setUpperLimitToConfigFile(self):
        status = False
        try:
            messages = self.sim.readUnreadMessages()
            upperLimit = self.messageFilter.readUpperLimit(messages)
            if upperLimit:
                self.logMessage.log('upper limit found : ' + str(upperLimit))
                self.processConfigFile.updateUpperLimitNumber(str(upperLimit))
                status = True
        except:
            self.logMessage.log('Error in setting upper limit')
            pass
        return status

    # display text on LCD screen
    def displayOnLcd(self, text):
        if self.const.live:
            self.lcd.clear()
            self.lcd.message(text)
        else:
            print text


objConfiguration = Configuration()
objConfiguration.run()