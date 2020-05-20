import sys
print(sys.path)

#TODO: This is a way, but overriding __import__ might be better
from mock import Mock
if 'RPi' not in sys.modules.keys():
    sys.modules['RPi'] = Mock()
if 'RPi.GPIO' not in sys.modules.keys():
    sys.modules['RPi.GPIO'] = Mock()

from ConfigurationLoader.Parser import Parser
from ConfigurationLoader.AutoGenerated import AutoGenerated

from thermostate.thermostategroup import ThermostateGroup
from temperature.mqttproxy import MqttProxy
from heater.heater import Heater
from tigger.trigger import Trigger
from threading import Event

from heatmaster import HeatMaster

import time
import logging

import utils.ColoredLogger

import unittest


class BasicTest(unittest.TestCase):
    def test_BasicTest(self):
        import sys
        import os
        absFilePath = os.path.abspath(__file__)
        path, filename = os.path.split(absFilePath)
        confFile = path + "/config-test-simple.json"

        utils.ColoredLogger.setColoredLogger()

        ps = Parser(confFile)
        hm = HeatMaster(config = ps.getConfiguration())
        hm.run(5)
