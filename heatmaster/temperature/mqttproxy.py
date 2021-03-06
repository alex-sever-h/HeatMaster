import paho.mqtt.client as mqtt
from ConfigurationLoader.AutoGenerated import AutoGenerated
import datetime;

class MqttSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MqttSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MqttProxy(AutoGenerated, metaclass=MqttSingleton):

    def onConnect(self, client, userdata, flags, rc):
        # Subscribing in onConnectDispatcher() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for topic, handler in topicAndHandler:
            self.client.subscribe(topic)

    def onMessage(self, client, userdata, msg):

        handlerList = self.topicAndHandler[msg.topic]
        for handler in handlerList:
            print("will call function ", handler)
            handler(msg.payload)

    def onLog(self, mqttc, obj, level, string):
        print(string)

    def __init__(self):
        super().__init__()

        self.topicAndHandler = {}
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = self.onMessage
        self.client.on_log = self.onLog

    def initializeConfig(config):
        mq = MqttProxy()
        mq.classFinder = {"host": mq.setHost, "port" : mq.setPort}
        mq.loadConfig(config)
        mq.connect()

    def setHost(self, config):
        self.host_ = config

    def setPort(self, config):
        self.port_ = int(config)

    def connect(self, host = "", port = 0):
        if(host is not ""):
            self.host_ = host
        if(port is not 0):
            self.port_ = port

        print("Connect to ", self.host_, ":", self.port_)

        self.client.connect_async(self.host_, self.port_, 60)
        self.client.loop_start()

        print("MQTT broker proxy started")

    def subscribeToTopic(self, topic, handler):
        #print("subscribe ", self, " to topic ", topic, " with handler ", handler)

        try:
            self.topicAndHandler[topic].append(handler)
        except KeyError as e:
            self.topicAndHandler[topic] = [handler]

        print("GOt to list: ", self.topicAndHandler[topic])

        self.client.loop_stop()
        self.client.subscribe(topic)
        self.client.loop_start()

if __name__ == "__main__":
    host = "mqtt.tinker.haus"
    port = 1883

    def updatefunc():
        print ("needchangenow !!\n")

    mqttBroker = MqttProxy(host, port)

    while True:

        time.sleep(1)
