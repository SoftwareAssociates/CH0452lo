#!/usr/bin/python
__author__ = 'root'

from const import Constant
from logMessages import LogMessage
from simOperations import SIMOperations
from message import Message
from messageFilter import MessageFilter
from processConfigFile import ProcessConfigFile
from processSensorReading import ProcessSensorReading

import time


class InstantAction:

    logMessage = ''
    const = ''
    sim = ''
    messages = ''
    messageFilter = ''
    processConfigFile = ''
    processSensorData = ''

    def __init__(self):
        self.logMessage = LogMessage()
        self.const = Constant()
        self.sim = SIMOperations()
        self.messages = Message()
        self.processConfigFile = ProcessConfigFile()
        self.processSensorData = ProcessSensorReading()
        self.messageFilter = MessageFilter()

    def run(self):
        try:
            if self.processConfigFile.checkValuesInConfigFile():
                if self.sim.checkSIMCard():
                    while True:
                        messages = self.sim.readUnreadMessages()
                        if self.messageFilter.readCheckBalance(messages):
                            self.sim.sendSMSCheckBalance()
                            time.sleep(30)
                            lastReadMessage = self.sim.readFirstUnreadMessages()
                            message = self.messageFilter.readBalanceMessage(lastReadMessage)
                            self.sim.sendSMS(message)
                            time.sleep(5)
                            self.sim.deleteReadMessages()
                        elif self.messageFilter.readUsedWater(messages):
                            # get used water
                            waterFlow = self.processSensorData.getWaterUsed()
                            currentDate = time.strftime("%d.%m.%Y,%H:%M")
                            message = 'Dear Digital Farmer, Water used is %s litres as of %s' % (str(waterFlow), str(currentDate))
                            self.sim.sendSMS(message)
                            time.sleep(5)
                            self.sim.deleteReadMessages()
                else:
                    self.logMessage.log('No SIM Card detected - Instant Action')
                    self.run()
            else:
                self.logMessage.log('Invalid configuration data / No file found - Instant Action')
                self.run()
        except:
            self.logMessage.log('Error in Instant Action')
            time.sleep(60)
            self.run()


objInstantAction = InstantAction()
objInstantAction.run()


