import time
import unittest
import json
import redis
import json
from datetime import datetime
from datetime import timedelta  
import my_config;
import logging
import math
import os

from pypipeline.components.source.MQTTSource import MQTTIn
from pypipeline.components.destination.TaosDest import SaveSensorData
from pypipeline.components.source.Timer import Timer
from pypipeline.core.Destination import Destination
from pypipeline.core.DslPipelineBuilder import DslPipelineBuilder
from pypipeline.core.Plumber import Plumber
from pypipeline.core.Message import Message

logging.basicConfig(level=logging.DEBUG)
import my_config;
REDIS = redis.Redis(
    host=my_config.config["redis_host"], port=my_config.config["redis_port"])

mqtt_user ="caijie2"
class MQTTPipeline(unittest.TestCase):

    def test_simple_pipeline(self):
        plumber = Plumber()
        builder1 = DslPipelineBuilder()
        #pipeline1 = builder1.source(MQTTIn, {"topic": "p/caijie/#"}).to(processData).to(SaveSensorData, {"template": "tao_sensor_data2_insert.tp"}).process(lambda ex: print(ex.out_msg.body))
        
        #pipeline1 = builder1.source(MQTTIn, {"topic": "p/caijie/#"}).to(processData).wiretap((SaveSensorData, {"template": "tao_sensor_data2_insert.tp"}))#.process(lambda ex: print(ex.out_msg.body))
        pipeline1 = builder1.source(MQTTIn, {"topic": "p/"+mqtt_user+"/#"}).multicast({})\
            .pipeline().to(processData).to(SaveSensorData, {"template": "tao_sensor_data2_insert.tp"}).end_pipeline()\
            .end_multicast().process(lambda ex: print(ex.out_msg.body))
            #.pipeline().to(SaveSensorData, {"template": "tao_sensor_data2_insert.tp"}).end_pipeline()\
        plumber.add_pipeline(pipeline1)
        plumber.start()
        time.sleep(1)
        plumber.stop()

"""

p/caijie2/a4cf1256/init
{}


p/caijie2/a4cf1256/data
{"rgb1":{"15":0,"7":0,"6":0,"10":0,"11":0,"1":0,"0":0,"3":0,"2":0,"12":0,"13":0,"9":0,"8":0,"16":0,"17":0,"18":0,"19":0,"5":0,"4":0,"14":0}}

p/caijie2/a4cf1256/set 
{"g":"g2", "s":"s2", "gw":"gw1"}

def slip(exchange):
    return [
        (D1, {}),
        (D2, {})
    ]
""" 

def sort_by_number(s):
    return int(s)

def getGW(m):
    return "gw_"+ m[-2] ;

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

def SaveSensorDataToRedis(da, u, s, g,  dt, sensor, sensor_type, sensor_value, gateway):
    
    key = "sc:"+u+"_"+gateway+"_"+sensor+"_"+sensor_type; 
    r = REDIS.keys(key)
    # logging.debug(data);
    date_format = "%d/%m/%Y %H:%M:%S"
    now = datetime.now()
    dt_string = now.strftime(date_format)
    max_amount =3;
    period_sescond = 300;
    if(len(r) > 0):
        #logging.debug("exits")
        r = loadStringToJson(key)
        now2 = datetime.strptime(r["dt"], date_format) 
        d =math.floor((now-now2).total_seconds())
        #if(d > period_sescond):
        if(r["c"] >= max_amount):
            pSaveSensorDataToTaos(da, u, s, g,    sensor, sensor_type, r, gateway )
            r =   reset(dt_string);
        #logging.debug(r)
    else:
        r =   reset(dt_string);

        #logging.debug("not exits" + str(r))
    #print(r["c"],r["d"])
     
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


def pSaveSensorDataToTaos(da, u, s, g,    sensor, sensor_type, r, gateway):
    sensor_value ="";
    for x in r["d"]:
        v = "%s:%s" %( x["d"], x["v"])
        if(sensor_value ==""):
            sensor_value =  v; 
        else:
            sensor_value = sensor_value +","+v; 
     
    da.append({"u":u,"s":s, "g":g, "dt":r["dt"], "sensor":sensor, "sensor_type":sensor_type , "sensor_value":sensor_value, "gateway":gateway, "amount": r["c"] })
    #SaveSensorDataToTaos(da, u, s, g,  r["dt"],  sensor, sensor_type, sensor_value, gateway, r["c"])

dt_format ="%d/%m/%Y %H:%M:%S"
def reset(dt_string):
    return { 'dt':dt_string,'dtl':dt_string, 'c' : 0, 'd':[]}
    #print (u, s, g,  dt, sensor, sensor_type, sensor_value, gateway)

def getGateWayInfo(gateway):
    r = loadStringToJson(gateway); 
    now = datetime.now()
    dt_string = now.strftime(dt_format)
    if(r=={}): 
        return r;
    else:
        if(r["expire_dt"]==""):
            expire_dt = now + timedelta(days=20)  
            expire_dt = expire_dt.strftime(dt_format)
            r[ "expire_dt"] = expire_dt ;
            REDIS.set(gateway, str(r))
            
    return r;

#used for inerting gw to the system
def initGateWay(gateway):
    r = loadStringToJson(gateway);
    now = datetime.now()
    dt_string = now.strftime(dt_format)
    #if(r=={}):  
    r={"dt":dt_string,"s":"","g":"", "gw":"","expire_dt":"" }
    REDIS.set(gateway, str(r))

    return r;


def setGateWay(gateway,d):
    r = loadStringToJson(gateway);
    now = datetime.now()
    dt_string = now.strftime(dt_format)
    if(r!={}):  
        r={"dt":dt_string,"s":d["s"],"g":d["g"],"gw":d["gw"], "expire_dt":"" }
        print("setGateWay", gateway ,r)
        REDIS.set(gateway, str(r))

    return r;

def processMessage(topic, message):
    print(topic)
    m = topic.split('/')
    # data to json object
    #logging.debug(context)
    cmd= m[-1] 
    gateway =getGW(m)
    d = []
    if(cmd =="init"):
        initGateWay(gateway)
        return d
    if(cmd =="set"):
        setGateWay(gateway, message)
        return d
    if(cmd =="data"):
        d= processGWData(topic, message)
        return d;
    
    if(cmd =="exit"):
        os._exit(1)
    
    return d;


def processGWData(topic, message):
    print(topic)
    m = topic.split('/')
    # data to json object
    #logging.debug(context)
    cmd= m[-1] 
    gateway =getGW(m) 
    d = [] 

    r = getGateWayInfo(gateway)
    u =   m[1]
    s = ''
    group =  ''
    #gateway = m[2]
    print("processGWData:",r)
    now = datetime.now()
    
    if(r!={}):
        s = r["s"]
        group = r["g"] 
        gateway = r["gw"] 
        expire_dt = r["expire_dt"] 
        converted_datetime = datetime.strptime(expire_dt, dt_format)
        if(converted_datetime < now):
            print("gateway ", gateway ,"expired at ", expire_dt)
            return d;
    else: # gw is not in the system
        print("gateway ", gateway ," is not in the system")
        return d;

    j = message
    nlid = ""  

    
    

    dt_string = now.strftime(dt_format)
    dt=dt_string
    #dt = j["dt"];
    da =[] 
    for d in j :
        #print(d);
        data = j[d]
        t = type(data).__name__
        #print(type(data).__name__);
        if(t== 'list'):
            c =0;
            for dd in data:
                sensor = d;
                sensor_type = ''.join([i for i in d if not i.isdigit()])+d[c];
                sensor_value =dd;
                #da.append({"u":u,"s":s, "g":group, "dt":dt, "sensor":sensor, "sensor_type":sensor_type , "sensor_value":sensor_value, "gateway":gateway, "amount":0 })
                SaveSensorDataToRedis( da, u,s, group, dt, sensor, sensor_type, sensor_value, gateway )
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
            #da.append({"u":u,"s":s, "g":group, "dt":dt, "sensor":sensor, "sensor_type":sensor_type , "sensor_value":sensor_value, "gateway":gateway , "amount":0 })
            SaveSensorDataToRedis( da, u, s, group,dt , sensor, sensor_type, sensor_value, gateway )
        else:
            sensor = d;
            sensor_type = ''.join([i for i in d if not i.isdigit()]);
            sensor_value =data; 
            SaveSensorDataToRedis(da,  u, s, group,dt , sensor, sensor_type, sensor_value, gateway ) 
    
    return da

 

class processData(Destination):
    def process(self, exchange):
        r = processMessage(exchange.in_msg.body["topic"], exchange.in_msg.body["message"])
        #print( r );
        m = Message();
        m.body = r;
        exchange.out_msg = m;
        #print(str(exchange.in_msg.body) + " D1")


class D2(Destination):
    def process(self, exchange):
        print(exchange.in_msg.body + " D2")