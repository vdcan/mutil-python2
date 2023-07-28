import time
import unittest 
 
from MQTTPipeline import MQTTPipeline

import signal
import sys

import os

def sigint_handler(signal, frame):
    print( 'Interrupted')
    #sys.exit()
    os._exit(1)
signal.signal(signal.SIGINT, sigint_handler)
print("MQTest")
t = MQTTPipeline ();
t.test_simple_pipeline(); 