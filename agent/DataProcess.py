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
import logging
import time
import logging.handlers
import os
import my_config
import taos
import math
#import classes;
#import DataInit;
from datetime import datetime
#print(my_config.config)
"""


 CREATE TABLE   sensor_data2 (
	add_on timestamp  ,
	dt  binary(50) ,
    amount int,
    sensor  binary(50) ,
    sensor_type binary(50), 
    sensor_value binary(5000),
    gateway  binary(50)
)  TAGS ( suser  binary(50),	  sset  binary(50),  sgroup  binary(50));


"""
REDIS = redis.Redis(
    host=my_config.config["redis_host"], port=my_config.config["redis_port"])

logging.basicConfig(level=logging.DEBUG)

def loadRangeToJson(key):
    l = REDIS.lrange(key, 0, -1)
    r = []

    for d in l:
        d = d.decode()
        y = json.loads(d)
        r.append(y)
    # logging.debug(r);
    return r


def loadStringToJson(key):
    l = REDIS.get(key)
    if(l == None):
        return{}
    try:
        l = l.decode("utf-8")
    except:
        logging.debug(key)
    # logging.debug(l);
    l = l.replace("'", '"')
    # logging.debug(l);
    r = json.loads(l)
    # logging.debug(r);
    return r
conn = taos.connect(host=my_config.config["taos_host"],user=my_config.config["taos_user"], password=my_config.config["taos_pwd"])

def sendMqttMessage(topic, msg):
    topic = topic.lower()
    mqttc.publish(topic, msg)
    #logging.debug(topic, msg);

def sort_by_number(s):
    return int(s)

def processData(m, context):
    m = m.split('/')
    # data to json object
    #logging.debug(context)
    # return;
    j = json.loads(context)
    d = []
    nlid = "" 
    print (j, m)
    u = m[1]
    s = m[2]
    group = m[3]
    gateway = m[4]
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt=dt_string
    #dt = j["dt"];
    for d in j :
        #print(d);
        data = j[d]
        t = type(data).__name__
        print(type(data).__name__);
        if(t== 'list'):
            c =0;
            for dd in data:
                sensor = d;
                sensor_type = ''.join([i for i in d if not i.isdigit()])+d[c];
                sensor_value =dd;
                SaveSensorDataToRedis( u,s, group, dt, sensor, sensor_type, sensor_value, gateway )
                c =c +1;
                #print("array")
        elif( t =="dict"):
            sensor = d;
            sensor_type = ''.join([i for i in d if not i.isdigit()]);
            #sorted(data.keys(), key=sort_by_number)
            tmpData="";
            for key in sorted(data.keys(), key=sort_by_number):
                #tmpData = tmpData+key+":"+str(data[key])+","
                tmpData = tmpData+str(data[key])
            sensor_value =tmpData
            sensor_value = sensor_value.replace("\"","");
            sensor_value = sensor_value.replace("'","");
            sensor_value = sensor_value.replace(" ","");
            SaveSensorDataToRedis( u, s, group,dt , sensor, sensor_type, sensor_value, gateway )
        else:
            sensor = d;
            sensor_type = ''.join([i for i in d if not i.isdigit()]);
            sensor_value =data;
            SaveSensorDataToRedis( u, s, group,dt , sensor, sensor_type, sensor_value, gateway )
        #sensor = d["id"];
        #sensor_type = d["t"];
        #sensor_value = d["v"];
        #SaveSensorDataToTaos( u, '1', dt, sensor, sensor_type, sensor_value, gateway )
    #u, g, dt, sensor, sensor_type, sensor_value, gateway
    return
 

def on_message(mqttc, obj, msg):
    m = msg.topic
    #m= m.replace("s/SensorData2", "");
    ms = msg.payload.decode("utf-8")
    ms = ms.replace("'", "\"")
    ms = ms.replace(",,", ",")
    # logging.debug(m,ms)
    topic, msg = convertData(m, ms)
    #logging.debug(topic, msg);
    logging.debug(topic+" "+ msg )
    if(topic != ""):
        #sendMqttMessage(topic, msg)
        processData(topic, msg)


def on_publish(mqttc, obj, mid):
    #logging.debug("mid: " + str(mid))
    m = mid


def on_subscribe(mqttc, obj, mid, granted_qos):
    logging.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    logging.debug(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()


def on_connect(mqttc, obj, flags, rc):
    logging.debug("rc: " + str(rc))

def doMQTT():
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    # Uncomment to enable debug messages
    # mqttc.on_log = on_log
    mqttc.connect(my_config.config["mqtt_host"], 1883, 60)
    print("doMQTT",my_config.config["mqtt_host"])
    mqttc.subscribe("p/#", 0)

    mqttc.loop_forever()


def convertData(topic, msg):
    #print(topic, msg)
    return (topic, msg)


def InitTaos():
    c1 = conn.cursor()
    # Create a database
    c1.execute('create database if not exists appiot  precision "us"')
    c1.execute('use appiot')
    # Create a table
    c1.execute('CREATE TABLE   sensor_data (	add_on timestamp ,     dt binary(50),    sensor  binary(50) ,    sensor_type binary(50),   sensor_value binary(50),    gateway  binary(50))  TAGS ( suser  binary(50),	  sgroup  binary(50));')


def loadStringToJson(key):
    l = REDIS.get(key)
    if(l == None):
        return{}
    try:
        l = l.decode("utf-8")
    except:
        logging.debug(key)
    # logging.debug(l);
    l = l.replace("'", '"')
    # logging.debug(l);
    r = json.loads(l)
    # logging.debug(r);
    return r
#FLUSHALL

def SaveSensorDataToRedis(u, s, g,  dt, sensor, sensor_type, sensor_value, gateway):
    
    key = "sc:"+u+"_"+gateway+"_"+sensor+"_"+sensor_type;
    logging.debug("key " + key)
    r = REDIS.keys(key)
    # logging.debug(data);
    date_format = "%d/%m/%Y %H:%M:%S"
    now = datetime.now()
    dt_string = now.strftime(date_format)
    max_amount =25;
    period_sescond = 300;
    if(len(r) > 0):
        logging.debug("exits")
        r = loadStringToJson(key)
        now2 = datetime.strptime(r["dt"], date_format) 
        d =math.floor((now-now2).total_seconds())
        #if(d > period_sescond):
        if(r["c"] >= max_amount):
            pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway )
            r =   reset(dt_string);
        logging.debug(r)
    else:
        r =   reset(dt_string);

        logging.debug("not exits" + str(r))
    print(r["c"],r["d"])
     
    now2 = datetime.strptime(r["dtl"], date_format) 
    d =math.floor((now-now2).total_seconds())
    i =0;
    exit_flag =0;
    for x in r["d"]:
        if(x["v"] == sensor_value ):
            sensor_value = "#"+str(i);
            break;
        i = i +1; 
    
    r["d"].append ({"d": d, "v": sensor_value});
    #r["d"].append(str( d)+":"+ sensor_value );
    r["c"] =r["c"] +1;
    r["dtl"] =dt_string ;
    REDIS.set(key, str(r))


def reset(dt_string):
    return { 'dt':dt_string,'dtl':dt_string, 'c' : 0, 'd':[]}
    #print (u, s, g,  dt, sensor, sensor_type, sensor_value, gateway)
 
# "{'dt': '25/07/2023 20:14:58', 'dtl': '25/07/2023 20:15:23', 'c': 2, 'd': [{'d': 0, 'v': '15377111111117111111'}, {'d': 25, 'v': '66666666666667666666'}]}"

def pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway):
    sensor_value ="";
    for x in r["d"]:
        v = "%s:%s" %( x["d"], x["v"])
        if(sensor_value ==""):
            sensor_value =  v; 
        else:
            sensor_value = sensor_value +","+v; 
    SaveSensorDataToTaos(u, s, g,  r["dt"],  sensor, sensor_type, sensor_value, gateway, r["c"])

def SaveSensorDataToTaos(u, s, g,  dt,  sensor, sensor_type, sensor_value, gateway, amount):
    #print(nlid, node_code, client_id, sts, data);
    #InitTaos()
    #print(u, s, g,  dt,  sensor, sensor_type, sensor_value, gateway, amount);
    c1 = conn.cursor()
    c1.execute('use appiot;\r\n') 
    #s= "CREATE TABLE  IF NOT EXISTS SensorData%s  USING SensorData TAGS ('%s');\r\n" %( nlid, nlid )

    s2 = "CREATE TABLE  IF NOT EXISTS sensor_data2_"+u +"_" +s +"_" +g+\
        "  USING sensor_data2 TAGS (  '"+u+"','"+s+"','"+g+"');\r\n"  # %( nlid, nlid )
    #print(s2);
    c1.execute(s2)
    sqlcmd = ['insert into sensor_data2_%s_%s_%s  values' % (u, s,  g)]
    #print(sqlcmd);
    sqlcmd.append('(now, \'%s\', %s, \'%s\', \'%s\', \'%s\', \'%s\');' %
                  (dt, amount, sensor, sensor_type, sensor_value, gateway))
    print(' '.join(sqlcmd));
    c1.execute(' '.join(sqlcmd))
    time.sleep(0.01)
    print('sleep 0.01 ');


#di.loadDataFromSQL()

doMQTT()
