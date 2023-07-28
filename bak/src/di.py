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
import DataInit;
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

def loadDataFromSQL3():
	DBTool.mysql_redis("vd_user")

def loadDataFromSQL():	
 
    DBTool.mysql_redis("vd_user")
    DBTool.mysql_redis("vd_action")
    DBTool.mysql_redis("vd_menu")
    DBTool.mysql_redis("v_button")
    DBTool.mysql_redis("mqtt_device_specification")
    DBTool.mysql_redis("vd_user")

    reorderUser();
    reorderMenu();
    reorderButton();
    reorderMQTTDeviceS();
    reorderAction();
	 
def runCMD(c):
	cmd=my_config.config["sqlserver_loader"]
	c="%s %s" % (cmd,c)
	logging_d(c)
	os.system(c)

def reorderMQTTDeviceS():
    r = loadRangeToJson("mqtt_device_specification"); 
    for k in r:
        #k = k.decode("utf-8")
        #logging_d(k );
        doActionMQTTDeviceS('', k);
    #logging_d(r);
    REDIS.delete("mqtt_device_specification");
    #return r;	

def doActionMQTTDeviceS(key, value):
    rn=[]; 
    k2 =  "usp_MQTTDeviceS_pager"#+key
    REDIS.lpush(k2, str(value));   
    	
	
def reorderAction():
    r = loadRangeToJson("vd_action"); 
    for k in r:
        #k = k.decode("utf-8")
        #logging_d(k );
        #doActionDetail(k["app_code"], k);
        doActionDetail(str(k["id"]), k);
    #logging_d(r);
    #REDIS.delete("vd_action");
    #return r;	

def doActionDetail(key, value):
    rn=[]; 
    k2 =  "vd_action:"+key
    REDIS.lpush(k2, str(value));   
    
def doActionIDDetail(key, value):
    rn=[]; 
    k2 =  "vd_action:"+key
    REDIS.lpush(k2, str(value));   
	
def reorderButton():
    r = loadRangeToJson("v_button"); 
    for k in r:
        #k = k.decode("utf-8")
        #logging_d(k );
        doButtonDetail(k["menu_code"], k);
    #logging_d(r);
    REDIS.delete("vd_button");
    #return r;	

def doButtonDetail(key, value):
    rn=[]; 
    k2 =  "v_button:"+key
    REDIS.lpush(k2, str(value));   
    	
def reorderUser():
    r = loadRangeToJson("vd_user"); 
    for k in r:
        #k = k.decode("utf-8")
        #logging_d(k );
        doUserDetail(k["user_code"], k);
    #logging_d(r);
    REDIS.delete("vd_user");
    #return r;	

def doUserDetail(key, value):
    rn=[]; 
    k2 =  "vd_user:"+key
    REDIS.set(k2, str(value));   
		 

def reorderMenu():
    r = loadRangeToJson("vd_menu"); 
    
    m={};
    for k in r: 
        if(k["app_code"] not in m.keys()):
            m[k["app_code"]]=k["app_code"]
        if(k["visible_flag"] ==1 and k["enabled"] ==1):
            doMenuDetail(k["app_code"], k);
    #logging_d(r);
    #print(m);
    for k2 in m.keys():
        if(k2!=""):
            for k in r:  
                if(k["visible_flag"] ==1 and k["enabled"] ==1 and k["app_code"]==''):
                    doMenuDetail(k2, k); 
    REDIS.delete("vd_menu");
    #return r;
    
def addMenu():
    r = REDIS.keys("vd_menu:*"); 
    for k in r:
        k = k.decode("utf-8")
        logging_d(k);
        doFormula(k);
 
        
def doMenuDetail(key, value):
    rn=[]; 
    k2 =  "vd_menu:"+key+'_'+ str(value["menu_type"])
    icon_class = value["icon_class"]
    icon_class = icon_class.replace('icon-standard-','')
    icon_class = icon_class.replace('icon-hamburg-','')
    icon_class = icon_class.replace('icon-metro-','')
    icon_class= '/Scripts/03jeasyui/icons/icon-standard/16x16/' +icon_class +'.png'
    value["icon"]=icon_class
    value["menu_token"]=value["url"]+"-"+value["menu_code"]
    REDIS.lpush(k2, str(value));   	
 
        
REDIS = redis.Redis(host= my_config.config["redis_host"], port=my_config.config["redis_port"]) 

MaxRows=200;
def on_connect(mqttc, obj, flags, rc):
    logging_d("rc: " + str(rc))

def loadRangeToJson(key):
    l = REDIS.lrange(key ,0,-1)
    r=[]
    
    for d in l:
        #print(d);
        d =d.decode();
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

def loadTextToRedis():   
    print("loadTextToRedis"); 
 

    thisdir = os.getcwd()

    # r=root, d=directories, f = files
    for r, d, f in os.walk("redis"):
        for file in f:
            if file.endswith(".txt"):
                #print (file);
                redisName = file;
                #redisName = file[4:];
                redisName = redisName.replace(".txt","");
                redisName = redisName.replace("_colon_",":");
                print (redisName);
                f = open("redis"+os.path.sep+file, "r", encoding='UTF-8')
                REDIS.lpush(redisName,f.read());
                #print(f.read())
REDIS.flushdb() 
DataInit.loadDataFromSQL();
loadTextToRedis(); 
loadDataFromSQL();