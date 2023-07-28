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

import context  # Ensures paho is in PYTHONPATH

import paho.mqtt.client as mqtt
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

#from flask import Flask
#app = Flask(__name__)

#import taos
#taos_conn =  taos.connect(host=my_config.config["taos_host"], user=my_config.config["taos_user"], password=my_config.config["taos_pwd"] )
 
handler = logging.handlers.WatchedFileHandler(
    os.environ.get("LOGFILE", my_config.config["logPath"]))
formatter = logging.Formatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
root.addHandler(handler)
  
    

logging.basicConfig(level=logging.debug)
logging.exception("Exception in main()")

def logging_d(t):
	#logging.debug(t)
	print(t);

def loadDataFromSQL():
	# cmd=my_config.config["sqlserver_loader"]
	# c="%s %s" % (cmd,"redis CSTBC v_node_location_text node_location_id")
    DBTool.CSTBC("v_node_location_text","node_location_id")
	# logging_d(c)
	# os.system(c)
	# c="%s %s" % (cmd,"redis CSTBC v_value_range node_location_id")	
    DBTool.CSTBC("v_value_range","node_location_id")
	# logging_d(c)
	# os.system(c)
	# c="%s %s" % (cmd,"redis CSTBC v_alarm_method alarm_code")	
    DBTool.CSTBC("v_alarm_method","alarm_code")
	# logging_d(c)
	# os.system(c)
	
	
	# c="%s %s" % (cmd,"redis CST  node_alarm_code")
    DBTool.CST2("node_alarm_code")
	 
	# logging_d(c)
	# os.system(c)
	# c="%s %s" % (cmd,"redis CSTBC v_alarm_method alarm_code")
    DBTool.CSTBC("v_alarm_method","alarm_code")
	 
	# logging_d(c)
	# os.system(c)
	
	# c="%s %s" % (cmd,"redis CSTBC v_node_node_client_id node_client_id")
    DBTool.CSTBC("v_node_node_client_id","node_client_id")
	 
	# logging_d(c)
	# os.system(c)
	
	# c="%s %s" % (cmd,"redis CSTBC node_location id")
    DBTool.CSTBC("node_location","id")
	 
	# logging_d(c)
	# os.system(c)
	# c="%s %s" % (cmd,"redis CPT  usp_protocol_detail_list protocol_code,protocol_detil")
    DBTool.CPT2("usp_protocol_detail_list","protocol_code,protocol_detil")
	 
	# logging_d(c)
	# os.system(c)
	# c="%s %s" % (cmd,"redis CSTBC v_node node_location_id")
    DBTool.CSTBC("v_node","node_location_id")
	  
    reorderFormula(); 
    reorderRangeValue();
    reorderNodeLocationText()
    reorderNode();
    reorderProtocalDetail();
	
gAlarmCode ={};

def initMemData():
		global gAlarmCode
		gAlarmCode = loadRangeToJson("node_alarm_code");
		
def reorderProtocalDetail():
    r = loadRangeToJson("protocol_code"); 
    for k in r:
        #k = k.decode("utf-8")
        #logging_d(k );
        doProtocalDetail(k["protocol_code"]);
    #logging_d(r);
    #return r;	

def doProtocalDetail(k):
    rn=[];
    d=loadRangeToJson("protocol_detil")
    k2 =  "protocol_detil:"+k
    for dt in d:
        if(dt["protocol_code"]==k):     
            rn.append(  dt) ; 
    REDIS.delete(k2);
    REDIS.set(k2, str(rn));   
		

def reorderFormula():
    r = REDIS.keys("v_node_location_text:*"); 
    for k in r:
        k = k.decode("utf-8")
        logging_d(k);
        doFormula(k);
    #logging_d(r);
    #return r;	

def doFormula(k):
    rn={};
    d=loadRangeToJson(k)
    
    k = k.replace("v_node_location_text","formula")
    for dt in d:
        #print(k,dt);
        if(   'formula' in dt.keys() and dt["formula"]!=""):     
            rn[dt["node_code"]+"_"+dt["node_cmd_name"]] =  dt ; 
    REDIS.delete(k);
    REDIS.set(k, str(rn));   
        			
def reorderNode():
    r = REDIS.keys("v_node:*"); 
    for k in r:
        k = k.decode("utf-8")
        logging_d(k);
        doReorderNode(k);
    #logging_d(r);
    #return r;		

def reorderRangeValue():
    r = REDIS.keys("v_value_range:*"); 
    for k in r:
        k = k.decode("utf-8")
        #print(k);
        doReorderRangeValue(k);
    #logging_d(r);
    #return r;		
def reorderNodeLocationText():
    r = REDIS.keys("v_node_location_text:*"); 
    for k in r:
        k = k.decode("utf-8")
        logging_d(k);
        doReorderNodeLocationText(k);
    #logging_d(r);
    #return r;
#logging_d (pipe.read())

def doReorderNode(k):

    rn={};
    #print(k)
    try:
        d=loadRangeToJson(k)
    except:
        logging_d(k);
        return;
    
    
    for dt in d: 
        if('node_code' in dt.keys() ):
            rn[dt["node_code"]] =  dt ; 
    REDIS.delete(k);
    REDIS.set(k , str(rn));   

def doReorderNodeLocationText(k):
    rn={};
    d=loadRangeToJson(k)
    for dt in d: 
            rn[dt["node_code"]+"_"+dt["node_cmd_name"]] =  dt ; 
    REDIS.delete(k);
    REDIS.set(k, str(rn));   

def doReorderRangeValue(k):
    rn={};
    d=loadRangeToJson(k)
    for dt in d:
        if( 'type' in dt.keys() and dt["type"] in rn):
            rn[dt["type"]]["data"].append(dt);
        else:
            if( 'alarm_code' in dt.keys() ):
                rn[dt["type"]]={"data":[], "alarm_code":dt["alarm_code"]}#["data"]	=[]
                #rn[dt["type"]]["alarm_code"]	=dt["alarm_code"]
                rn[dt["type"]]["data"].append(dt);
    #logging_d("----------------");
    for d2 in rn:    
        logging_d(d2);#,rn[d2]);
        #logging_d("----------------");
    REDIS.delete(k);
    REDIS.set(k, str(rn));   
        
REDIS = redis.Redis(host= my_config.config["redis_host"], port=my_config.config["redis_port"]) 

MaxRows=200;
def on_connect(mqttc, obj, flags, rc):
    logging_d("rc: " + str(rc))

def loadRangeToJson(key):
    l = REDIS.lrange(key ,0,-1)
    r=[]
    
    for d in l:
        d =d.decode();
        d=d.replace("Decimal(\"", "");
        d=d.replace("\")", "");
        #print(d);
        y = json.loads(d)
        r.append(y);
    #logging_d(r);
    return r;

def loadStringToJson(key):
    l = REDIS.get(key )
    if(l == None):
        return{};
    try:
        l=l.decode("utf-8")
    except:
        logging_d(key);
    #logging_d(l);
    l= l.replace("'",'"')
    #logging_d(l);
    r = json.loads(l) 
    #logging_d(r);
    return r;
    
 
 
#REDIS.flushdb() 
#initMemData();	
	
#loadDataFromSQL();



#@app.route("/")
#def hello():
#    return "Hello from Python3!"

#if __name__ == "__main__":
#    app.run(host='0.0.0.0')
