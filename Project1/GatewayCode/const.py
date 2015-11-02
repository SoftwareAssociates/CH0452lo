#!/usr/bin/python
__author__ = 'root'

import os


class Constant:

    CONFIG_FILE = ''
    SENSOR_DATA_FILE = ''
    PY_SCRIPT_PATH = ''
    LOG_PATH = ''
    DATA_PATH = ''
    HOST = '192.168.8.1'
    SERIAL_PORT = '/dev/ttyAMA0'
    SERIAL_GSM_PORT = '/dev/ttyAMA0'
    BAUD_RATE = 9600
    TIMEOUT = 10
    GSM_TIMEOUT = 2
    ENABLE_LOG = True
    LCD_SCROLL = True

    SENSOR_CODE_TEMPERATURE = 1
    SENSOR_CODE_HUMIDITY = 2
    SENSOR_CODE_MOISTURE = 3
    SENSOR_CODE_WATER = 4
    SENSOR_CODE_BATTERY = 5
    SENSOR_CODE_WATER_RESET = 6

    GPIO_PIN_VALVE = 26
    GPIO_PIN_BUZZER = 22
    GPIO_PIN_FULLY_FUNCTIONAL_LED = 13
    GPIO_PIN_ERROR_LED = 21

    GPIO_STATUS_POWER_ON = 1
    GPIO_STATUS_POWER_OFF = 0

    live = True

    def __init__(self):
        self.PY_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.LOG_PATH = self.PY_SCRIPT_PATH + '/log/'
        self.DATA_PATH = self.PY_SCRIPT_PATH + '/data/'
        self.CONFIG_FILE = self.DATA_PATH + 'configData.cnf'
        self.SENSOR_DATA_FILE = self.DATA_PATH + 'sensorData.cnf'
        if self.PY_SCRIPT_PATH == "/home/web/Python/iot/taitafarm":
            self.live = False
