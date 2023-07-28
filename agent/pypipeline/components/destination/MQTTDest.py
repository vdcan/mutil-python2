from pypipeline.core.Destination import Destination 

import paho.mqtt.client as mqtt


mqttc = mqtt.Client()

def sendMqttMessage(topic, msg): 
    mqttc.publish(topic, msg)
    #logging.debug(topic, msg);
 
# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.

 

class MQTTOut(Destination):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.topic = params["topic"]
        mqttc.connect('mqttagent.polltek.com', 1883, 60)

    def process(self, exchange):
        #print("\nLog: " + self.channel + "\n" + str(exchange) + "\n")
        sendMqttMessage(self.topic , exchange.in_msg.body) 