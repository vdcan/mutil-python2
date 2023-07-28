from pypipeline.core.Source import Source
import threading
import time
from pypipeline.core.Exchange import Exchange
from pypipeline.core.Message import Message
 
import redis

# Connect to Redis server
import my_config;
redis_client = redis.Redis(
    host=my_config.config["redis_host"], port=my_config.config["redis_port"])

class MQIn(Source):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.channel = params["channel"]
        self.thread = None

    def start(self):
        self.thread = MQThread(self, self.plumber)
        self.thread.start()

    def stop(self):
        self.thread.stop()



class MQThread(threading.Thread):
    def __init__(self, source, plumber):
        super().__init__()
        self.stopped = False
        self.source = source
        self.channel = source.channel
        self.plumber = plumber
        self.count = 0

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

    def subscribe_to_queue(self,channel):
        pubsub = redis_client.pubsub()
        pubsub.subscribe(channel)
        for message in pubsub.listen():
            if message['type'] == 'message':
                self.message_handler(message)


    def run(self):
        self.subscribe_to_queue(self.channel)
"""

        while not self.stopped:
            time.sleep(self.period)
            if self.plumber is not None:
                exchange = self.plumber.create_exchange()
            else:
                exchange = Exchange()
            message = Message()
            message.body = "This is exchange " + str(self.count)
            exchange.in_msg = message
            self.source.chain.process(exchange)
            self.count += 1
"""