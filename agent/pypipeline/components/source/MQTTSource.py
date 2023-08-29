from pypipeline.core.Source import Source
import threading
import time
from pypipeline.core.Exchange import Exchange
from pypipeline.core.Message import Message
 
import paho.mqtt.client as mqtt
import json
import my_config
 

class MQTTIn(Source):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.topic = params["topic"]
        self.thread = None

    def start(self):
        self.thread = MQThread(self, self.plumber)
        self.thread.start()

    def stop(self):
        self.thread.stop()



class MQThread(threading.Thread):
    
    def on_message( self, mqttc, obj, msg):
        m = msg.topic
        #m= m.replace("s/SensorData2", "");
        ms = msg.payload.decode("utf-8")
        ms = ms.replace("'", "\"")
        ms = ms.replace(",,", ",")
        topic = m
        print(m,ms)
        #topic, msg = convertData(m, ms)
        #logging.debug(topic, msg);
        if self.plumber is not None:
                exchange = self.plumber.create_exchange()
        else:
            exchange = Exchange()
        if(topic != ""):
            message = Message()
            message.body = {"topic": topic, "message":json.loads(ms)   }
            #print(message)
            exchange.in_msg =  message
            self.source.chain.process(exchange)


    def __init__(self, source, plumber):
        super().__init__()
        self.stopped = False
        self.source = source
        self.topic = source.topic
        self.plumber = plumber
        self.count = 0 
        self.mqttc = mqtt.Client()
        self.mqttc.me = self;
        self.mqttc.on_message = self.on_message

    def stop(self):
        self.stopped = True    

    def message_handler(self, msg):
        if self.plumber is not None:
                exchange = self.plumber.create_exchange()
        else:
            exchange = Exchange()
        message = Message()
        message.body = "This is exchange " +str(msg["data"].decode())
        exchange.in_msg = message
        self.source.chain.process(exchange)
        
        #print(f"Received message: {message['data'].decode()}")
 
    def run(self):
        print("MQTTIn:",my_config.config["mqtt_host"] )
        #flag = self.mqttc.connect(my_config.config["mqtt_host"], 1883, 160)  
        #flag = self.mqttc.connect(my_config.config["mqtt_host"] , 1883, 60)  
        
        flag = self.mqttc.connect("35.220.135.133", 1883, 60)  
        print("self.topic", self.topic)
        flag2= self.mqttc.subscribe(self.topic , 1)
        print("run  topic", self.topic, flag,flag2)
        
        self.mqttc.loop_forever()