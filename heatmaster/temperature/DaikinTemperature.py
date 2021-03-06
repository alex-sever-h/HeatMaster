from ConfigurationLoader.AutoGenerated import AutoGenerated
from temperature.temperature import Temperature
import datetime;
import requests as req
from threading import Thread,Event

import logging

class DaikinTemperature(Thread, Temperature, AutoGenerated):

    def __init__(self, host = None, callback = None, config = None, pollrate=5):
        AutoGenerated.__init__(self)
        Temperature.__init__(self)
        Thread.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.stopped = Event()

        self.temperature_ = float('nan')
        self.setPollrate(pollrate)
        self.sensors = {}

        self.setCallback(callback)

        self.classFinder = {"host": self.setHost, "pollrate":self.setPollrate}

        if(host):
            self.setHost(host)
        elif(config):
            self.loadConfig(config)

        self.start()

    def setHost(self, config):
        self.host_ = config

    def setPollrate(self, config):
        self.pollrate_ = int(config)

    def run(self):
        while not self.stopped.wait(self.pollrate_):
            self.scheduledUpdate()

    def interrogate(self):
        url = 'http://' + self.host_ + "/aircon/get_sensor_info"
        headers = {'Host': self.host_ }
        r = req.get(url, headers=headers)
        return r

    def parseSensor(self, response):
        self.logger.debug (response)

        split = response.split(",")
        for sensor in split:
            k, v = sensor.split("=")
            self.logger.debug ("HVAC parameter {} is {}".format(k, v))

            self.sensors[k] = v

    def scheduledUpdate(self):
        self.updateTemperature()

    def updateTemperature(self):
        response = self.interrogate()
        self.parseSensor(response.text)
        self.temperature_ = self.sensors['htemp']
        self.timestamp_ = datetime.datetime.now().timestamp()

        self.propagate(None, self.temperature_)

    def get(self):
        return self.temperature_

    def getTime(self):
        return self.timestamp_ini

    def __str__(self):
        return "Daikin HVAC temperature input from " + str(self.host_)


if __name__ == "__main__":
    host = '10.10.31.61'
    port = 80

    def updatefunc():
        print ("needchangenow !!\n")

    m1 = DaikinTemperature(host, pollrate=1, callback = updatefunc)


    while True:
        import time

        print("Temperature 1 is ", m1.get())

        time.sleep(30)
