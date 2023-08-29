import time
import unittest 
 
from MQTTPipeline import MQTTPipeline

import signal
import sys
import time
import os

def sigint_handler(signal, frame):
    print( 'Interrupted')
    #sys.exit()
    os._exit(1)
signal.signal(signal.SIGINT, sigint_handler)
print("MQTest")
time.sleep(2)
t = MQTTPipeline ();
time.sleep(1)
t.test_simple_pipeline(); 