from ConfigurationLoader.Parser import Parser
from ConfigurationLoader.AutoGenerated import AutoGenerated

from thermostate.thermostategroup import ThermostateGroup
from temperature.mqttproxy import MqttProxy
from heater.heater import Heater
from tigger.trigger import Trigger
from threading import Event

import time
import logging

import utils.ColoredLogger

class HeatMaster(Trigger, AutoGenerated):

    def __init__(self, config = None):
        AutoGenerated.__init__(self)
        Trigger.__init__(self)

        self.logger = logging.getLogger(self.__class__.__name__)

        self.recalculateEvent = Event()

        self.classFinder = {
            "mqtt": MqttProxy.initializeConfig,
            "thermostates" : ThermostateGroup,
            "heater" : Heater}
        self.logger.info (self.classFinder)

        if(config):
            self.children = self.loadConfig(config)

        self.registerCallback(self.children, self.recalculateTrigger)

        self.logger.warning ("----------------------------------------- INSPECT START TIME -----------------------------------------")
        self.inspect(True)
        self.logger.warning ("------------------------------------------ INSPECT END TIME ------------------------------------------")

    def recalculateTrigger(self, chain, arg):
        self.logger.warning ("trigger recalculation because of %s" % chain)
        self.recalculateEvent.set()

    def run(self, timeout_seconds = 0):
        seconds = time.time()
        while timeout_seconds == 0 or time.time() < seconds + timeout_seconds:
            self.recalculateEvent.wait(10)
            self.logger.info ("!!!!!!!! Woken up !!!!!!")
            self.recalculateEvent.clear()

if __name__ == "__main__":
    import sys
    confFile = sys.argv[1]

    utils.ColoredLogger.setColoredLogger()

    ps = Parser(confFile)
    hm = HeatMaster(config = ps.getConfiguration())
    hm.run()