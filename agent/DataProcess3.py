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
#import redis
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
#import classes;
#import DataInit;
from datetime import datetime
#print(my_config.config)

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
    logging.debug(context)
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
                SaveSensorDataToTaos( u,s, group, dt, sensor, sensor_type, sensor_value, gateway )
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
            SaveSensorDataToTaos( u, s, group,dt , sensor, sensor_type, sensor_value, gateway )
        else:
            sensor = d;
            sensor_type = ''.join([i for i in d if not i.isdigit()]);
            sensor_value =data;
            SaveSensorDataToTaos( u, s, group,dt , sensor, sensor_type, sensor_value, gateway )
        #sensor = d["id"];
        #sensor_type = d["t"];
        #sensor_value = d["v"];
        #SaveSensorDataToTaos( u, '1', dt, sensor, sensor_type, sensor_value, gateway )
    #u, g, dt, sensor, sensor_type, sensor_value, gateway
    return

def processData_old(m, context):
    m = m.split('/')
    # data to json object
    logging.debug(context)
    # return;
    j = json.loads(context)
    d = []
    nlid = "" 
    print (j, m)
    u = m[1]
    s = m[2]
    gateway = m[3]
    dt = j["dt"];
    for d in j["values"]:

        sensor = d["id"];
        sensor_type = d["t"];
        sensor_value = d["v"];
        SaveSensorDataToTaos( u, '1', dt, sensor, sensor_type, sensor_value, gateway )
    #u, g, dt, sensor, sensor_type, sensor_value, gateway
    return

    formula = loadFormula(nlid)

    last_v = {}
    valT = {}
    for i, val in enumerate(j["Data"]["row"]):
        if(j["node_code"]+"_"+val["t"] in formula):
            f = formula[j["node_code"]+"_"+val["t"]]["formula"]
            #logging.debug("forumla",f )      ;
            # logging.debug(val);
            form = Template(f)
            msg = form.substitute(val)
            #logging.debug("forumla msg>>>",msg )      ;
            exec('val["v"] = ' + msg)
            del formula[j["node_code"]+"_"+val["t"]]

        val["node_code"] = j["node_code"]
        val["sts"] = j["sts"]
        val["nid"] = m[-1]
        valT[val["t"]] = val["v"]
        last_v = val
        d.append(val)
        try:
            for k2 in formula:

                f = formula[k2]  # ["formula"]
                form = Template(f["formula"])
                msg = form.substitute(valT)
                #logging.debug("forumla msg>>>",msg )      ;
                last_v2 = copy.copy(last_v)
                exec('last_v2["v"] = ' + msg)
                last_v2["node_code"] = f["node_code"]
                last_v2["t"] = f["node_cmd_name"]
                # logging.debug(last_v2);
                d.append(last_v2)
        except:
            print("exception")

    d = str(d)
    d = d.replace("'", '"')
    jdata = json.loads(d)
    # create data string for redis

    # logging.debug("jdata",jdata);
    # return;
    d = d.replace("[", "")
    d = d.replace("]", "")
    # use node location id as key
    key = 'SensorData2:'+nlid  # m[-1]
    #logging.debug(key, d)
    # logging.debug(l);
    # save all data as status for each nlid
    setStatus(str(nlid), jdata)
    # only keep latest MaxRows rows for eache data
    pushToRedisAndTrim(key, d, MaxRows)
    #REDIS.ltrim(key,0, MaxRows -1);
    #logging.debug(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    alarmAndActionProcess(nlid)


def on_message(mqttc, obj, msg):
    m = msg.topic
    #m= m.replace("s/SensorData2", "");
    ms = msg.payload.decode("utf-8")
    ms = ms.replace("'", "\"")
    ms = ms.replace(",,", ",")
    # logging.debug(m,ms)
    topic, msg = convertData(m, ms)
    #logging.debug(topic, msg);
    print(topic, msg )
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


def SaveSensorDataToTaos(u, s, g,  dt, sensor, sensor_type, sensor_value, gateway):
    #print(nlid, node_code, client_id, sts, data);
    #InitTaos()
    c1 = conn.cursor()
    c1.execute('use appiot;\r\n') 
    #s= "CREATE TABLE  IF NOT EXISTS SensorData%s  USING SensorData TAGS ('%s');\r\n" %( nlid, nlid )

    s2 = "CREATE TABLE  IF NOT EXISTS sensor_data_"+u +"_" +s +"_" +g+\
        "  USING sensor_data TAGS (  '"+u+"','"+s+"','"+g+"');\r\n"  # %( nlid, nlid )
    #print(s2);
    c1.execute(s2)
    sqlcmd = ['insert into sensor_data_%s_%s_%s  values' % (u, s,  g)]
    #print(sqlcmd);
    sqlcmd.append('(now, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' %
                  (dt, sensor, sensor_type, sensor_value, gateway))
    print(' '.join(sqlcmd));
    c1.execute(' '.join(sqlcmd))
    time.sleep(0.01)
    print('sleep 0.01 ');


#di.loadDataFromSQL()

doMQTT()
