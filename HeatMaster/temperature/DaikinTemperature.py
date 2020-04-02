from ConfigurationLoader.AutoGenerated import AutoGenerated
from temperature.temperature import Temperature
import datetime;
import requests as req
import sched, time

class DaikinTemperature(Temperature, AutoGenerated):

    def __init__(self, host = None, callback = None, config = None, pollrate=5):
        AutoGenerated.__init__(self)
        Temperature.__init__(self, callback)
        self.temperature_ = float('nan')
        self.pollrate_ = pollrate
        self.sensors = {}

        self.classFinder = {"host": self.setHost}

        if(host):
            self.setHost(host)
        elif(config):
            self.loadConfig(config)

        self.startPolling()

    def setHost(self, config):
        self.host_ = config

    def startPolling(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(self.pollrate_, 1, self.scheduledUpdate)
        #self.s.run()

    def interrogate(self):
        url = 'http://' + self.host_ + "/aircon/get_sensor_info"
        headers = {'Host': self.host_ }
        r = req.get(url, headers=headers)
        return r

    def parseSensor(self, response):
        split = response.split(",")
        #print (split)

        for sensor in split:
            k, v = sensor.split("=")
            print ("Entry ", k, " is ", v)

            self.sensors[k] = v

    def scheduledUpdate(self):
        self.updateTemperature()
        self.s.enter(self.pollrate_, 1, self.scheduledUpdate)

    def updateTemperature(self):
        response = self.interrogate()
        self.parseSensor(response.text)
        self.temperature_ = self.sensors['htemp']
        self.timestamp_ = datetime.datetime.now().timestamp()

        if (self.callback_ is not None):
            self.callback_()

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
