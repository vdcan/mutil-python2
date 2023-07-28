from pypipeline.core.Destination import Destination
import redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class MQOut(Destination):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.channel = params["channel"]

    def process(self, exchange):
        #print("\nLog: " + self.channel + "\n" + str(exchange) + "\n")
        redis_client.publish(self.channel, exchange.in_msg.body)