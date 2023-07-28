from pypipeline.core.Source import Source
import threading
import time
from pypipeline.core.Exchange import Exchange
from pypipeline.core.Message import Message


class Timer(Source):
    def __init__(self, plumber, params):
        super().__init__(plumber, params)
        self.period = float(params["period"])
        self.thread = None

    def start(self):
        self.thread = TimerThread(self, self.plumber)
        self.thread.start()

    def stop(self):
        self.thread.stop()


class TimerThread(threading.Thread):
    def __init__(self, source, plumber):
        super().__init__()
        self.stopped = False
        self.source = source
        self.period = source.period
        self.plumber = plumber
        self.count = 0

    def stop(self):
        self.stopped = True

    def run(self):
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
