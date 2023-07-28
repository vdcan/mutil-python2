# This file is part of https://github.com/jainamoswal/Flask-Example.
# Usage covered in <IDC lICENSE>
# Jainam Oswal. <jainam.me> 


# Import Libraries 
from app import app
from flask import jsonify

from datetime import date
from flask import request
import json

import taos
import redis
import math
import copy

import logging
from datetime import datetime, timedelta
from ctypes import * 
config={
"logPath":"/yourapp.log",
"redis":" jssqlredis",
"redis_host":"iot_redis",
"redis_port":6379,
"sqlserver_loader":"E:\\workdir\\MQTTJSql\\JSBaseTDSSO_test\\bin\\Debug\\JSBaseTDSSO_test.exe",

"taos_host":"iot_taosdb",
"taos_user":"root",

"taos_pwd":"taosdata",
}

#import classes;
#import DataInit;

#print(my_config.config)

conn = taos.connect(host=config["taos_host"],user=config["taos_user"], password=config["taos_pwd"])
# Define route "/api".
@app.route('/api')
def api():
  # return in JSON format. (For API)
  return jsonify({"message":"Hello from Flask!"})


@app.route('/listresult', methods=['POST' ])
def fetch_all_demo(): 
  start = request.form.get('start', default = '0', type = str) 
  length = request.form.get('length', default = '10', type = str) 
  search = request.form.get('search[value]', default = '', type = str) 
  #search = request.args.get('search[value]', default = '', type = str) 
  where ="";
  search = search.replace("'","");
  
  search = search.replace(";","");
  
  if(search !=""):
     where = " where suser ='"+search +"'"
  query =  "select  count(*) c from appiot.sensor_data   {where} ;".format(where = where)
  #print(query);
  result: taos.TaosResult = conn.query(query)
  rows = result.fetch_all_into_dict()
  c =0
  for entry in rows: 
      c= int(entry['c'])
  print (c)
  #result: taos.TaosResult = conn.query(query )
  query =  "select * from appiot.sensor_data   {where}  order by add_on  desc limit {start}, {length}  ;".format(where = where, start= start, length = length)
  print(query);
  #return;
  result: taos.TaosResult = conn.query(query)
  rows = result.fetch_all_into_dict()
  print("row count:", result.row_count)
  print("===============all data===================")
  for entry in rows: 
      entry['add_on'] = int(entry['add_on'].timestamp())
  r ={"iTotalRecords": c,
      "iTotalDisplayRecords":c,
      "aaData":rows
      }
  #print(r)
  
  songsJSON =json.dumps(r, indent=4, sort_keys=True, default=str)
  return songsJSON;


@app.route('/listresult2', methods=['POST' ])
def fetch_all_demo2(): 
  start = request.form.get('start', default = '0', type = str) 
  length = request.form.get('length', default = '10', type = str) 
  search = request.form.get('search[value]', default = '', type = str) 
  #search = request.args.get('search[value]', default = '', type = str) 
  where ="";
  search = search.replace("'","");
  
  search = search.replace(";","");
  
  if(search !=""):
     where = " where suser ='"+search +"'"
  
  return select('caijie','esp1','rgb1','rgb',int(start) , 1);
 
REDIS = redis.Redis(
    host=config["redis_host"], port=config["redis_port"])

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
#conn = taos.connect(host=config["taos_host"],user=config["taos_user"], password=config["taos_pwd"])
 
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

    r = sorted(r, key=lambda x: datetime.strptime(x["dt"], "%d/%m/%Y %H:%M:%S"),reverse=True)
    r2 ={"iTotalRecords": c,
      "iTotalDisplayRecords":c,
      "aaData":r
      } 
    
    songsJSON =json.dumps(r2, indent=4, sort_keys=True, default=str)
    print (songsJSON)
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
    #dataObj = copy.deepcopy(entry);
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
        dataObj["dt"] =  dt.strftime(date_format);
        dataObj["sensor_value"] =  dv;
        da.append(dataObj);
        #da.append({"dt": dt.strftime(date_format), "v": dv}) 
  ra.extend(da);      
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
