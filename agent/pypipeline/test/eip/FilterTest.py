import time
import unittest
from pypipeline.components.destination.Log import Log

from pypipeline.components.source.Timer import Timer
from pypipeline.core.DslPipelineBuilder import DslPipelineBuilder
from pypipeline.core.Message import Message
from pypipeline.core.Plumber import Plumber

class FilterTest(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()
        pipeline1 = builder1.source(Timer, {"period": 1.0}).filter(Filter()).process(messageout)
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(10)
        plumber.stop()


class Filter:
    def __call__(self, exchange):
        parts = exchange.in_msg.body.split()
        return int(parts[-1]) % 2 == 0


def filter_method(exchange):
    parts = exchange.in_msg.body.split()
    return int(parts[-1]) % 2 == 0

def messageout(ex):
    print("messageout",ex)