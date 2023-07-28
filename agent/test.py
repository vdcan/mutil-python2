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
import copy
#import classes;
#import DataInit; 
from datetime import datetime, timedelta
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
 
def sort_by_number(s):
    return int(s)
 
def sort_by_date(r): 
  date_format = "%d/%m/%Y %H:%M:%S"
  dt = datetime.strptime(r["dt"], date_format) 
  return int(dt.timestamp())
  
def sort_by_one(r):
    print("sort_by_one",r ,"\r\n");
    #return 0;
    return r["add_on"]
  
 
c="sc:caijie_esp1_rgb1_rgb"
def select(u, gw, s, t, index, size):
    
    key ='sc:'+u+"_"+gw+"_"+s+"_"+t ;
    r=[];
    index = math.ceil(index   /25);
    if(index ==0):
        r = REDIS.keys(key) 
        if(len(r) > 0):
            r = loadStringToJson(key)
            r = restoreData(r,u, gw, s, t)
    c =  selectFromTaos(r) 

    r2 ={"iTotalRecords": c,
      "iTotalDisplayRecords":c,
      "aaData":r
      } 
    
    songsJSON =json.dumps(r2, indent=4, sort_keys=True, default=str)
    #print (songsJSON)
    return songsJSON;
 
def selectFromTaos(ra):
  date_format = "%d/%m/%Y %H:%M:%S"
  start = 0
  length = 1
  search = ''
  where =''
  
  if(search !=""):
     where = " where suser ='"+search +"'"
  query =  "select  sum(amount) c from appiot.sensor_data2   {where} ;".format(where = where)
  #print(query);
  result: taos.TaosResult = conn.query(query)
  rows = result.fetch_all_into_dict()
  c =0
  for entry in rows: 
      c= int(entry['c'])

  #result: taos.TaosResult = conn.query(query )
  query =  "select * from appiot.sensor_data2   {where}  order by add_on  desc limit {start}, {length}  ;".format(where = where, start= start, length = length)
  print(query);
  #return;
  result: taos.TaosResult = conn.query(query)
  rows = result.fetch_all_into_dict()
  print("row count:", result.row_count)
  print("===============all data===================")
  for entry in rows: 
      
    da =[];
    entry['add_on'] = int(entry['add_on'].timestamp())
    data = entry['sensor_value'].split(",")
    dt = datetime.strptime(entry["dt"], date_format) 
    for d in data:
        dataObj = copy.deepcopy(entry);
        da1 = d.split(":")
        df = da1[0]
        dv = da1[1] 
        #print(df, dv)
        if (dv.startswith("#")):
            #print(x["v"])
            #print(dv[1:])
            dv =da[ int(dv[1:])]["sensor_value"]; 
        dt = dt  + timedelta(seconds=int(df, 10)) 
        print(dt.strftime(date_format), dv)
        dataObj["dt"] =  dt.strftime(date_format);
        dataObj["sensor_value"] =  dv;
        da.append(dataObj);
        #da.append({"dt": dt.strftime(date_format), "v": dv}) 
  ra.extend(da);      
  songsJSON =json.dumps(da, indent=4, sort_keys=True, default=str)
  print (songsJSON)
  ra =   sorted(ra, key=lambda x: datetime.strptime(x["dt"], "%d/%m/%Y %H:%M:%S"))
  """
  r ={"iTotalRecords": c,
      "iTotalDisplayRecords":c,
      "aaData":rows
      }
  #print(ra)
  r1 = sorted(ra, key=sort_by_date, reverse=True )#,  key=lambda x: int( x["add_on"]))
  #sorted_dates = sorted(ra, key=lambda x: datetime.strptime(x["dt"], "%d/%m/%Y %H:%M:%S"))

  #ra.sort(key=sort_by_date x: x.dt)
  print(sorted_dates);
  
  songsJSON =json.dumps(r, indent=4, sort_keys=True, default=str)
  return songsJSON;
"""
  return c;
def restoreData(r, u, gw, s, t):
    
    date_format = "%d/%m/%Y %H:%M:%S"
    dt =  datetime.strptime(r["dt"], date_format) 
    da =[];
    counter =0;
    for x in r["d"]:
        dt = dt  + timedelta(seconds=x["d"]) 
        v ="";
        if (x["v"].startswith("#")):
            #print(x["v"])
            v =da[ int(x["v"][1:])]["sensor_value"];
        else:
            v = x["v"];
        da.append({"add_on":counter, "dt": dt.strftime(date_format), "sensor_value": v,
                   'amount': 25, 'sensor': s, 'sensor_type': t, 'gateway': gw, 'suser': u, 'sset': 's', 'sgroup': 'g'}) 
        counter = counter+1
    #print(da);
    return da;



def SaveSensorDataToRedis(u, s, g,  dt, sensor, sensor_type, sensor_value, gateway):
    
    key = "sc:"+u+"_"+gateway+"_"+sensor+"_"+sensor_type;
    logging.debug("key " + key)
    r = REDIS.keys(key)
    # logging.debug(data);
    date_format = "%d/%m/%Y %H:%M:%S"
    now = datetime.now()
    dt_string = now.strftime(date_format)
    period_sescond = 300;


    if(len(r) > 0):
        logging.debug("exits")
        r = loadStringToJson(key)
        now2 = datetime.strptime(r["dt"], date_format) 
        d =math.floor((now-now2).total_seconds())
        if(d > period_sescond):
            #pSaveSensorDataToTaos(u, s, g,    sensor, sensor_type, r, gateway )
            r =   reset(dt_string);
        logging.debug(r)
    else:
        r =  {}# reset(dt_string);

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


select('caijie','esp1','rgb1','rgb', 0, 10);