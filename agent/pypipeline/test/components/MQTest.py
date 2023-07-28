import time
import unittest

from pypipeline.components.source.MQTTSource import MQTTIn
from pypipeline.components.destination.MQTTDest import MQTTOut
from pypipeline.components.source.RedisMQSource import MQIn
from pypipeline.components.destination.RedisMQDest import MQOut
from pypipeline.components.destination.Log import Log
from pypipeline.components.source.Timer import Timer
from pypipeline.core.DslPipelineBuilder import DslPipelineBuilder
from pypipeline.core.Plumber import Plumber


class MQTest(unittest.TestCase):

    def test_log(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(Timer, {"period": 1.0}).to(MQOut, {"channel": "my_queue"})
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(3)
        plumber.stop()
    def test_log2(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(MQIn, {"channel": "my_queue"}).to(Log, {"name": "my_queue"})
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(3)
        plumber.stop()
    def mqtt_out(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(Timer, {"period": 1.0}).to(MQTTOut, {"topic": "p/caijie/s11/g1/esp1/ts4"}) 
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(3)
        plumber.stop()
    def mqtt_in(self):
        plumber = Plumber()
        builder = DslPipelineBuilder()
        pipeline = builder.source(MQTTIn, {"topic": "p/caijie/#"}).to(Log, {"name": "my_queue"})
        plumber.add_pipeline(pipeline)
        plumber.start()
        time.sleep(23)
        plumber.stop()
