#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.
 
 
import redis
import json 
import subprocess
import os
from string import Template
import copy
import datetime
import logging;

import logging.handlers
import os
import my_config;
import DBTool

import sys
import os
from os import listdir
from os.path import isfile, join
#import taos
#taos_conn =  taos.connect(host=my_config.config["taos_host"], user=my_config.config["taos_user"], password=my_config.config["taos_pwd"] )
#E:\workdir\MQTTJSql\ExportTool\ExportTool\bin\Debug\target\redis 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", my_config.config["logPath"]))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
root.addHandler(handler)
  
  
REDIS = redis.Redis(host= my_config.config["redis_host"], port=my_config.config["redis_port"])   

logging.basicConfig(level=logging.debug)
logging.exception("Exception in main()")

 
def doUserDetail(fn):
    print (cwd +"\\"+fn)
    f = open(cwd +"\\"+fn, "r", encoding = "utf-8")
    k2 = fn.replace("_colon_",":").replace(".txt","")
    value = f.read();
    print (value)
    REDIS.set(k2, str(value));   
		 
 
print(str(sys.argv))

cwd =sys.argv[1];# os.getcwd()
for f in os.listdir(cwd):
    doUserDetail(f); 
