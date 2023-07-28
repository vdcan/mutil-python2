import time
import unittest 
 
from pypipeline.test.components.MQTest import MQTest

import signal
import sys

import os

def sigint_handler(signal, frame):
    print( 'Interrupted')
    #sys.exit()
    os._exit(1)
signal.signal(signal.SIGINT, sigint_handler)
print("MQTest")
t = MQTest ();
t.mqtt_in(); 